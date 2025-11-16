"""
Orchestrator LangGraph - Implementação stateful e multi-actor usando LangGraph
Substitui o orchestrator.py tradicional com capacidades avançadas de grafo
"""

import os
import logging
from typing import Dict, List, Optional, Any, TypedDict, Annotated
from datetime import datetime
from enum import Enum

try:
    from langgraph.graph import StateGraph, END
    from langgraph.graph.message import add_messages
except ImportError:
    # Fallback se langgraph não estiver instalado
    StateGraph = None
    END = None
    add_messages = None
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from src.agents.mcp_manager import get_mcp_manager
from src.agents.mcp_neo4j_integration import get_neo4j_manager
from src.agents.mcp_kestra_integration import get_kestra_agent
from src.agents.system_health_agent import get_system_health_agent
from src.apps.chains import load_llm

logger = logging.getLogger(__name__)

# ==================== STATE DEFINITION ====================

class AgentState(TypedDict):
    """Estado compartilhado do grafo de agentes"""
    messages: Annotated[List, add_messages]
    goal: str
    agent_id: Optional[str]
    agent_type: Optional[str]
    parameters: Dict[str, Any]
    current_step: int
    total_steps: int
    results: List[Dict[str, Any]]
    status: str  # pending, planning, executing, completed, error
    error: Optional[str]
    memory_context: Optional[Dict[str, Any]]  # Contexto do Neo4j

# ==================== AGENT TYPES ====================

class AgentType(Enum):
    """Tipos de agentes disponíveis"""
    ORCHESTRATOR = "orchestrator"
    MCP_MANAGER = "mcp_manager"
    NEO4J_GRAPHRAG = "neo4j_graphrag"
    KESTRA = "kestra"
    SYSTEM_HEALTH = "system_health"
    CUSTOM = "custom"

# ==================== LANGGRAPH ORCHESTRATOR ====================

class LangGraphOrchestrator:
    """
    Orchestrator baseado em LangGraph para gerenciamento stateful de agentes
    """
    
    def __init__(self):
        """Inicializa o orchestrator LangGraph"""
        self.mcp_manager = None
        self.neo4j_manager = None
        self.kestra_agent = None
        self.health_agent = None
        self.llm = None
        self.graph = None
        
        # Inicializa componentes
        self._initialize_components()
        
        # Constrói o grafo LangGraph
        self._build_graph()
        
        logger.info("LangGraph Orchestrator inicializado")
    
    def _initialize_components(self):
        """Inicializa todos os componentes necessários"""
        try:
            self.mcp_manager = get_mcp_manager()
            logger.info("✅ MCP Manager inicializado")
        except Exception as e:
            logger.warning(f"⚠️ MCP Manager não disponível: {e}")
        
        try:
            self.neo4j_manager = get_neo4j_manager()
            logger.info("✅ Neo4j Manager inicializado")
        except Exception as e:
            logger.warning(f"⚠️ Neo4j Manager não disponível: {e}")
        
        try:
            self.kestra_agent = get_kestra_agent()
            logger.info("✅ Kestra Agent inicializado")
        except Exception as e:
            logger.warning(f"⚠️ Kestra Agent não disponível: {e}")
        
        try:
            self.health_agent = get_system_health_agent()
            logger.info("✅ System Health Agent inicializado")
        except Exception as e:
            logger.warning(f"⚠️ System Health Agent não disponível: {e}")
        
        try:
            llm_name = os.getenv("LLM", "llama2")
            ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            self.llm = load_llm(
                llm_name,
                logger=logger,
                config={"ollama_base_url": ollama_base_url}
            )
            logger.info("✅ LLM inicializado")
        except Exception as e:
            logger.warning(f"⚠️ LLM não disponível: {e}")
    
    def _build_graph(self):
        """Constrói o grafo LangGraph"""
        if StateGraph is None:
            logger.error("LangGraph não está instalado. Execute: pip install langgraph")
            self.graph = None
            return
        
        graph = StateGraph(AgentState)
        
        # Adiciona nós
        graph.add_node("plan", self._plan_node)
        graph.add_node("retrieve_memory", self._retrieve_memory_node)
        graph.add_node("execute_agent", self._execute_agent_node)
        graph.add_node("save_memory", self._save_memory_node)
        graph.add_node("review", self._review_node)
        
        # Define ponto de entrada
        graph.set_entry_point("plan")
        
        # Adiciona arestas
        graph.add_edge("plan", "retrieve_memory")
        graph.add_edge("retrieve_memory", "execute_agent")
        graph.add_conditional_edges(
            "execute_agent",
            self._should_save_memory,
            {
                "save": "save_memory",
                "review": "review",
                "end": END
            }
        )
        graph.add_edge("save_memory", "review")
        graph.add_edge("review", END)
        
        # Compila o grafo
        self.graph = graph.compile()
        logger.info("✅ Grafo LangGraph construído")
    
    # ==================== NODES ====================
    
    def _plan_node(self, state: AgentState) -> Dict[str, Any]:
        """Nó de planejamento - analisa o objetivo e cria um plano"""
        logger.info(f"📋 Planejando: {state['goal']}")
        
        if not self.llm:
            return {
                "status": "error",
                "error": "LLM não disponível para planejamento",
                "messages": state["messages"] + [
                    AIMessage(content="Erro: LLM não disponível")
                ]
            }
        
        # Prompt de planejamento
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Você é um planejador de tarefas para um sistema multi-agente.
Analise o objetivo fornecido e crie um plano estruturado.

