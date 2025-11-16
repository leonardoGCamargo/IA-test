"""
Módulo Orchestrator - Coordenação centralizada de todos os agentes especializados.

Este módulo atua como um Tech Lead, planejando e distribuindo tarefas
entre os agentes especializados do sistema.

CONSOLIDADO: Agora inclui funcionalidades do Master Agent (planejamento inteligente).
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import logging
from pathlib import Path
import json

from src.agents.mcp_manager import MCPManager, get_mcp_manager
from src.agents.mcp_docker_integration import DockerMCPDetector
from src.agents.mcp_obsidian_integration import ObsidianManager
from src.agents.mcp_neo4j_integration import Neo4jGraphRAGManager, get_neo4j_manager
from src.agents.mcp_kestra_integration import KestraAgent, get_kestra_agent
from src.agents.git_integration import GitIntegrationAgent, get_git_agent
from src.agents.db_manager import DatabaseManager, get_db_manager, DatabaseType, DatabaseConfig
from src.agents.system_health_agent import SystemHealthAgent, get_system_health_agent

# Importações para planejamento inteligente (Master Agent)
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage
from langchain_core.output_parsers import StrOutputParser
from src.apps.chains import load_llm

logger = logging.getLogger(__name__)


class AgentType(Enum):
    """Tipos de agentes especializados."""
    MCP_ARCHITECT = "mcp_architect"
    DOCKER_INTEGRATION = "docker_integration"
    OBSIDIAN = "obsidian"
    NEO4J_GRAPHRAG = "neo4j_graphrag"
    STREAMLIT_UI = "streamlit_ui"
    KESTRA = "kestra"
    LANGGRAPH = "langgraph"
    GIT_INTEGRATION = "git_integration"
    DB_MANAGER = "db_manager"
    SYSTEM_HEALTH = "system_health"  # Consolidado: Diagnostic + Helper + Resolution


@dataclass
class Task:
    """Representa uma tarefa a ser executada por um agente."""
    id: str
    agent_type: AgentType
    description: str
    parameters: Dict[str, Any]
    status: str = "pending"  # pending, in_progress, completed, failed
    result: Optional[Any] = None
    error: Optional[str] = None


class Orchestrator:
    """
    Orchestrator - Coordenador central dos agentes especializados.
    
    CONSOLIDADO: Agora inclui funcionalidades de planejamento inteligente do Master Agent.
    
    Responsabilidades:
    - Planejar e distribuir tarefas
    - Planejamento inteligente usando LangChain (do Master Agent)
    - Manter consistência arquitetural
    - Coordenar fluxos entre componentes
    - Gerenciar dependências e docker-compose
    """
    
    def __init__(self):
        """Inicializa o Orchestrator com todos os agentes."""
        self.mcp_manager = get_mcp_manager()
        self.docker_detector = DockerMCPDetector()
        self.obsidian_manager = ObsidianManager()
        
        # Neo4j manager (lazy loading - pode falhar)
        try:
            self.neo4j_manager = get_neo4j_manager()
            self.neo4j_available = True
        except Exception as e:
            logger.warning(f"Neo4j não disponível: {e}")
            self.neo4j_manager = None
            self.neo4j_available = False
        
        # Kestra agent
        try:
            self.kestra_agent = get_kestra_agent()
            self.kestra_available = True
        except Exception as e:
            logger.warning(f"Kestra não disponível: {e}")
            self.kestra_agent = None
            self.kestra_available = False
        
        # System Health Agent (consolidado: Diagnostic + Helper + Resolution)
        try:
            self.health_agent = get_system_health_agent()
            self.health_available = True
        except Exception as e:
            logger.warning(f"System Health Agent não disponível: {e}")
            self.health_agent = None
            self.health_available = False
        
        # Git Integration Agent
        try:
            self.git_agent = get_git_agent()
            self.git_available = True
        except Exception as e:
            logger.warning(f"Git Agent não disponível: {e}")
            self.git_agent = None
            self.git_available = False
        
        # Database Manager
        try:
            self.db_manager = get_db_manager()
            self.db_manager_available = True
        except Exception as e:
            logger.warning(f"Database Manager não disponível: {e}")
            self.db_manager = None
            self.db_manager_available = False
        
        # LLM para planejamento inteligente (do Master Agent)
        try:
            import os
            from dotenv import load_dotenv
            load_dotenv()
            llm_name = os.getenv("LLM", "llama2")
            ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            self.llm = load_llm(
                llm_name,
                logger=logger,
                config={"ollama_base_url": ollama_base_url}
            )
            self.llm_available = True
        except Exception as e:
            logger.warning(f"LLM não disponível para planejamento: {e}")
            self.llm = None
            self.llm_available = False
        
        # Lista de tarefas
        self.tasks: List[Task] = []
        
        logger.info("Orchestrator inicializado (consolidado com Master Agent)")
    
    def create_task(
        self,
        agent_type: AgentType,
        description: str,
        parameters: Dict[str, Any]
    ) -> Task:
        """
        Cria uma nova tarefa para um agente.
        
        Args:
            agent_type: Tipo do agente que executará a tarefa
            description: Descrição da tarefa
            parameters: Parâmetros para a tarefa
            
        Returns:
            Task criada
        """
        task_id = f"{agent_type.value}_{len(self.tasks)}"
        task = Task(
            id=task_id,
            agent_type=agent_type,
            description=description,
            parameters=parameters
        )
        self.tasks.append(task)
        logger.info(f"Tarefa criada: {task_id} - {description}")
        return task
    
    def execute_goal(self, goal: str) -> Dict[str, Any]:
        """
        Executa um objetivo em linguagem natural usando planejamento inteligente.
        
        CONSOLIDADO: Funcionalidade do Master Agent integrada.
        
        Args:
            goal: Objetivo em linguagem natural
            
        Returns:
            Resultado da execução
        """
        if not self.llm_available:
            logger.warning("LLM não disponível, usando planejamento básico")
            return self._execute_goal_basic(goal)
        
        logger.info(f"Executando objetivo com planejamento inteligente: {goal}")
        
        # Fase 1: Planejamento
        plan = self._create_intelligent_plan(goal)
        logger.info(f"Plano criado: {plan}")
        
        # Fase 2: Execução
        results = []
        for step in plan.get("steps", []):
            action = step.get("action", "")
            tool = step.get("tool", "")
            
            try:
                result = self._execute_planned_step(action, tool, step.get("parameters", {}))
                results.append({
                    "step": step.get("step", 0),
                    "action": action,
                    "tool": tool,
                    "result": result,
                    "success": True
                })
            except Exception as e:
                logger.error(f"Erro ao executar passo: {e}")
                results.append({
                    "step": step.get("step", 0),
                    "action": action,
                    "tool": tool,
                    "error": str(e),
                    "success": False
                })
        
        return {
            "goal": goal,
            "plan": plan,
            "results": results,
            "success": all(r.get("success", False) for r in results)
        }
    
    def _create_intelligent_plan(self, goal: str) -> Dict[str, Any]:
        """Cria plano inteligente usando LLM."""
        planning_prompt = ChatPromptTemplate.from_messages([
            ("system", """Você é um planejador especializado em orquestração de agentes.
