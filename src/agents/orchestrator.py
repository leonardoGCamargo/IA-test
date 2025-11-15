"""
Módulo Orchestrator - Coordenação centralizada de todos os agentes especializados.

Este módulo atua como um Tech Lead, planejando e distribuindo tarefas
entre os agentes especializados do sistema.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import logging
from pathlib import Path

from src.agents.mcp_manager import MCPManager, get_mcp_manager
from src.agents.mcp_docker_integration import DockerMCPDetector
from src.agents.mcp_obsidian_integration import ObsidianManager
from src.agents.mcp_neo4j_integration import Neo4jGraphRAGManager, get_neo4j_manager
from src.agents.mcp_kestra_integration import KestraAgent, get_kestra_agent
from src.agents.kestra_langchain_master import KestraLangChainMaster, get_master_agent
from src.agents.agent_helper_system import AgentHelperSystem, get_helper_system, get_monitor_helper, get_optimizer_helper
from src.agents.git_integration import GitIntegrationAgent, get_git_agent

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
    KESTRA_LANGCHAIN_MASTER = "kestra_langchain_master"
    AGENT_HELPER = "agent_helper"
    GIT_INTEGRATION = "git_integration"


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
    
    Responsabilidades:
    - Planejar e distribuir tarefas
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
        
        # Kestra & LangChain Master
        try:
            self.master_agent = get_master_agent()
            self.master_available = True
        except Exception as e:
            logger.warning(f"Master Agent não disponível: {e}")
            self.master_agent = None
            self.master_available = False
        
        # Agent Helper System
        try:
            self.helper_system = get_helper_system()
            self.helper_available = True
        except Exception as e:
            logger.warning(f"Helper System não disponível: {e}")
            self.helper_system = None
            self.helper_available = False
        
        # Git Integration Agent
        try:
            self.git_agent = get_git_agent()
            self.git_available = True
        except Exception as e:
            logger.warning(f"Git Agent não disponível: {e}")
            self.git_agent = None
            self.git_available = False
        
        # Lista de tarefas
        self.tasks: List[Task] = []
        
        logger.info("Orchestrator inicializado")
    
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
            elif task.agent_type == AgentType.KESTRA_LANGCHAIN_MASTER:
                result = self._execute_master_task(task)
            elif task.agent_type == AgentType.AGENT_HELPER:
                result = self._execute_helper_task(task)
            elif task.agent_type == AgentType.GIT_INTEGRATION:
                result = self._execute_git_task(task)
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
    
    def _execute_mcp_architect_task(self, task: Task) -> Any:
        """Executa tarefas do MCP Architect Agent."""
        action = task.parameters.get("action")
        
        if action == "add_server":
            server_info = task.parameters.get("server_info")
            from mcp_manager import MCPServer
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
    
    def _execute_master_task(self, task: Task) -> Any:
        """Executa tarefas do Kestra & LangChain Master Agent."""
        if not self.master_available:
            raise RuntimeError("Master Agent não está disponível")
        
        action = task.parameters.get("action")
        
        if action == "execute_goal":
            goal = task.parameters.get("goal")
            return self.master_agent.execute_goal(goal)
        
        elif action == "create_intelligent_workflow":
            description = task.parameters.get("description")
            workflow = self.master_agent.create_intelligent_workflow(description)
            return workflow.to_dict()
        
        else:
            raise ValueError(f"Ação não suportada: {action}")
    
    def _execute_helper_task(self, task: Task) -> Any:
        """Executa tarefas do Agent Helper System."""
        if not self.helper_available:
            raise RuntimeError("Helper System não está disponível")
        
        action = task.parameters.get("action")
        
        if action == "monitor_agent":
            agent_name = task.parameters.get("agent_name")
            monitor = get_monitor_helper()
            metrics = monitor.monitor_agent(agent_name)
            return {
                "name": metrics.name,
                "status": metrics.status.value,
                "performance_score": metrics.performance_score,
                "issues": metrics.issues
            }
        
        elif action == "optimize_agent":
            agent_name = task.parameters.get("agent_name")
            optimizer = get_optimizer_helper()
            return optimizer.optimize_agent(agent_name)
        
        elif action == "get_full_report":
            return self.helper_system.get_full_report()
        
        else:
            raise ValueError(f"Ação não suportada: {action}")
    
    def _execute_git_task(self, task: Task) -> Any:
        """Executa tarefas do Git Integration Agent."""
        if not self.git_available:
            raise RuntimeError("Git Agent não está disponível")
        
        action = task.parameters.get("action")
        return self.git_agent.execute_action(action, task.parameters)
    
    def sync_mcp_to_neo4j(self, server_name: Optional[str] = None) -> Dict[str, int]:
        """
        Sincroniza servidores MCP para o Neo4j.
        
        Args:
            server_name: Nome do servidor específico (None para todos)
            
        Returns:
            Estatísticas de sincronização
        """
        if not self.neo4j_available:
            logger.warning("Neo4j não disponível, pulando sincronização")
            return {"synced": 0, "failed": 0}
        
        servers = [self.mcp_manager.get_server(server_name)] if server_name else self.mcp_manager.list_servers()
        
        synced = 0
        failed = 0
        
        for server in servers:
            if server:
                mcp_info = {
                    "name": server.name,
                    "id": server.name,
                    "command": server.command,
                    "args": server.args,
                    "description": server.description or "",
                    "enabled": server.enabled
                }
                
                try:
                    if self.neo4j_manager.create_mcp_node(mcp_info):
                        synced += 1
                    else:
                        failed += 1
                except Exception as e:
                    logger.error(f"Erro ao sincronizar servidor {server.name}: {e}")
                    failed += 1
        
        logger.info(f"Sincronização MCP→Neo4j: {synced} sucessos, {failed} falhas")
        return {"synced": synced, "failed": failed}
    
    def sync_mcp_to_obsidian(self, server_name: Optional[str] = None) -> Dict[str, int]:
        """
        Sincroniza servidores MCP para o Obsidian.
        
        Args:
            server_name: Nome do servidor específico (None para todos)
            
        Returns:
            Estatísticas de sincronização
        """
        servers = [self.mcp_manager.get_server(server_name)] if server_name else self.mcp_manager.list_servers()
        
        created = 0
        failed = 0
        
        for server in servers:
            if server:
                mcp_info = {
                    "command": server.command,
                    "args": server.args,
                    "description": server.description,
                    "enabled": server.enabled
                }
                
                try:
                    note_path = self.obsidian_manager.create_mcp_note(server.name, mcp_info)
                    if note_path:
                        created += 1
                    else:
                        failed += 1
                except Exception as e:
                    logger.error(f"Erro ao criar nota Obsidian para {server.name}: {e}")
                    failed += 1
        
        logger.info(f"Sincronização MCP→Obsidian: {created} notas criadas, {failed} falhas")
        return {"created": created, "failed": failed}
    
    def create_full_sync_pipeline(self) -> List[Task]:
        """
        Cria um pipeline completo de sincronização entre todos os componentes.
        
        Returns:
            Lista de tarefas criadas
        """
        pipeline = []
        
        # 1. Sincronizar MCPs para Neo4j
        task1 = self.create_task(
            AgentType.NEO4J_GRAPHRAG,
            "Sincronizar MCPs para Neo4j",
            {"action": "sync_mcps"}
        )
        pipeline.append(task1)
        
        # 2. Sincronizar MCPs para Obsidian
        task2 = self.create_task(
            AgentType.OBSIDIAN,
            "Sincronizar MCPs para Obsidian",
            {"action": "sync_mcps"}
        )
        pipeline.append(task2)
        
        # 3. Importar notas Obsidian para Neo4j
        if self.obsidian_manager.vault_path:
            task3 = self.create_task(
                AgentType.OBSIDIAN,
                "Importar notas Obsidian para Neo4j",
                {
                    "action": "import_to_neo4j",
                    "vault_path": str(self.obsidian_manager.vault_path)
                }
            )
            pipeline.append(task3)
        
        return pipeline
    
    def get_system_status(self) -> Dict[str, Any]:
        """
        Obtém status geral do sistema.
        
        Returns:
            Dicionário com status de todos os componentes
        """
        status = {
            "mcp_manager": {
                "available": True,
                "servers_count": len(self.mcp_manager.list_servers()),
                "enabled_count": len(self.mcp_manager.list_enabled_servers())
            },
            "docker": {
                "available": True,
                "containers_count": len(self.docker_detector.list_running_containers()),
                "mcp_services_count": len(self.docker_detector.detect_mcp_services())
            },
            "obsidian": {
                "available": self.obsidian_manager.vault_path is not None,
                "vault_path": str(self.obsidian_manager.vault_path) if self.obsidian_manager.vault_path else None
            },
            "neo4j": {
                "available": self.neo4j_available,
                "statistics": self.neo4j_manager.get_graph_statistics() if self.neo4j_available else None
            },
            "kestra": {
                "available": self.kestra_available,
                "workflows_count": len(self.kestra_agent.list_workflows()) if self.kestra_available else 0
            },
            "kestra_langchain_master": {
                "available": self.master_available
            },
            "agent_helper_system": {
                "available": self.helper_available
            },
            "git_integration": {
                "available": self.git_available,
                "status": self.git_agent.get_status().__dict__ if self.git_available else None
            },
            "tasks": {
                "total": len(self.tasks),
                "pending": len([t for t in self.tasks if t.status == "pending"]),
                "in_progress": len([t for t in self.tasks if t.status == "in_progress"]),
                "completed": len([t for t in self.tasks if t.status == "completed"]),
                "failed": len([t for t in self.tasks if t.status == "failed"])
            }
        }
        
        return status


# Instância global do Orchestrator
_orchestrator_instance: Optional[Orchestrator] = None


def get_orchestrator() -> Orchestrator:
    """Retorna a instância global do Orchestrator."""
    global _orchestrator_instance
    if _orchestrator_instance is None:
        _orchestrator_instance = Orchestrator()
    return _orchestrator_instance

