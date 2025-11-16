# 🧪 Guia de Testes - IA-Test

Este guia explica como executar testes no projeto IA-Test usando pytest e TestSprite.

## 📋 Índice

- [Instalação](#instalação)
- [Executando Testes](#executando-testes)
- [TestSprite](#testsprite)
- [Estrutura de Testes](#estrutura-de-testes)
- [Adicionando Novos Testes](#adicionando-novos-testes)

## 🚀 Instalação

### 1. Instalar Dependências

```bash
# Instalar todas as dependências (incluindo testes)
pip install -r config/requirements.txt

# Ou apenas dependências de teste
pip install pytest pytest-cov pytest-asyncio pytest-mock
```

### 2. Configurar Ambiente

```bash
# Execute o script de setup
python scripts/setup_tests.py
```

## 🧪 Executando Testes

### Testes Básicos

```bash
# Todos os testes
pytest

# Testes específicos
pytest tests/test_orchestrator.py
pytest tests/test_agents.py

# Com verbosidade
pytest -v

# Com output detalhado
pytest -vv
```

### Com Cobertura

```bash
# Cobertura no terminal
pytest --cov=src --cov-report=term-missing

# Cobertura em HTML
pytest --cov=src --cov-report=html
# Abra: htmlcov/index.html
```

### Testes Marcados

```bash
# Apenas testes unitários
pytest -m unit

# Apenas testes de integração
pytest -m integration

# Excluir testes lentos
pytest -m "not slow"
```

## 🤖 TestSprite

O TestSprite é uma ferramenta de teste automatizado que usa IA para gerar testes.

### Instalação

1. **Instalar MCP Server:**
```bash
npm install -g @testsprite/mcp-server
```

2. **Configurar no Cursor:**
   - Abra configurações do Cursor
   - Adicione o TestSprite como MCP Server
   - Configure a API key

3. **Obter API Key:**
   - Acesse https://testsprite.com
   - Crie uma conta
   - Gere uma API key
   - Adicione no `.env`:
   ```env
   TESTSPRITE_API_KEY=sua-api-key
   ```

### Uso

1. **Gerar Testes Automaticamente:**
   - Abra um arquivo Python
   - Use o comando "Generate tests" do TestSprite
   - Revise os testes gerados

2. **Executar via TestSprite:**
   - Use "Run tests" no arquivo
   - Ou "Run all tests" para tudo

### Configuração

O projeto possui um arquivo `.testsprite.yml` configurado com:
- Agentes prioritários para teste
- Aplicações para testar
- Configurações de cobertura
- Integrações (Docker, Neo4j)

Consulte `docs/TESTSPRITE_SETUP.md` para mais detalhes.

## 📁 Estrutura de Testes

```
tests/
├── __init__.py
├── conftest.py          # Configuração pytest
├── test_orchestrator.py # Testes do Orchestrator
├── test_agents.py       # Testes dos agentes
├── test_apps.py         # Testes das aplicações
└── README.md            # Documentação dos testes
```

## ✏️ Adicionando Novos Testes

### Manualmente

1. Crie um arquivo `test_*.py` em `tests/`
2. Importe os módulos necessários
3. Escreva os testes usando pytest

**Exemplo:**

```python
import pytest
from src.agents.my_agent import MyAgent

class TestMyAgent:
    def test_initialization(self):
        agent = MyAgent()
        assert agent is not None
    
    def test_method(self):
        agent = MyAgent()
        result = agent.do_something()
        assert result == expected_value
```

### Via TestSprite

1. Abra o arquivo que deseja testar
2. Use o comando "Generate tests"
3. Revise e ajuste os testes gerados

## 🏷️ Marcadores de Teste

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

**Marcadores disponíveis:**
- `@pytest.mark.unit` - Testes unitários
- `@pytest.mark.integration` - Testes de integração
- `@pytest.mark.slow` - Testes que demoram
- `@pytest.mark.requires_db` - Requer banco de dados
- `@pytest.mark.requires_ollama` - Requer Ollama
- `@pytest.mark.requires_docker` - Requer Docker

## 📊 Relatórios

Os relatórios são salvos em `test_reports/`:
- `test_reports/index.html` - Relatório HTML
- `test_reports/coverage.json` - Cobertura JSON

## 🔧 Troubleshooting

### pytest não encontrado

```bash
pip install pytest
```

### Módulos não encontrados

Verifique se o diretório raiz está no `sys.path`:
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
```

### TestSprite não aparece

1. Verifique se o MCP Server está instalado
2. Verifique se a API key está configurada
3. Reinicie o Cursor

## 📚 Recursos

- [Documentação TestSprite](https://docs.testsprite.com)
- [Documentação pytest](https://docs.pytest.org)
- [Guia de Testes Python](https://docs.python.org/3/library/unittest.html)
- [TestSprite Setup Guide](docs/TESTSPRITE_SETUP.md)

## 💡 Dicas

1. **Execute testes frequentemente** durante o desenvolvimento
2. **Use cobertura** para identificar código não testado
3. **Marque testes apropriadamente** para facilitar execução seletiva
4. **Use TestSprite** para gerar testes automaticamente
5. **Mantenha testes simples** e focados

## 🎯 Próximos Passos

1. ✅ Execute `python scripts/setup_tests.py`
2. ✅ Execute `pytest` para verificar se tudo funciona
3. ✅ Configure TestSprite se desejar usar IA para gerar testes
4. ✅ Adicione mais testes conforme necessário

---

**Última atualização:** 2025-01-27

