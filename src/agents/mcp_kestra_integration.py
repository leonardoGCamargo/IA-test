"""
Integração com Kestra para orquestração de pipelines automatizados.

Este módulo implementa o Kestra Agent responsável por:
- Criar e gerenciar workflows Kestra
- Agendar tarefas automatizadas
- Orquestrar fluxos MCP → Neo4j → Obsidian
- Automação de importações e sincronizações
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class KestraWorkflow:
    """Representa um workflow Kestra."""
    id: str
    name: str
    namespace: str = "mcp"
    description: Optional[str] = None
    tasks: List[Dict[str, Any]] = None
    triggers: List[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict:
        """Converte workflow para dicionário."""
        return {
            "id": self.id,
            "namespace": self.namespace,
            "description": self.description,
            "tasks": self.tasks or [],
            "triggers": self.triggers or []
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'KestraWorkflow':
        """Cria workflow a partir de dicionário."""
        return cls(
            id=data["id"],
            name=data.get("name", data["id"]),
            namespace=data.get("namespace", "mcp"),
            description=data.get("description"),
            tasks=data.get("tasks", []),
            triggers=data.get("triggers", [])
        )


class KestraAgent:
    """
    Agente Kestra para orquestração de pipelines.
    
    Responsabilidades:
    - Criar workflows Kestra
    - Agendar execuções
    - Gerenciar pipelines de sincronização
    - Automatizar fluxos MCP → Neo4j → Obsidian
    """
    
    def __init__(self, kestra_url: Optional[str] = None, kestra_user: Optional[str] = None, kestra_password: Optional[str] = None):
        """
        Inicializa o agente Kestra.
        
        Args:
            kestra_url: URL do Kestra (ex: http://localhost:8080)
            kestra_user: Usuário do Kestra
            kestra_password: Senha do Kestra
        """
        self.kestra_url = kestra_url or "http://localhost:8080"
        self.kestra_user = kestra_user
        self.kestra_password = kestra_password
        self.workflows_dir = Path("kestra_workflows")
        self.workflows_dir.mkdir(exist_ok=True)
        
        # Lista de workflows gerenciados
        self.workflows: Dict[str, KestraWorkflow] = {}
        self.load_workflows()
        
        logger.info(f"KestraAgent inicializado (URL: {self.kestra_url})")
    
    def load_workflows(self) -> None:
        """Carrega workflows do diretório."""
        if not self.workflows_dir.exists():
            return
        
        for workflow_file in self.workflows_dir.glob("*.yaml"):
            try:
                # TODO: Implementar parser YAML quando Kestra estiver disponível
                workflow_id = workflow_file.stem
                logger.debug(f"Workflow encontrado: {workflow_id}")
            except Exception as e:
                logger.error(f"Erro ao carregar workflow {workflow_file}: {e}")
    
    def create_sync_mcp_workflow(self) -> KestraWorkflow:
        """
        Cria workflow para sincronizar MCPs entre componentes.
        
        Returns:
            Workflow criado
        """
        workflow = KestraWorkflow(
            id="sync-mcp-full",
            name="Sync MCP Full Pipeline",
            description="Sincroniza MCPs entre MCP Manager, Neo4j e Obsidian",
            tasks=[
                {
                    "id": "sync-mcp-to-neo4j",
                    "type": "io.kestra.core.tasks.scripts.Python",
                    "docker": {
                        "image": "python:3.11"
                    },
                    "script": """
from src.agents.mcp_manager import get_mcp_manager
from src.agents.mcp_neo4j_integration import get_neo4j_manager

mcp_manager = get_mcp_manager()
neo4j_manager = get_neo4j_manager()

servers = mcp_manager.list_servers()
for server in servers:
    mcp_info = {
        "name": server.name,
        "id": server.name,
        "command": server.command,
        "args": server.args,
        "description": server.description or "",
        "enabled": server.enabled
    }
    neo4j_manager.create_mcp_node(mcp_info)
"""
                },
                {
                    "id": "sync-mcp-to-obsidian",
                    "type": "io.kestra.core.tasks.scripts.Python",
                    "docker": {
                        "image": "python:3.11"
                    },
                    "script": """
from src.agents.mcp_manager import get_mcp_manager
from src.agents.mcp_obsidian_integration import ObsidianManager

mcp_manager = get_mcp_manager()
obsidian_manager = ObsidianManager()

servers = mcp_manager.list_servers()
for server in servers:
    mcp_info = {
        "command": server.command,
        "args": server.args,
        "description": server.description,
        "enabled": server.enabled
    }
    obsidian_manager.create_mcp_note(server.name, mcp_info)
"""
                }
            ],
            triggers=[
                {
                    "id": "schedule",
                    "type": "io.kestra.core.models.triggers.types.Schedule",
                    "cron": "0 */6 * * *"  # A cada 6 horas
                }
            ]
        )
        
        self.workflows[workflow.id] = workflow
        self.save_workflow(workflow)
        logger.info(f"Workflow criado: {workflow.id}")
        return workflow
    
    def create_import_obsidian_workflow(self, vault_path: str) -> KestraWorkflow:
        """
        Cria workflow para importar notas Obsidian para Neo4j.
        
        Args:
            vault_path: Caminho do vault Obsidian
            
        Returns:
            Workflow criado
        """
        workflow = KestraWorkflow(
            id="import-obsidian-vault",
            name="Import Obsidian Vault to Neo4j",
            description=f"Importa notas do vault Obsidian ({vault_path}) para Neo4j",
            tasks=[
                {
                    "id": "import-vault",
                    "type": "io.kestra.core.tasks.scripts.Python",
                    "docker": {
                        "image": "python:3.11"
                    },
                    "script": f"""
from pathlib import Path
from src.agents.mcp_neo4j_integration import get_neo4j_manager

neo4j_manager = get_neo4j_manager()
vault_path = Path("{vault_path}")
imported = neo4j_manager.import_obsidian_vault(vault_path)
print(f"{{imported}} notas importadas")
"""
                }
            ],
            triggers=[
                {
                    "id": "schedule",
                    "type": "io.kestra.core.models.triggers.types.Schedule",
                    "cron": "0 2 * * *"  # Diariamente às 2h
                }
            ]
        )
        
        self.workflows[workflow.id] = workflow
        self.save_workflow(workflow)
        logger.info(f"Workflow criado: {workflow.id}")
        return workflow
    
    def create_health_check_workflow(self) -> KestraWorkflow:
        """
        Cria workflow para verificar saúde dos serviços MCP.
        
        Returns:
            Workflow criado
        """
        workflow = KestraWorkflow(
            id="mcp-health-check",
            name="MCP Health Check",
            description="Verifica saúde de todos os servidores MCP",
            tasks=[
                {
                    "id": "check-mcp-health",
                    "type": "io.kestra.core.tasks.scripts.Python",
                    "docker": {
                        "image": "python:3.11"
                    },
                    "script": """
import asyncio
from src.agents.mcp_manager import get_mcp_manager

async def check_all():
    mcp_manager = get_mcp_manager()
    servers = mcp_manager.list_enabled_servers()
    
    results = {}
    for server in servers:
        health = await mcp_manager.check_server_health(server.name)
        results[server.name] = health
    
    print(json.dumps(results, indent=2))
    return results

asyncio.run(check_all())
"""
                },
                {
                    "id": "notify-on-failure",
                    "type": "io.kestra.core.tasks.notifications.Notification",
                    "condition": "{{ failed }}",
                    "channels": ["email", "slack"]  # Configurar conforme necessário
                }
            ],
            triggers=[
                {
                    "id": "schedule",
                    "type": "io.kestra.core.models.triggers.types.Schedule",
                    "cron": "*/30 * * * *"  # A cada 30 minutos
                }
            ]
        )
        
        self.workflows[workflow.id] = workflow
        self.save_workflow(workflow)
        logger.info(f"Workflow criado: {workflow.id}")
        return workflow
    
    def save_workflow(self, workflow: KestraWorkflow) -> bool:
        """
        Salva workflow em arquivo YAML.
        
        Args:
            workflow: Workflow a salvar
            
        Returns:
            True se salvo com sucesso
        """
        try:
            # Converte para formato Kestra YAML
            yaml_content = self._workflow_to_yaml(workflow)
            
            workflow_file = self.workflows_dir / f"{workflow.id}.yaml"
            with open(workflow_file, 'w', encoding='utf-8') as f:
                f.write(yaml_content)
            
            logger.info(f"Workflow salvo: {workflow_file}")
            return True
        except Exception as e:
            logger.error(f"Erro ao salvar workflow: {e}")
            return False
    
    def _workflow_to_yaml(self, workflow: KestraWorkflow) -> str:
        """
        Converte workflow para formato YAML do Kestra.
        
        Args:
            workflow: Workflow a converter
            
        Returns:
            String YAML
        """
        yaml_lines = [
            f"id: {workflow.id}",
            f"namespace: {workflow.namespace}",
            ""
        ]
        
        if workflow.description:
            yaml_lines.append(f"description: {workflow.description}")
            yaml_lines.append("")
        
        # Tasks
        if workflow.tasks:
            yaml_lines.append("tasks:")
            for task in workflow.tasks:
                yaml_lines.append(f"  - id: {task['id']}")
                yaml_lines.append(f"    type: {task['type']}")
                
                # Adiciona propriedades específicas da task
                for key, value in task.items():
                    if key not in ['id', 'type']:
                        if isinstance(value, dict):
                            yaml_lines.append(f"    {key}:")
                            for k, v in value.items():
                                if isinstance(v, dict):
                                    yaml_lines.append(f"      {k}:")
                                    for k2, v2 in v.items():
                                        yaml_lines.append(f"        {k2}: {v2}")
                                else:
                                    yaml_lines.append(f"      {k}: {v}")
                        elif isinstance(value, list):
                            yaml_lines.append(f"    {key}:")
                            for item in value:
                                yaml_lines.append(f"      - {item}")
                        else:
                            yaml_lines.append(f"    {key}: {value}")
                yaml_lines.append("")
        
        # Triggers
        if workflow.triggers:
            yaml_lines.append("triggers:")
            for trigger in workflow.triggers:
                yaml_lines.append(f"  - id: {trigger['id']}")
                yaml_lines.append(f"    type: {trigger['type']}")
                
                for key, value in trigger.items():
                    if key not in ['id', 'type']:
                        yaml_lines.append(f"    {key}: {value}")
                yaml_lines.append("")
        
        return "\n".join(yaml_lines)
    
    def list_workflows(self) -> List[KestraWorkflow]:
        """Lista todos os workflows gerenciados."""
        return list(self.workflows.values())
    
    def get_workflow(self, workflow_id: str) -> Optional[KestraWorkflow]:
        """Retorna um workflow pelo ID."""
        return self.workflows.get(workflow_id)
    
    def delete_workflow(self, workflow_id: str) -> bool:
        """
        Remove um workflow.
        
        Args:
            workflow_id: ID do workflow
            
        Returns:
            True se removido com sucesso
        """
        if workflow_id in self.workflows:
            del self.workflows[workflow_id]
        
        workflow_file = self.workflows_dir / f"{workflow_id}.yaml"
        if workflow_file.exists():
            workflow_file.unlink()
        
        logger.info(f"Workflow removido: {workflow_id}")
        return True
    
    def generate_default_workflows(self) -> List[KestraWorkflow]:
        """
        Gera workflows padrão do sistema.
        
        Returns:
            Lista de workflows criados
        """
        workflows = []
        
        # Workflow de sincronização MCP
        workflows.append(self.create_sync_mcp_workflow())
        
        # Workflow de health check
        workflows.append(self.create_health_check_workflow())
        
        # Workflow de import Obsidian (se vault configurado)
        # Será criado dinamicamente quando vault for configurado
        
        logger.info(f"{len(workflows)} workflows padrão criados")
        return workflows


# Instância global do agente Kestra
_kestra_agent_instance: Optional[KestraAgent] = None


def get_kestra_agent() -> KestraAgent:
    """Retorna a instância global do agente Kestra."""
    global _kestra_agent_instance
    if _kestra_agent_instance is None:
        _kestra_agent_instance = KestraAgent()
    return _kestra_agent_instance

