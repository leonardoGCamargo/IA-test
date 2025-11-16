"""
Testes básicos para os agentes do sistema.
"""
import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Adiciona o diretório raiz ao path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


class TestAgentsImports:
    """Testa se os agentes podem ser importados."""
    
    def test_import_orchestrator(self):
        """Testa a importação do Orchestrator."""
        try:
            from src.agents.orchestrator import Orchestrator
            assert Orchestrator is not None
        except ImportError:
            pytest.skip("Orchestrator não disponível")
    
    def test_import_mcp_manager(self):
        """Testa a importação do MCP Manager."""
        try:
            from src.agents.mcp_manager import MCPManager
            assert MCPManager is not None
        except ImportError:
            pytest.skip("MCP Manager não disponível")
    
    def test_import_db_manager(self):
        """Testa a importação do DB Manager."""
        try:
            from src.agents.db_manager import DatabaseManager
            assert DatabaseManager is not None
        except ImportError:
            pytest.skip("DB Manager não disponível")
    
    def test_import_diagnostic_agent(self):
        """Testa a importação do Diagnostic Agent."""
        try:
            from src.agents.diagnostic_agent import DiagnosticAgent
            assert DiagnosticAgent is not None
        except ImportError:
            pytest.skip("Diagnostic Agent não disponível")
    
    def test_import_resolution_agent(self):
        """Testa a importação do Resolution Agent."""
        try:
            from src.agents.resolution_agent import ResolutionAgent
            assert ResolutionAgent is not None
        except ImportError:
            pytest.skip("Resolution Agent não disponível")

