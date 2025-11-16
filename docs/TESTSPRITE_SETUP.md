# Configuração TestSprite para IA-Test

## Visão Geral

O TestSprite é uma ferramenta de teste automatizado que usa IA para gerar, executar e gerenciar testes. Este guia explica como configurar e usar o TestSprite no projeto IA-Test.

## Instalação

### 1. Instalar TestSprite MCP Server

O TestSprite funciona como um MCP Server que se integra ao Cursor/VS Code.

**Opção 1: Via npm (recomendado)**

```bash
npm install -g @testsprite/mcp-server
```

**Opção 2: Via pip (se disponível)**

```bash
pip install testsprite-mcp
```

### 2. Configurar no Cursor

1. Abra as configurações do Cursor
2. Procure por "MCP Servers"
3. Adicione o TestSprite:

```json
{
  "mcpServers": {
    "testsprite": {
      "command": "npx",
      "args": ["-y", "@testsprite/mcp-server"],
      "env": {
        "TESTSPRITE_API_KEY": "sua-api-key-aqui"
      }
    }
  }
}
```

### 3. Obter API Key

1. Acesse https://testsprite.com
2. Crie uma conta ou faça login
3. Gere uma API key no painel
4. Adicione a key no arquivo `.env`:

```env
TESTSPRITE_API_KEY=sua-api-key-aqui
```

## Configuração do Projeto

O projeto já possui um arquivo `.testsprite.yml` configurado com:

- **Agentes prioritários**: Orchestrator, DB Manager, MCP Manager
- **Aplicações**: API, Bot, Utils
- **Framework de teste**: pytest
- **Cobertura mínima**: 70%

## Uso

### Gerar Testes Automaticamente

1. Abra um arquivo Python (ex: `src/agents/orchestrator.py`)
2. Use o comando do TestSprite: "Generate tests for this file"
3. O TestSprite gerará testes baseados no código

### Executar Testes

**Via TestSprite (no Cursor):**
- Use o comando "Run tests" no arquivo
- Ou "Run all tests" para executar tudo

**Via pytest (terminal):**
```bash
# Todos os testes
pytest

# Testes específicos
pytest tests/test_orchestrator.py

# Com cobertura
pytest --cov=src --cov-report=html
```

### Ver Relatórios

Os relatórios são salvos em `test_reports/`:
- `test_reports/index.html` - Relatório HTML
- `test_reports/coverage.json` - Cobertura JSON

## Estrutura de Testes

```
tests/
├── __init__.py
├── conftest.py          # Configuração pytest
├── test_orchestrator.py # Testes do Orchestrator
├── test_agents.py       # Testes dos agentes
└── test_apps.py         # Testes das aplicações
```

## Testes Existentes

### Testes do Orchestrator
- Inicialização
- Criação de tarefas
- Status do sistema

### Testes dos Agentes
- Importação de módulos
- Disponibilidade de classes

### Testes das Aplicações
- Importação de módulos
- Disponibilidade de funções

## Adicionando Novos Testes

### Manualmente

1. Crie um arquivo `test_*.py` em `tests/`
2. Importe os módulos necessários
3. Escreva os testes usando pytest

Exemplo:

```python
import pytest
from src.agents.my_agent import MyAgent

class TestMyAgent:
    def test_initialization(self):
        agent = MyAgent()
        assert agent is not None
```

### Via TestSprite

1. Abra o arquivo que deseja testar
2. Use o comando "Generate tests"
3. Revise e ajuste os testes gerados

## Marcadores de Teste

Use marcadores para categorizar testes:

```python
@pytest.mark.unit
def test_simple_function():
    pass

@pytest.mark.integration
@pytest.mark.requires_db
def test_database_operation():
    pass
```

Marcadores disponíveis:
- `@pytest.mark.unit` - Testes unitários
- `@pytest.mark.integration` - Testes de integração
- `@pytest.mark.slow` - Testes que demoram
- `@pytest.mark.requires_db` - Requer banco de dados
- `@pytest.mark.requires_ollama` - Requer Ollama
- `@pytest.mark.requires_docker` - Requer Docker

## Integração Contínua

O TestSprite pode ser integrado ao CI/CD:

```yaml
# .github/workflows/tests.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - run: pip install -r config/requirements.txt
      - run: pytest --cov=src
```

## Troubleshooting

### TestSprite não aparece no Cursor

1. Verifique se o MCP Server está instalado
2. Verifique se a API key está configurada
3. Reinicie o Cursor

### Testes falhando

1. Verifique se as dependências estão instaladas
2. Verifique se os serviços necessários estão rodando (Docker, Neo4j, etc.)
3. Execute `pytest -v` para ver detalhes

### Cobertura baixa

1. Use `pytest --cov=src --cov-report=term-missing` para ver o que falta
2. Adicione testes para os módulos não cobertos
3. Use o TestSprite para gerar testes automaticamente

## Recursos

- [Documentação TestSprite](https://docs.testsprite.com)
- [Documentação pytest](https://docs.pytest.org)
- [Guia de Testes Python](https://docs.python.org/3/library/unittest.html)

## Suporte

Para problemas com o TestSprite:
- Consulte a documentação oficial
- Abra uma issue no repositório do TestSprite
- Entre em contato com o suporte

Para problemas com os testes do projeto:
- Verifique os logs em `test_reports/`
- Execute `pytest -v` para mais detalhes
- Consulte a documentação do pytest

