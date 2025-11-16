# Testes do Projeto IA-Test

Este diretório contém os testes do projeto IA-Test.

## Estrutura

```
tests/
├── __init__.py
├── conftest.py          # Configuração pytest
├── test_orchestrator.py # Testes do Orchestrator
├── test_agents.py       # Testes dos agentes
├── test_apps.py         # Testes das aplicações
└── README.md            # Este arquivo
```

## Executando os Testes

### Com pytest

```bash
# Todos os testes
pytest

# Testes específicos
pytest tests/test_orchestrator.py

# Com cobertura
pytest --cov=src --cov-report=html

# Testes marcados
pytest -m unit
pytest -m integration
```

### Com TestSprite

O TestSprite pode ser configurado via MCP Server. Consulte a documentação em:
- https://docs.testsprite.com

Para usar o TestSprite:

1. Instale o MCP Server do TestSprite
2. Configure a API key no arquivo `.testsprite.yml`
3. Execute os testes via IDE (Cursor/VS Code)

## Marcadores de Teste

- `@pytest.mark.unit` - Testes unitários
- `@pytest.mark.integration` - Testes de integração
- `@pytest.mark.slow` - Testes que demoram
- `@pytest.mark.requires_db` - Requer banco de dados
- `@pytest.mark.requires_ollama` - Requer Ollama
- `@pytest.mark.requires_docker` - Requer Docker

## Adicionando Novos Testes

1. Crie um arquivo `test_*.py` no diretório `tests/`
2. Importe os módulos necessários
3. Use fixtures do `conftest.py` quando apropriado
4. Adicione marcadores apropriados

Exemplo:

```python
import pytest
from src.agents.my_agent import MyAgent

class TestMyAgent:
    def test_initialization(self):
        agent = MyAgent()
        assert agent is not None
```

## Cobertura de Testes

Para verificar a cobertura:

```bash
pytest --cov=src --cov-report=term-missing
```

## Integração com TestSprite

O TestSprite pode gerar testes automaticamente. Para ativar:

1. Configure o MCP Server do TestSprite no Cursor
2. Use o comando "Generate tests" no arquivo que deseja testar
3. O TestSprite gerará testes baseados no código

