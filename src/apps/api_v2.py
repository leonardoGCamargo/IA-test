"""
FastAPI v2 - API Gateway completo para sistema multi-agente
Inclui endpoints para agentes, WebSockets, integração com LangGraph e LangSmith
"""

import os
import json
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import uvicorn
import socketio
from socketio import ASGIApp
try:
    from langsmith import Client as LangSmithClient
except ImportError:
    LangSmithClient = None

# Carrega variáveis de ambiente
if os.path.exists(".env"):
    load_dotenv(".env")
elif os.path.exists("config/.env"):
    load_dotenv("config/.env")

# Importações do sistema
from src.agents.orchestrator_langgraph import get_langgraph_orchestrator
from src.agents.mcp_manager import get_mcp_manager
from src.agents.mcp_neo4j_integration import get_neo4j_manager

# Configuração LangSmith
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT", "ia-test")
langsmith_client = None
if LANGCHAIN_API_KEY and LangSmithClient:
    try:
        langsmith_client = LangSmithClient(api_key=LANGCHAIN_API_KEY)
    except Exception as e:
        print(f"⚠️ Erro ao inicializar LangSmith: {e}")

# Socket.IO Server
sio = socketio.AsyncServer(
    cors_allowed_origins="*",
    async_mode='asgi'
)

# Gerenciador de conexões WebSocket (para WebSocket nativo do FastAPI)
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.agent_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, agent_id: Optional[str] = None):
        await websocket.accept()
        self.active_connections.append(websocket)
        if agent_id:
            if agent_id not in self.agent_connections:
                self.agent_connections[agent_id] = []
            self.agent_connections[agent_id].append(websocket)

    def disconnect(self, websocket: WebSocket, agent_id: Optional[str] = None):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        if agent_id and agent_id in self.agent_connections:
            if websocket in self.agent_connections[agent_id]:
                self.agent_connections[agent_id].remove(websocket)

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        await websocket.send_json(message)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass

    async def send_to_agent(self, agent_id: str, message: dict):
        # Envia via Socket.IO também
        await sio.emit('agent_status', message, room=agent_id)
        # E via WebSocket nativo
        if agent_id in self.agent_connections:
            for connection in self.agent_connections[agent_id]:
                try:
                    await connection.send_json(message)
                except:
                    pass

manager = ConnectionManager()

# Socket.IO Event Handlers
@sio.event
async def connect(sid, environ):
    print(f"Socket.IO client conectado: {sid}")

@sio.event
async def disconnect(sid):
    print(f"Socket.IO client desconectado: {sid}")

@sio.event
async def subscribe_agent(sid, data):
    agent_id = data.get('agent_id')
    if agent_id:
        sio.enter_room(sid, agent_id)
        await sio.emit('subscribed', {'agent_id': agent_id}, room=sid)

# Modelos Pydantic
class AgentExecuteRequest(BaseModel):
    goal: str = Field(..., description="Objetivo ou tarefa em linguagem natural")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Parâmetros adicionais")

class WorkflowExecuteRequest(BaseModel):
    inputs: Dict[str, Any] = Field(default_factory=dict, description="Inputs do workflow")

class MemoryQueryRequest(BaseModel):
    query: str = Field(..., description="Query Cypher ou pergunta em linguagem natural")
    limit: int = Field(default=10, ge=1, le=100)

# Inicialização do app
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Inicializando FastAPI v2...")
    try:
        # Inicializa orchestrator LangGraph
        orchestrator = get_langgraph_orchestrator()
        app.state.orchestrator = orchestrator
        print("✅ LangGraph Orchestrator inicializado")
    except Exception as e:
        print(f"⚠️ Erro ao inicializar orchestrator: {e}")
        app.state.orchestrator = None
    
    try:
        mcp_manager = get_mcp_manager()
        app.state.mcp_manager = mcp_manager
        print("✅ MCP Manager inicializado")
    except Exception as e:
        print(f"⚠️ Erro ao inicializar MCP Manager: {e}")
        app.state.mcp_manager = None
    
    try:
        neo4j_manager = get_neo4j_manager()
        app.state.neo4j_manager = neo4j_manager
        print("✅ Neo4j Manager inicializado")
    except Exception as e:
        print(f"⚠️ Erro ao inicializar Neo4j Manager: {e}")
        app.state.neo4j_manager = None
    
    yield
    
    # Shutdown
    print("🛑 Encerrando FastAPI v2...")

