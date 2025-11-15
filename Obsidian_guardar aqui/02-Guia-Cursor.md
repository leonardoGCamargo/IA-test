# 🖥️ Guia de Uso do Cursor

> **Como usar o Cursor com o sistema de agentes**

## 🎯 O que é o Cursor

O Cursor é um editor de código baseado em VSCode que integra IA para ajudar na programação. Ele permite conversar com agentes diretamente no editor.

## 🤖 Usando Agentes no Cursor

### 1. Abrir Chat com Agente

**Atalho:** `Ctrl+L` (Windows) / `Cmd+L` (Mac)

No chat, você pode:
- Fazer perguntas sobre o código
- Pedir para criar/modificar código
- Solicitar explicações
- Pedir ajuda com debug

### 2. Comandos Úteis

#### Pedir para Criar um Agente
```
Crie um novo agente que [descrição da funcionalidade]
```

#### Pedir para Modificar Código
```
Modifique o arquivo [nome] para [descrição da mudança]
```

#### Pedir Explicação
```
Explique como funciona o [arquivo/função]
```

#### Pedir para Integrar
```
Integre o [componente] com o Orchestrator
```

### 3. Context-Aware

O Cursor entende o contexto:
- Arquivo atual aberto
- Seleção de código
- Estrutura do projeto
- Histórico de conversas

**Dica:** Selecione código antes de fazer perguntas para dar contexto.

## 🔧 Configurações Importantes

### 1. Workspace Settings

Crie `.vscode/settings.json`:

```json
{
  "python.defaultInterpreterPath": "./venv/bin/python",
  "python.analysis.extraPaths": [
    "./",
    "./venv/lib/python3.11/site-packages"
  ],
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true,
    "**/node_modules": true,
    "**/.git": false
  },
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": false,
  "python.linting.flake8Enabled": true
}
```

### 2. Extensões Recomendadas

- **Python** - Suporte a Python
- **Docker** - Gerenciamento de containers
- **YAML** - Suporte a YAML (docker-compose)
- **Markdown Preview Enhanced** - Preview de Markdown
- **GitLens** - Visualização Git avançada

## 🎯 Trabalhando com o Sistema de Agentes

### 1. Explorar Estrutura

Use o Cursor para:
```bash
# No terminal integrado
tree -L 2 -I '__pycache__|*.pyc|node_modules'

# Ou use o explorador de arquivos
Ctrl+Shift+E
```

### 2. Navegar entre Arquivos

- **Atalho:** `Ctrl+P` (Windows) / `Cmd+P` (Mac)
- **Buscar símbolo:** `Ctrl+Shift+O` (Windows) / `Cmd+Shift+O` (Mac)
- **Buscar em todos os arquivos:** `Ctrl+Shift+F` (Windows) / `Cmd+Shift+F` (Mac)

### 3. Refatorar Código

Selecione código e use:
- `F2` - Renomear símbolo
- `Ctrl+.` (Windows) / `Cmd+.` (Mac) - Quick fix
- `Shift+Alt+F` (Windows) / `Shift+Option+F` (Mac) - Formatar

## 🤖 Exemplos de Comandos no Cursor

### Criar Novo Agente
```
Sistema: Cursor, preciso criar um novo agente que monitora performance do sistema.

Cursor pode ajudar criando:
- Estrutura básica do agente
- Integração com Orchestrator
- Documentação
- Testes
```

### Modificar Agente Existente
```
Sistema: Modifique o Helper System para adicionar métricas de tempo de resposta.

Cursor vai:
- Identificar arquivo correto (agent_helper_system.py)
- Adicionar nova funcionalidade
- Atualizar imports se necessário
- Manter compatibilidade com código existente
```

### Debug
```
Sistema: O Orchestrator não está executando tarefas do Master Agent.

Cursor vai:
- Analisar código do Orchestrator
- Verificar integração com Master Agent
- Sugerir correções
- Explicar o problema
```

## 🔗 Integração com Agentes do Sistema

### 1. Usar Orchestrator via Terminal

No terminal integrado do Cursor:

```bash
# Iniciar Python interativo
python

# Importar Orchestrator
>>> from orchestrator import get_orchestrator
>>> orchestrator = get_orchestrator()
>>> status = orchestrator.get_system_status()
>>> print(status)
```

### 2. Executar Scripts

```bash
# Executar demonstração
python master_demo.py

# Executar testes
pytest tests/

# Executar agente específico
python -m mcp_manager
```

### 3. Debug com Cursor

- Coloque breakpoints: Clique na margem esquerda
- **F5** - Iniciar debug
- **F10** - Step over
- **F11** - Step into
- **Shift+F11** - Step out

## 📝 Snippets Úteis

### Snippet para Novo Agente

Crie em `.vscode/agent.code-snippets`:

```json
{
  "New Agent": {
    "prefix": "newagent",
    "body": [
      "\"\"\"",
      "Agente: ${1:Nome do Agente}",
      "Descrição: ${2:Descrição do agente}",
      "\"\"\"",
      "",
      "from typing import Dict, List, Optional, Any",
      "import logging",
      "",
      "logger = logging.getLogger(__name__)",
      "",
      "",
      "class ${3:AgentName}:",
      "    \"\"\"${4:Descrição da classe}\"\"\"",
      "    ",
      "    def __init__(self):",
      "        \"\"\"Inicializa o agente.\"\"\"",
      "        logger.info(\"${3:AgentName} inicializado\")",
      "",
      "",
      "# Instância global",
      "_agent_instance: Optional[${3:AgentName}] = None",
      "",
      "",
      "def get_${5:agent_name}() -> ${3:AgentName}:",
      "    \"\"\"Retorna instância global do agente.\"\"\"",
      "    global _agent_instance",
      "    if _agent_instance is None:",
      "        _agent_instance = ${3:AgentName}()",
      "    return _agent_instance"
    ],
    "description": "Cria estrutura básica de um novo agente"
  }
}
```

## 🎨 Atalhos Úteis

| Ação | Windows | Mac |
|------|---------|-----|
| Chat com IA | `Ctrl+L` | `Cmd+L` |
| Buscar arquivo | `Ctrl+P` | `Cmd+P` |
| Buscar símbolo | `Ctrl+Shift+O` | `Cmd+Shift+O` |
| Buscar em todos | `Ctrl+Shift+F` | `Cmd+Shift+F` |
| Terminal | `Ctrl+`` ` | `Cmd+`` ` |
| Explorador | `Ctrl+Shift+E` | `Cmd+Shift+E` |
| Comando | `Ctrl+Shift+P` | `Cmd+Shift+P` |
| Formatar | `Shift+Alt+F` | `Shift+Option+F` |

## 🔗 Integração com Docker

### Executar Comandos Docker

No terminal do Cursor:

```bash
# Ver status dos containers
docker compose ps

# Ver logs
docker compose logs -f mcp-manager

# Executar comando em container
docker compose exec mcp-manager python -c "from orchestrator import get_orchestrator; print(get_orchestrator().get_system_status())"
```

### Debug Docker

1. Anexar debugger ao container
2. Usar port forwarding
3. Ver logs em tempo real

## 📚 Links Úteis

- [[00-MAPA-DE-AGENTES|Voltar ao Mapa]]
- [[01-Guia-Obsidian|Guia do Obsidian]]
- [[03-Manual-Sistema-Agentes|Manual do Sistema]]
- [[04-Como-Criar-Agentes|Como Criar Agentes]]

## 🏷️ Tags

#cursor #guia #ide #desenvolvimento #tooling

---

**Dica:** O Cursor aprende com seu código! Use-o frequentemente para melhorar resultados.

