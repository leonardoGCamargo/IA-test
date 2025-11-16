"""
Agentes Principais do Sistema MCP

CONSOLIDADO: Agentes foram otimizados e consolidados.
"""

from .orchestrator import get_orchestrator, AgentType
from .mcp_manager import get_mcp_manager
from .mcp_neo4j_integration import get_neo4j_manager
from .mcp_kestra_integration import get_kestra_agent
from .git_integration import get_git_agent
from .db_manager import get_db_manager, DatabaseType, DatabaseConfig
from .system_health_agent import get_system_health_agent, SystemHealthReport

# Mantém imports para compatibilidade (deprecated)
from .diagnostic_agent import DiagnosticIssue, IssueSeverity, IssueCategory
from .resolution_agent import Resolution
from .agent_helper_system import AgentMetrics, AgentStatus

__all__ = [
    "get_orchestrator",
    "AgentType",
    "get_mcp_manager",
    "get_neo4j_manager",
    "get_kestra_agent",
    "get_git_agent",
    "get_db_manager",
    "DatabaseType",
    "DatabaseConfig",
    "get_system_health_agent",
    "SystemHealthReport",
    # Compatibilidade (deprecated)
    "DiagnosticIssue",
    "IssueSeverity",
    "IssueCategory",
    "Resolution",
    "AgentMetrics",
    "AgentStatus",
]