Dado um objetivo, crie um plano detalhado de como alcançá-lo usando os agentes disponíveis.

Agentes disponíveis:
- MCP_ARCHITECT: Gerenciar servidores MCP
- NEO4J_GRAPHRAG: Grafo de conhecimento
- OBSIDIAN: Gestão de notas
- KESTRA: Orquestração de pipelines
- SYSTEM_HEALTH: Diagnóstico, monitoramento e resolução de problemas
- DB_MANAGER: Gerenciamento de bancos de dados
- GIT_INTEGRATION: Integração com Git

Crie um plano passo a passo em JSON:
{
    "steps": [
        {"step": 1, "action": "descrição", "tool": "agent_type", "parameters": {}},
        ...
    ]
}"""),
            ("human", f"Objetivo: {goal}")
        ])
        
        chain = planning_prompt | self.llm | StrOutputParser()
        plan_text = chain.invoke({"goal": goal})
        
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
        
        return plan
    
    def _execute_planned_step(self, action: str, tool: str, parameters: Dict[str, Any]) -> Any:
        """Executa um passo do plano."""
        # Mapeia tool para AgentType
        agent_type_map = {
            "mcp_architect": AgentType.MCP_ARCHITECT,
            "neo4j_graphrag": AgentType.NEO4J_GRAPHRAG,
            "obsidian": AgentType.OBSIDIAN,
            "kestra": AgentType.KESTRA,
            "system_health": AgentType.SYSTEM_HEALTH,
            "db_manager": AgentType.DB_MANAGER,
            "git_integration": AgentType.GIT_INTEGRATION,
        }
        
        agent_type = agent_type_map.get(tool.lower())
        if not agent_type:
            return {"error": f"Tool não reconhecido: {tool}"}
        
        # Cria e executa tarefa
        task = self.create_task(agent_type, action, parameters)
        return self.execute_task(task)
    
    def _execute_goal_basic(self, goal: str) -> Dict[str, Any]:
        """Executa objetivo sem LLM (planejamento básico)."""
        return {
            "goal": goal,
            "plan": {"steps": [{"step": 1, "action": goal, "tool": "manual"}]},
            "results": [{"step": 1, "action": goal, "result": "Execução básica", "success": True}],
            "success": True
        }
    
    def execute_task(self, task: Task) -> Any:
        """
        Executa uma tarefa delegando para o agente apropriado.
        
        Args:
            task: Tarefa a ser executada
            
        Returns:
            Resultado da execução
        """
        task.status = "in_progress"
        logger.info(f"Executando tarefa: {task.id}")
        
        try:
            if task.agent_type == AgentType.MCP_ARCHITECT:
                result = self._execute_mcp_architect_task(task)
            elif task.agent_type == AgentType.DOCKER_INTEGRATION:
                result = self._execute_docker_task(task)
            elif task.agent_type == AgentType.OBSIDIAN:
                result = self._execute_obsidian_task(task)
            elif task.agent_type == AgentType.NEO4J_GRAPHRAG:
                result = self._execute_neo4j_task(task)
            elif task.agent_type == AgentType.KESTRA:
                result = self._execute_kestra_task(task)
            elif task.agent_type == AgentType.GIT_INTEGRATION:
                result = self._execute_git_task(task)
            elif task.agent_type == AgentType.DB_MANAGER:
                result = self._execute_db_manager_task(task)
            elif task.agent_type == AgentType.SYSTEM_HEALTH:
                result = self._execute_system_health_task(task)
            else:
                raise ValueError(f"Tipo de agente não suportado: {task.agent_type}")
            
            task.status = "completed"
            task.result = result
            logger.info(f"Tarefa concluída: {task.id}")
            return result
            
        except Exception as e:
            task.status = "failed"
            task.error = str(e)
            logger.error(f"Erro ao executar tarefa {task.id}: {e}")
            raise
    
    def _execute_system_health_task(self, task: Task) -> Any:
        """Executa tarefas do System Health Agent (consolidado)."""
        if not self.health_available:
            raise RuntimeError("System Health Agent não está disponível")
        
        action = task.parameters.get("action")
        
        if action == "run_full_health_check":
            report = self.health_agent.run_full_health_check()
            return report.to_dict()
        
        elif action == "diagnose_issues":
            issues = self.health_agent.diagnose_issues()
            return [issue.to_dict() for issue in issues]
        
        elif action == "monitor_agents":
            metrics = self.health_agent.monitor_agents()
            return {
                name: {
                    "name": m.name,
                    "status": m.status.value,
                    "performance_score": m.performance_score,
                    "issues": m.issues,
                    "suggestions": m.suggestions
                }
                for name, m in metrics.items()
            }
        
        elif action == "generate_resolutions":
            issues = task.parameters.get("issues")
            resolutions = self.health_agent.generate_resolutions(issues)
            return [r.to_dict() for r in resolutions]
        
        elif action == "optimize_agent":
            agent_name = task.parameters.get("agent_name")
            return self.health_agent.optimize_agent(agent_name)
        
        elif action == "get_summary":
            return self.health_agent.get_summary()
        
        else:
            raise ValueError(f"Ação não suportada: {action}")
    
    def _execute_mcp_architect_task(self, task: Task) -> Any:
        """Executa tarefas do MCP Architect Agent."""
        action = task.parameters.get("action")
        
        if action == "add_server":
            server_info = task.parameters.get("server_info")
            from src.agents.mcp_manager import MCPServer
            server = MCPServer(**server_info)
            return self.mcp_manager.add_server(server)
        
        elif action == "list_servers":
            return {
                "all": [s.to_dict() for s in self.mcp_manager.list_servers()],
                "enabled": [s.to_dict() for s in self.mcp_manager.list_enabled_servers()]
            }
        
        elif action == "check_health":
            server_name = task.parameters.get("server_name")
            import asyncio
            return asyncio.run(self.mcp_manager.check_server_health(server_name))
        
        else:
            raise ValueError(f"Ação não suportada: {action}")
    
    def _execute_docker_task(self, task: Task) -> Any:
        """Executa tarefas do Docker Integration Agent."""
        action = task.parameters.get("action")
        
        if action == "list_containers":
            return [c.__dict__ for c in self.docker_detector.list_running_containers()]
        
        elif action == "detect_mcp_services":
            return [s.__dict__ for s in self.docker_detector.detect_mcp_services()]
        
        elif action == "get_service_info":
            service_name = task.parameters.get("service_name")
            return self.docker_detector.get_service_info(service_name)
        
        else:
            raise ValueError(f"Ação não suportada: {action}")
    
    def _execute_obsidian_task(self, task: Task) -> Any:
        """Executa tarefas do Obsidian Agent."""
        action = task.parameters.get("action")
        
        if action == "create_mcp_note":
            mcp_name = task.parameters.get("mcp_name")
            mcp_info = task.parameters.get("mcp_info")
            related_notes = task.parameters.get("related_notes", [])
            note_path = self.obsidian_manager.create_mcp_note(mcp_name, mcp_info, related_notes)
            return {"note_path": str(note_path) if note_path else None}
        
        elif action == "create_rag_note":
            rag_name = task.parameters.get("rag_name")
            rag_info = task.parameters.get("rag_info")
            related_mcps = task.parameters.get("related_mcps", [])
            note_path = self.obsidian_manager.create_rag_note(rag_name, rag_info, related_mcps)
            return {"note_path": str(note_path) if note_path else None}
        
        elif action == "import_to_neo4j":
            if not self.neo4j_available:
                raise RuntimeError("Neo4j não está disponível")
            vault_path = Path(task.parameters.get("vault_path"))
            imported = self.neo4j_manager.import_obsidian_vault(vault_path)
            return {"imported_count": imported}
        
        else:
            raise ValueError(f"Ação não suportada: {action}")
    
    def _execute_neo4j_task(self, task: Task) -> Any:
        """Executa tarefas do Neo4j GraphRAG Agent."""
        if not self.neo4j_available:
            raise RuntimeError("Neo4j não está disponível")
        
        action = task.parameters.get("action")
        
        if action == "create_mcp_node":
            mcp_info = task.parameters.get("mcp_info")
            return self.neo4j_manager.create_mcp_node(mcp_info)
        
        elif action == "query_graphrag":
            question = task.parameters.get("question")
            return {"answer": self.neo4j_manager.query_graphrag(question)}
        
        elif action == "get_statistics":
            return self.neo4j_manager.get_graph_statistics()
        
        elif action == "visualize_graph":
            node_types = task.parameters.get("node_types")
            limit = task.parameters.get("limit", 50)
            return self.neo4j_manager.get_graph_visualization_data(node_types, limit)
        
        else:
            raise ValueError(f"Ação não suportada: {action}")
    
    def _execute_kestra_task(self, task: Task) -> Any:
        """Executa tarefas do Kestra Agent."""
        if not self.kestra_available:
            raise RuntimeError("Kestra não está disponível")
        
        action = task.parameters.get("action")
        
        if action == "create_sync_workflow":
            return self.kestra_agent.create_sync_mcp_workflow().to_dict()
        
        elif action == "create_import_obsidian_workflow":
            vault_path = task.parameters.get("vault_path")
            return self.kestra_agent.create_import_obsidian_workflow(vault_path).to_dict()
        
        elif action == "create_health_check_workflow":
            return self.kestra_agent.create_health_check_workflow().to_dict()
        
        elif action == "list_workflows":
            return [w.to_dict() for w in self.kestra_agent.list_workflows()]
        
        elif action == "generate_default_workflows":
            workflows = self.kestra_agent.generate_default_workflows()
            return [w.to_dict() for w in workflows]
        
        else:
            raise ValueError(f"Ação não suportada: {action}")
    
    def _execute_git_task(self, task: Task) -> Any:
        """Executa tarefas do Git Integration Agent."""
        if not self.git_available:
            raise RuntimeError("Git Agent não está disponível")
        
        action = task.parameters.get("action")
        return self.git_agent.execute_action(action, task.parameters)
    
    def _execute_db_manager_task(self, task: Task) -> Any:
        """Executa tarefas do Database Manager."""
        if not self.db_manager_available:
            raise RuntimeError("Database Manager não está disponível")
        
        action = task.parameters.get("action")
        
        if action == "add_database":
            db_type = DatabaseType(task.parameters.get("db_type"))
            config = DatabaseConfig(
                db_type=db_type,
                name=task.parameters.get("name"),
                uri=task.parameters.get("uri"),
                host=task.parameters.get("host"),
                port=task.parameters.get("port"),
                database=task.parameters.get("database"),
                username=task.parameters.get("username"),
                password=task.parameters.get("password"),
                api_key=task.parameters.get("api_key"),
                project_id=task.parameters.get("project_id"),
                connection_string=task.parameters.get("connection_string"),
                enabled=task.parameters.get("enabled", True),
                metadata=task.parameters.get("metadata", {})
            )
            return self.db_manager.add_database(config)
        
        elif action == "list_databases":
            return self.db_manager.list_databases()
        
        elif action == "connect":
            name = task.parameters.get("name")
            return self.db_manager.connect(name)
        
        elif action == "execute_query":
            name = task.parameters.get("name")
            query = task.parameters.get("query")
            parameters = task.parameters.get("parameters")
            result = self.db_manager.execute_query(name, query, parameters)
            return {
                "success": result.success,
                "data": result.data,
                "error": result.error,
                "rows_affected": result.rows_affected,
                "execution_time": result.execution_time
            }
        
        else:
            raise ValueError(f"Ação não suportada: {action}")
    
    def sync_mcp_to_neo4j(self, server_name: Optional[str] = None) -> Dict[str, Any]:
        """Sincroniza MCPs para Neo4j."""
        if not self.neo4j_available:
            return {"success": False, "error": "Neo4j não disponível"}
        
        servers = self.mcp_manager.list_servers() if not server_name else [
            s for s in self.mcp_manager.list_servers() if s.name == server_name
        ]
        
        synced = 0
        for server in servers:
            try:
                mcp_info = {
                    "name": server.name,
                    "command": server.command,
                    "args": server.args,
                    "enabled": server.enabled,
                    "description": server.description
                }
                self.neo4j_manager.create_mcp_node(mcp_info)
                synced += 1
            except Exception as e:
                logger.error(f"Erro ao sincronizar {server.name}: {e}")
        
        return {"success": True, "synced_count": synced, "total": len(servers)}
    
    def sync_mcp_to_obsidian(self, server_name: Optional[str] = None) -> Dict[str, Any]:
        """Sincroniza MCPs para Obsidian."""
        servers = self.mcp_manager.list_servers() if not server_name else [
            s for s in self.mcp_manager.list_servers() if s.name == server_name
        ]
        
        created = 0
        for server in servers:
            try:
                mcp_info = {
                    "name": server.name,
                    "command": server.command,
                    "args": server.args,
                    "enabled": server.enabled,
                    "description": server.description
                }
                self.obsidian_manager.create_mcp_note(server.name, mcp_info)
                created += 1
            except Exception as e:
                logger.error(f"Erro ao criar nota para {server.name}: {e}")
        
        return {"success": True, "created_count": created, "total": len(servers)}
    
    def get_system_status(self) -> Dict[str, Any]:
        """Retorna status completo do sistema."""
        status = {
            "orchestrator": {
                "status": "active",
                "total_tasks": len(self.tasks),
                "completed_tasks": len([t for t in self.tasks if t.status == "completed"]),
                "failed_tasks": len([t for t in self.tasks if t.status == "failed"])
            },
            "mcp_manager": {
                "status": "active",
                "servers_count": len(self.mcp_manager.list_servers()),
                "enabled_count": len(self.mcp_manager.list_enabled_servers())
            },
            "neo4j": {
                "available": self.neo4j_available,
                "status": "active" if self.neo4j_available else "unavailable"
            },
            "kestra": {
                "available": self.kestra_available,
                "status": "active" if self.kestra_available else "unavailable"
            },
            "health_agent": {
                "available": self.health_available,
                "status": "active" if self.health_available else "unavailable"
            },
            "git_agent": {
                "available": self.git_available,
                "status": "active" if self.git_available else "unavailable"
            },
            "db_manager": {
                "available": self.db_manager_available,
                "status": "active" if self.db_manager_available else "unavailable"
            },
            "llm": {
                "available": self.llm_available,
                "status": "active" if self.llm_available else "unavailable"
            }
        }
        
        # Adiciona status de saúde se disponível
        if self.health_available:
            try:
                health_summary = self.health_agent.get_summary()
                status["system_health"] = health_summary
            except Exception as e:
                logger.warning(f"Erro ao obter status de saúde: {e}")
        
        return status


# Instância global
_orchestrator_instance: Optional[Orchestrator] = None


def get_orchestrator() -> Orchestrator:
    """Retorna a instância global do Orchestrator."""
    global _orchestrator_instance
    if _orchestrator_instance is None:
        _orchestrator_instance = Orchestrator()
    return _orchestrator_instance
