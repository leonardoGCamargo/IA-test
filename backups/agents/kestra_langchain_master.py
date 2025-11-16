"""
Kestra & LangChain Master - Agente Mestre que combina LangChain Agents com Kestra Workflows.

Este módulo implementa um agente mestre que:
- Usa LangChain Agents para planejar e raciocinar
- Cria e executa workflows Kestra dinamicamente
- Coordena múltiplos agentes especializados
- Otimiza e ajusta workflows baseado em feedback
"""

from typing import Dict, List, Optional, Any, TypedDict, Annotated
from dataclasses import dataclass, asdict
from datetime import datetime
import json
import logging
from pathlib import Path

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.runnables import RunnablePassthrough
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain.tools import StructuredTool
from typing_extensions import TypedDict

from src.apps.chains import load_llm, load_embedding_model
from src.agents.orchestrator import get_orchestrator, AgentType
from src.agents.mcp_kestra_integration import get_kestra_agent, KestraWorkflow
from src.agents.mcp_manager import get_mcp_manager
from src.agents.mcp_neo4j_integration import get_neo4j_manager

logger = logging.getLogger(__name__)


class MasterState(TypedDict):
    """Estado do agente mestre."""
    messages: Annotated[List[BaseMessage], lambda x, y: x + y]
    goal: str
    plan: str
    workflows: List[Dict[str, Any]]
    results: List[Dict[str, Any]]
    feedback: str
    iteration: int