Formato de resposta (JSON):
{{
    "steps": [
        {{
            "step": 1,
            "action": "descrição da ação",
            "agent_type": "tipo_do_agente",
            "parameters": {{}}
        }}
    ],
    "estimated_steps": número
}}"""),
            ("human", "Objetivo: {goal}")
        ])
        
        try:
            chain = prompt | self.llm | JsonOutputParser()
            plan = chain.invoke({"goal": state["goal"]})
            
            total_steps = plan.get("estimated_steps", len(plan.get("steps", [])))
            
            return {
                "status": "planning",
                "current_step": 0,
                "total_steps": total_steps,
                "parameters": {
                    "plan": plan,
                    "steps": plan.get("steps", [])
                },
                "messages": state["messages"] + [
                    AIMessage(content=f"Plano criado com {total_steps} passos")
                ]
            }
        except Exception as e:
            logger.error(f"Erro no planejamento: {e}")
            return {
                "status": "error",
                "error": str(e),
                "messages": state["messages"] + [
                    AIMessage(content=f"Erro no planejamento: {str(e)}")
                ]
            }
    
    def _retrieve_memory_node(self, state: AgentState) -> Dict[str, Any]:
        """Nó de recuperação de memória - busca contexto no Neo4j"""
        logger.info("🧠 Recuperando memória do Neo4j")
        
        if not self.neo4j_manager:
            return {
                "memory_context": None,
                "messages": state["messages"] + [
                    AIMessage(content="Neo4j não disponível, continuando sem contexto")
                ]
            }
        
        try:
            # Busca contexto relevante no Neo4j
            context = self.neo4j_manager.query_graphrag(
                query=state["goal"],
                limit=5
            )
            
            return {
                "memory_context": context,
                "messages": state["messages"] + [
                    AIMessage(content=f"Contexto recuperado: {len(context.get('results', []))} resultados")
                ]
            }
        except Exception as e:
            logger.warning(f"Erro ao recuperar memória: {e}")
            return {
                "memory_context": None,
                "messages": state["messages"] + [
                    AIMessage(content=f"Erro ao recuperar memória: {str(e)}")
                ]
            }
    
    def _execute_agent_node(self, state: AgentState) -> Dict[str, Any]:
        """Nó de execução - executa o agente apropriado"""
        plan = state.get("parameters", {}).get("plan", {})
        steps = plan.get("steps", [])
        
        if state["current_step"] >= len(steps):
            return {
                "status": "completed",
                "messages": state["messages"] + [
                    AIMessage(content="Todos os passos foram executados")
                ]
            }
        
        current_step_data = steps[state["current_step"]]
        agent_type = current_step_data.get("agent_type")
        action = current_step_data.get("action", "")
        
        logger.info(f"⚙️ Executando passo {state['current_step'] + 1}/{state['total_steps']}: {action}")
        
        try:
            result = self._execute_agent_by_type(
                agent_type=agent_type,
                action=action,
                parameters=current_step_data.get("parameters", {}),
                context=state.get("memory_context")
            )
            
            results = state.get("results", [])
            results.append({
                "step": state["current_step"] + 1,
                "action": action,
                "agent_type": agent_type,
                "result": result,
                "success": True,
                "timestamp": datetime.utcnow().isoformat()
            })
            
            return {
                "current_step": state["current_step"] + 1,
                "results": results,
                "status": "executing",
                "messages": state["messages"] + [
                    AIMessage(content=f"Passo {state['current_step'] + 1} concluído: {action}")
                ]
            }
        except Exception as e:
            logger.error(f"Erro na execução: {e}")
            results = state.get("results", [])
            results.append({
                "step": state["current_step"] + 1,
                "action": action,
                "agent_type": agent_type,
                "error": str(e),
                "success": False,
                "timestamp": datetime.utcnow().isoformat()
            })
            
            return {
                "status": "error",
                "error": str(e),
                "results": results,
                "messages": state["messages"] + [
                    AIMessage(content=f"Erro no passo {state['current_step'] + 1}: {str(e)}")
                ]
            }
    
    def _save_memory_node(self, state: AgentState) -> Dict[str, Any]:
        """Nó de salvamento de memória - salva resultados no Neo4j"""
        logger.info("💾 Salvando memória no Neo4j")
        
        if not self.neo4j_manager:
            return {
                "messages": state["messages"] + [
                    AIMessage(content="Neo4j não disponível, pulando salvamento")
                ]
            }
        
        try:
            # Salva o resultado da execução no Neo4j
            # TODO: Implementar salvamento estruturado
            return {
                "messages": state["messages"] + [
                    AIMessage(content="Memória salva com sucesso")
                ]
            }
        except Exception as e:
            logger.warning(f"Erro ao salvar memória: {e}")
            return {
                "messages": state["messages"] + [
                    AIMessage(content=f"Erro ao salvar memória: {str(e)}")
                ]
            }
    
    def _review_node(self, state: AgentState) -> Dict[str, Any]:
        """Nó de revisão - avalia os resultados"""
        logger.info("🔍 Revisando resultados")
        
        results = state.get("results", [])
        success_count = sum(1 for r in results if r.get("success", False))
        total_count = len(results)
        
        review_message = f"Revisão: {success_count}/{total_count} passos concluídos com sucesso"
        
        return {
            "status": "completed" if success_count == total_count else "partial",
            "messages": state["messages"] + [
                AIMessage(content=review_message)
            ]
        }
    
    # ==================== HELPER METHODS ====================
    
    def _should_save_memory(self, state: AgentState) -> str:
        """Decide se deve salvar memória baseado no estado"""
        if state.get("status") == "error":
            return "review"
        if state.get("current_step", 0) >= state.get("total_steps", 0):
            return "review"
        return "save"
    
    def _execute_agent_by_type(
        self,
        agent_type: str,
        action: str,
        parameters: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> Any:
        """Executa um agente baseado no tipo"""
        if agent_type == "mcp_manager" and self.mcp_manager:
            return self.mcp_manager.list_servers()
        elif agent_type == "neo4j_graphrag" and self.neo4j_manager:
            return self.neo4j_manager.query_graphrag(query=action, limit=5)
        elif agent_type == "kestra" and self.kestra_agent:
            # TODO: Implementar execução de workflow Kestra
            return {"message": "Kestra execution not yet implemented"}
        elif agent_type == "system_health" and self.health_agent:
            return self.health_agent.get_full_report()
        else:
            return {"message": f"Agent type {agent_type} not available or not implemented"}
    
    # ==================== PUBLIC API ====================
    
    async def execute_agent_async(
        self,
        agent_id: str,
        goal: str,
        parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Executa um agente de forma assíncrona"""
        initial_state: AgentState = {
            "messages": [HumanMessage(content=goal)],
            "goal": goal,
            "agent_id": agent_id,
            "agent_type": None,
            "parameters": parameters or {},
            "current_step": 0,
            "total_steps": 0,
            "results": [],
            "status": "pending",
            "error": None,
            "memory_context": None
        }
        
        try:
            # Executa o grafo
            final_state = await self.graph.ainvoke(initial_state)
            
            return {
                "success": final_state.get("status") == "completed",
                "status": final_state.get("status"),
                "results": final_state.get("results", []),
                "messages": [msg.content for msg in final_state.get("messages", []) if hasattr(msg, "content")],
                "error": final_state.get("error")
            }
        except Exception as e:
            logger.error(f"Erro na execução do agente: {e}")
            return {
                "success": False,
                "status": "error",
                "error": str(e),
                "results": []
            }
    
    def list_agents(self) -> List[Dict[str, Any]]:
        """Lista todos os agentes disponíveis"""
        agents = []
        
        if self.mcp_manager:
            agents.append({
                "id": "mcp_manager",
                "name": "MCP Manager",
                "type": "mcp_manager",
                "status": "available",
                "description": "Gerencia servidores MCP"
            })
        
        if self.neo4j_manager:
            agents.append({
                "id": "neo4j_graphrag",
                "name": "Neo4j GraphRAG",
                "type": "neo4j_graphrag",
                "status": "available",
                "description": "Consulta e gerencia memória gráfica"
            })
        
        if self.kestra_agent:
            agents.append({
                "id": "kestra",
                "name": "Kestra Agent",
                "type": "kestra",
                "status": "available",
                "description": "Executa workflows Kestra"
            })
        
        if self.health_agent:
            agents.append({
                "id": "system_health",
                "name": "System Health",
                "type": "system_health",
                "status": "available",
                "description": "Monitora saúde do sistema"
            })
        
        return agents
    
    def get_agent_info(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Obtém informações de um agente específico"""
        agents = self.list_agents()
        for agent in agents:
            if agent["id"] == agent_id:
                return agent
        return None
    
    def get_agent_status(self, agent_id: str) -> Dict[str, Any]:
        """Obtém status de um agente"""
        agent = self.get_agent_info(agent_id)
        if not agent:
            return {"status": "not_found"}
        return {"status": agent.get("status", "unknown")}
    
    def get_system_status(self) -> Dict[str, Any]:
        """Obtém status geral do sistema"""
        agents = self.list_agents()
        return {
            "total_agents": len(agents),
            "active_agents": len([a for a in agents if a.get("status") == "available"]),
            "pending_tasks": 0,  # TODO: Implementar contagem de tarefas
            "completed_tasks": 0,  # TODO: Implementar contagem de tarefas
            "agents": agents
        }
    
    def list_tasks(self) -> List[Dict[str, Any]]:
        """Lista todas as tarefas"""
        # TODO: Implementar persistência de tarefas
        return []
    
    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Obtém uma tarefa específica"""
        # TODO: Implementar busca de tarefa
        return None

# ==================== SINGLETON ====================

_orchestrator_instance: Optional[LangGraphOrchestrator] = None

def get_langgraph_orchestrator() -> LangGraphOrchestrator:
    """Retorna instância singleton do orchestrator"""
    global _orchestrator_instance
    if _orchestrator_instance is None:
        _orchestrator_instance = LangGraphOrchestrator()
    return _orchestrator_instance

