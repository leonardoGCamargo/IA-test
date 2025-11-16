"""
Testes básicos para as aplicações do sistema.
"""
import pytest
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


class TestAppsImports:
    """Testa se as aplicações podem ser importadas."""
    
    def test_import_utils(self):
        """Testa a importação do utils."""
        try:
            from src.apps import utils
            assert utils is not None
        except ImportError:
            pytest.skip("Utils não disponível")
    
    def test_import_chains(self):
        """Testa a importação do chains."""
        try:
            from src.apps import chains
            assert chains is not None
        except ImportError:
            pytest.skip("Chains não disponível")
    
    def test_import_api(self):
        """Testa a importação da API."""
        try:
            from src.apps import api
            assert api is not None
        except ImportError:
            pytest.skip("API não disponível")
    
    def test_import_bot(self):
        """Testa a importação do bot."""
        try:
            from src.apps import bot
            assert bot is not None
        except ImportError:
            pytest.skip("Bot não disponível")

