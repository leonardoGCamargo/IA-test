"""
Configuração pytest para o projeto IA-Test.
"""
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Configurações de teste
import pytest
import os
from unittest.mock import Mock, patch

@pytest.fixture
def mock_env_vars():
    """Mock de variáveis de ambiente para testes."""
    env_vars = {
        "NEO4J_URI": "neo4j://localhost:7687",
        "NEO4J_USERNAME": "neo4j",
        "NEO4J_PASSWORD": "test_password",
        "OLLAMA_BASE_URL": "http://localhost:11434",
        "LLM": "llama2",
        "EMBEDDING_MODEL": "sentence_transformer",
    }
    with patch.dict(os.environ, env_vars):
        yield env_vars

@pytest.fixture
def project_root():
    """Retorna o diretório raiz do projeto."""
    return Path(__file__).parent.parent