app = FastAPI(
    title="IA-Test Multi-Agent API",
    description="API Gateway para sistema multi-agente com LangGraph, Neo4j e Kestra",
    version="2.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar domínios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== HEALTH CHECK ====================

@app.get("/")
async def root():
    return {
        "message": "IA-Test Multi-Agent API v2",
        "status": "running",
        "version": "2.0.0"
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "orchestrator": app.state.orchestrator is not None,
        "mcp_manager": app.state.mcp_manager is not None,
        "neo4j_manager": app.state.neo4j_manager is not None,
        "langsmith": langsmith_client is not None
    }

# ==================== AGENTS ENDPOINTS ====================

@app.get("/api/v1/agents")
async def get_agents():
    """Lista todos os agentes disponíveis"""
    if not app.state.orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator não disponível")
    
    try:
        agents = app.state.orchestrator.list_agents()
        return {"agents": agents}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/agents/{agent_id}")
async def get_agent(agent_id: str):
    """Obtém detalhes de um agente específico"""
    if not app.state.orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator não disponível")
    
    try:
        agent = app.state.orchestrator.get_agent_info(agent_id)
        if not agent:
            raise HTTPException(status_code=404, detail="Agente não encontrado")
        return agent
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/agents/{agent_id}/execute")
async def execute_agent(agent_id: str, request: AgentExecuteRequest):
    """Executa um agente com um objetivo"""
    if not app.state.orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator não disponível")
    
    try:
        # Envia status inicial via WebSocket
        await manager.send_to_agent(
            agent_id,
            {
                "type": "agent_status",
                "agent_id": agent_id,
                "status": "starting",
                "message": f"Iniciando execução: {request.goal}",
                "timestamp": datetime.utcnow().isoformat()
            }
        )
        
        # Executa o agente
        result = await app.state.orchestrator.execute_agent_async(
            agent_id=agent_id,
            goal=request.goal,
            parameters=request.parameters
        )
        
        # Envia resultado via WebSocket
        await manager.send_to_agent(
            agent_id,
            {
                "type": "agent_status",
                "agent_id": agent_id,
                "status": "completed",
                "message": "Execução concluída",
                "data": result,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
        
        return result
    except Exception as e:
        await manager.send_to_agent(
            agent_id,
            {
                "type": "agent_status",
                "agent_id": agent_id,
                "status": "error",
                "message": f"Erro: {str(e)}",
                "timestamp": datetime.utcnow().isoformat()
            }
        )
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/agents/{agent_id}/status")
async def get_agent_status(agent_id: str):
    """Obtém status atual de um agente"""
    if not app.state.orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator não disponível")
    
    try:
        status = app.state.orchestrator.get_agent_status(agent_id)
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== SYSTEM STATUS ====================

@app.get("/api/v1/system/status")
async def get_system_status():
    """Obtém status geral do sistema"""
    if not app.state.orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator não disponível")
    
    try:
        status = app.state.orchestrator.get_system_status()
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== TASKS ENDPOINTS ====================

@app.get("/api/v1/tasks")
async def get_tasks():
    """Lista todas as tarefas"""
    if not app.state.orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator não disponível")
    
    try:
        tasks = app.state.orchestrator.list_tasks()
        return {"tasks": tasks}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/tasks/{task_id}")
async def get_task(task_id: str):
    """Obtém detalhes de uma tarefa"""
    if not app.state.orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator não disponível")
    
    try:
        task = app.state.orchestrator.get_task(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Tarefa não encontrada")
        return task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== WORKFLOWS (KESTRA) ====================

@app.get("/api/v1/workflows")
async def get_workflows():
    """Lista workflows Kestra disponíveis"""
    # TODO: Integrar com Kestra API
    return {"workflows": []}

@app.post("/api/v1/workflows/{workflow_id}/execute")
async def execute_workflow(workflow_id: str, request: WorkflowExecuteRequest):
    """Executa um workflow Kestra"""
    # TODO: Integrar com Kestra API
    return {"message": "Workflow execution not yet implemented"}

# ==================== MEMORY (NEO4J) ====================

@app.post("/api/v1/memory/query")
async def query_memory(request: MemoryQueryRequest):
    """Consulta a memória Neo4j"""
    if not app.state.neo4j_manager:
        raise HTTPException(status_code=503, detail="Neo4j Manager não disponível")
    
    try:
        result = app.state.neo4j_manager.query_graphrag(
            query=request.query,
            limit=request.limit
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== LANGSMITH TRACES ====================

@app.get("/api/v1/traces")
async def get_traces(limit: int = 50):
    """Obtém traces do LangSmith"""
    if not langsmith_client:
        raise HTTPException(status_code=503, detail="LangSmith não configurado")
    
    try:
        runs = langsmith_client.list_runs(
            project_name=LANGCHAIN_PROJECT,
            limit=limit
        )
        traces = []
        for run in runs:
            traces.append({
                "id": str(run.id),
                "name": run.name,
                "start_time": run.start_time.isoformat() if run.start_time else None,
                "end_time": run.end_time.isoformat() if run.end_time else None,
                "status": run.status,
                "inputs": run.inputs,
                "outputs": run.outputs,
            })
        return {"traces": traces}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== WEBSOCKET ====================

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket para comunicação em tempo real"""
    await manager.connect(websocket)
    agent_id = None
    try:
        while True:
            data = await websocket.receive_json()
            # Processa mensagens do cliente
            if data.get("type") == "subscribe_agent":
                agent_id = data.get("agent_id")
                await manager.connect(websocket, agent_id)
                await manager.send_personal_message(
                    {"type": "subscribed", "agent_id": agent_id},
                    websocket
                )
    except WebSocketDisconnect:
        manager.disconnect(websocket, agent_id)

@app.websocket("/ws/agent/{agent_id}")
async def websocket_agent_endpoint(websocket: WebSocket, agent_id: str):
    """WebSocket específico para um agente"""
    await manager.connect(websocket, agent_id)
    try:
        while True:
            data = await websocket.receive_json()
            # Processa mensagens específicas do agente
            await manager.send_personal_message(
                {"type": "ack", "data": data},
                websocket
            )
    except WebSocketDisconnect:
        manager.disconnect(websocket, agent_id)

# ==================== MAIN ====================

# Monta Socket.IO no FastAPI
socketio_app = ASGIApp(sio, app)

# Para compatibilidade, mantém app como principal
# Mas socketio_app deve ser usado no uvicorn
app.mount("/socket.io", socketio_app)

if __name__ == "__main__":
    uvicorn.run(
        socketio_app,  # Usa socketio_app para suportar Socket.IO
        host="0.0.0.0",
        port=8504,
        reload=True,
        log_level="info"
    )