class KestraLangChainMaster:
    """
    Agente Mestre que combina LangChain Agents com Kestra Workflows.
    
    Este agente:
    1. Recebe objetivos em linguagem natural
    2. Usa LangChain para planejar workflows
    3. Cria workflows Kestra dinamicamente
    4. Executa e monitora workflows
    5. Otimiza baseado em feedback
    """
    
    def __init__(
        self,
        llm_name: Optional[str] = None,
        embedding_model_name: Optional[str] = None,
        max_iterations: int = 5
    ):
        """
        Inicializa o Master Agent.
        
        Args:
            llm_name: Nome do modelo LLM
            embedding_model_name: Nome do modelo de embedding
            max_iterations: Número máximo de iterações de refinamento
        """
        import os
        from dotenv import load_dotenv
        load_dotenv()
        
        self.llm_name = llm_name or os.getenv("LLM", "llama2")
        self.embedding_model_name = embedding_model_name or os.getenv("EMBEDDING_MODEL", "sentence_transformer")
        self.ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.max_iterations = max_iterations
        
        # Carrega modelos
        try:
            self.llm = load_llm(
                self.llm_name,
                logger=logger,
                config={"ollama_base_url": self.ollama_base_url}
            )
            self.embeddings, _ = load_embedding_model(
                self.embedding_model_name,
                logger=logger,
                config={"ollama_base_url": self.ollama_base_url}
            )
            logger.info(f"Modelos carregados: LLM={self.llm_name}, Embedding={self.embedding_model_name}")
        except Exception as e:
            logger.error(f"Erro ao carregar modelos: {e}")
            raise
        
        # Inicializa componentes
        self.orchestrator = get_orchestrator()
        self.kestra_agent = get_kestra_agent()
        self.mcp_manager = get_mcp_manager()
        
        try:
            self.neo4j_manager = get_neo4j_manager()
            self.neo4j_available = True
        except Exception as e:
            logger.warning(f"Neo4j não disponível: {e}")
            self.neo4j_manager = None
            self.neo4j_available = False
        
        # Cria ferramentas para o agente LangChain
        self.tools = self._create_tools()
        
        # Constrói o grafo do agente
        self.agent_graph = self._build_agent_graph()
        
        logger.info("KestraLangChainMaster inicializado")
    
    def _create_tools(self) -> List[StructuredTool]:
        """Cria ferramentas para o agente LangChain."""
        
        def create_sync_workflow(description: str) -> str:
            """Cria workflow de sincronização MCP."""
            workflow = self.kestra_agent.create_sync_mcp_workflow()
            return f"Workflow criado: {workflow.id}"
        
        def create_health_check_workflow(interval_minutes: int = 30) -> str:
            """Cria workflow de health check."""
            workflow = self.kestra_agent.create_health_check_workflow()
            # Atualiza intervalo se necessário
            if workflow.triggers:
                workflow.triggers[0]["cron"] = f"*/{interval_minutes} * * * *"
                self.kestra_agent.save_workflow(workflow)
            return f"Workflow de health check criado: {workflow.id}"
        
        def sync_mcp_to_neo4j(server_name: Optional[str] = None) -> str:
            """Sincroniza MCPs para Neo4j."""
            result = self.orchestrator.sync_mcp_to_neo4j(server_name)
            return json.dumps(result)
        
        def sync_mcp_to_obsidian(server_name: Optional[str] = None) -> str:
            """Sincroniza MCPs para Obsidian."""
            result = self.orchestrator.sync_mcp_to_obsidian(server_name)
            return json.dumps(result)
        
        def get_system_status() -> str:
            """Obtém status do sistema."""
            status = self.orchestrator.get_system_status()
            return json.dumps(status, indent=2)
        
        def create_custom_workflow(workflow_id: str, tasks: List[Dict], schedule: Optional[str] = None) -> str:
            """Cria workflow customizado."""
            workflow = KestraWorkflow(
                id=workflow_id,
                name=f"Custom Workflow: {workflow_id}",
                description="Workflow criado dinamicamente pelo Master Agent",
                tasks=tasks,
                triggers=[{"id": "schedule", "type": "io.kestra.core.models.triggers.types.Schedule", "cron": schedule}] if schedule else []
            )
            self.kestra_agent.workflows[workflow_id] = workflow
            self.kestra_agent.save_workflow(workflow)
            return f"Workflow customizado criado: {workflow_id}"
        
        tools = [
            StructuredTool.from_function(create_sync_workflow),
            StructuredTool.from_function(create_health_check_workflow),
            StructuredTool.from_function(sync_mcp_to_neo4j),
            StructuredTool.from_function(sync_mcp_to_obsidian),
            StructuredTool.from_function(get_system_status),
            StructuredTool.from_function(create_custom_workflow),
        ]
        
        return tools
    
    def _build_agent_graph(self) -> StateGraph:
        """Constrói o grafo do agente usando LangGraph."""
        
        def planner(state: MasterState) -> MasterState:
            """Fase de planejamento - usa LLM para criar plano."""
            goal = state["goal"]
            messages = state["messages"]
            
            planning_prompt = ChatPromptTemplate.from_messages([
                ("system", """Você é um planejador especializado em orquestração de workflows.
Dado um objetivo, crie um plano detalhado de como alcançá-lo usando workflows Kestra.

Componentes disponíveis:
- MCP Manager: Gerenciar servidores MCP
- Neo4j GraphRAG: Grafo de conhecimento
- Obsidian: Gestão de notas
- Kestra: Orquestração de pipelines

Crie um plano passo a passo em JSON:
{
    "steps": [
        {"step": 1, "action": "descrição", "tool": "ferramenta"},
        ...
    ]
}"""),
                ("human", f"Objetivo: {goal}\n\nMensagens anteriores: {messages[-5:] if len(messages) > 5 else messages}")
            ])
            
            chain = planning_prompt | self.llm | StrOutputParser()
            plan_text = chain.invoke({"goal": goal, "messages": messages})
            
            # Tenta extrair JSON do plano
            try:
                import re
                json_match = re.search(r'\{.*\}', plan_text, re.DOTALL)
                if json_match:
                    plan = json.loads(json_match.group())
                else:
                    plan = {"steps": [{"step": 1, "action": plan_text, "tool": "manual"}]}
            except:
                plan = {"steps": [{"step": 1, "action": plan_text, "tool": "manual"}]}
            
            return {
                **state,
                "plan": json.dumps(plan, indent=2),
                "messages": state["messages"] + [AIMessage(content=f"Plano criado:\n{plan_text}")]
            }
        
        def executor(state: MasterState) -> MasterState:
            """Fase de execução - executa o plano."""
            plan_text = state.get("plan", "{}")
            
            try:
                plan = json.loads(plan_text)
                steps = plan.get("steps", [])
                
                results = []
                for step in steps:
                    action = step.get("action", "")
                    tool_name = step.get("tool", "")
                    
                    # Executa ação usando ferramenta apropriada
                    result = {"step": step.get("step", 0), "action": action, "result": "Executado"}
                    
                    # Mapeia ferramentas para ações
                    if "sync" in action.lower() and "neo4j" in action.lower():
                        result["result"] = self.orchestrator.sync_mcp_to_neo4j()
                    elif "sync" in action.lower() and "obsidian" in action.lower():
                        result["result"] = self.orchestrator.sync_mcp_to_obsidian()
                    elif "health" in action.lower() or "check" in action.lower():
                        workflow = self.kestra_agent.create_health_check_workflow()
                        result["result"] = f"Workflow criado: {workflow.id}"
                    elif "workflow" in action.lower() and "sync" in action.lower():
                        workflow = self.kestra_agent.create_sync_mcp_workflow()
                        result["result"] = f"Workflow criado: {workflow.id}"
                    else:
                        result["result"] = f"Ação genérica: {action}"
                    
                    results.append(result)
                
                return {
                    **state,
                    "results": results,
                    "messages": state["messages"] + [AIMessage(content=f"Execução concluída: {len(results)} passos")]
                }
            except Exception as e:
                logger.error(f"Erro na execução: {e}")
                return {
                    **state,
                    "results": [{"error": str(e)}],
                    "messages": state["messages"] + [AIMessage(content=f"Erro na execução: {e}")]
                }
        
        def reviewer(state: MasterState) -> MasterState:
            """Fase de revisão - avalia resultados."""
            goal = state["goal"]
            results = state.get("results", [])
            iteration = state.get("iteration", 0)
            
            if iteration >= self.max_iterations:
                return {**state, "messages": state["messages"] + [AIMessage(content="Máximo de iterações atingido")]}
            
            review_prompt = ChatPromptTemplate.from_messages([
                ("system", """Você é um revisor especializado. Avalie se o objetivo foi alcançado.
Se não foi, forneça feedback para melhorias."""),
                ("human", f"Objetivo: {goal}\n\nResultados: {json.dumps(results, indent=2)}\n\nO objetivo foi alcançado? Se não, o que precisa ser melhorado?")
            ])
            
            chain = review_prompt | self.llm | StrOutputParser()
            feedback = chain.invoke({"goal": goal, "results": results})
            
            # Decide se continua ou termina
            if "sim" in feedback.lower() or "sim" in feedback.lower()[:100] or "yes" in feedback.lower()[:100]:
                should_continue = False
            else:
                should_continue = True
            
            return {
                **state,
                "feedback": feedback,
                "iteration": iteration + 1,
                "messages": state["messages"] + [AIMessage(content=f"Revisão: {feedback}")]
            }
        
        # Constrói grafo
        workflow = StateGraph(MasterState)
        
        workflow.add_node("planner", planner)
        workflow.add_node("executor", executor)
        workflow.add_node("reviewer", reviewer)
        
        workflow.set_entry_point("planner")
        workflow.add_edge("planner", "executor")
        workflow.add_edge("executor", "reviewer")
        workflow.add_conditional_edges(
            "reviewer",
            lambda state: "continue" if state.get("iteration", 0) < self.max_iterations and "não" in state.get("feedback", "").lower()[:100] else "end",
            {
                "continue": "planner",
                "end": END
            }
        )
        
        return workflow.compile()
    
    def execute_goal(self, goal: str, initial_messages: Optional[List[BaseMessage]] = None) -> Dict[str, Any]:
        """
        Executa um objetivo usando o agente mestre.
        
        Args:
            goal: Objetivo em linguagem natural
            initial_messages: Mensagens iniciais (opcional)
            
        Returns:
            Resultado da execução
        """
        logger.info(f"Executando objetivo: {goal}")
        
        initial_state = {
            "messages": initial_messages or [HumanMessage(content=goal)],
            "goal": goal,
            "plan": "",
            "workflows": [],
            "results": [],
            "feedback": "",
            "iteration": 0
        }
        
        try:
            result = self.agent_graph.invoke(initial_state)
            
            return {
                "goal": goal,
                "plan": result.get("plan", ""),
                "results": result.get("results", []),
                "feedback": result.get("feedback", ""),
                "iterations": result.get("iteration", 0),
                "messages": [msg.content for msg in result.get("messages", [])]
            }
        except Exception as e:
            logger.error(f"Erro ao executar objetivo: {e}")
            return {
                "goal": goal,
                "error": str(e),
                "results": []
            }
    
    def create_intelligent_workflow(self, description: str) -> KestraWorkflow:
        """
        Cria workflow inteligente baseado em descrição em linguagem natural.
        
        Args:
            description: Descrição do workflow em linguagem natural
            
        Returns:
            Workflow criado
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Você é um especialista em criar workflows Kestra.
Dado uma descrição, crie uma estrutura de workflow em JSON.

Formato:
{
    "id": "workflow-id",
    "tasks": [
        {"id": "task-1", "type": "io.kestra.core.tasks.scripts.Python", "script": "código python"},
        ...
    ],
    "schedule": "cron expression (opcional)"
}"""),
            ("human", f"Crie um workflow para: {description}")
        ])
        
        chain = prompt | self.llm | StrOutputParser()
        workflow_json = chain.invoke({"description": description})
        
        try:
            import re
            json_match = re.search(r'\{.*\}', workflow_json, re.DOTALL)
            if json_match:
                workflow_data = json.loads(json_match.group())
                
                workflow = KestraWorkflow(
                    id=workflow_data.get("id", f"workflow-{datetime.now().timestamp()}"),
                    name=description[:50],
                    description=description,
                    tasks=workflow_data.get("tasks", []),
                    triggers=[{"id": "schedule", "type": "io.kestra.core.models.triggers.types.Schedule", "cron": workflow_data.get("schedule")}] if workflow_data.get("schedule") else []
                )
                
                self.kestra_agent.workflows[workflow.id] = workflow
                self.kestra_agent.save_workflow(workflow)
                
                logger.info(f"Workflow inteligente criado: {workflow.id}")
                return workflow
            else:
                raise ValueError("Não foi possível extrair JSON da resposta")
        except Exception as e:
            logger.error(f"Erro ao criar workflow inteligente: {e}")
            raise


# Instância global do Master Agent
_master_agent_instance: Optional[KestraLangChainMaster] = None


def get_master_agent() -> KestraLangChainMaster:
    """Retorna a instância global do Master Agent."""
    global _master_agent_instance
    if _master_agent_instance is None:
        _master_agent_instance = KestraLangChainMaster()
    return _master_agent_instance

