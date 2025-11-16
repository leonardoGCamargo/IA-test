# 🗺️ Guia de Navegação - MCP Orchestrator

> **Guia completo para encontrar seus arquivos Python e agentes**

## 📂 Estrutura Completa do Projeto

```
projeto/
│
├── 📁 src/                          # 👈 TODO SEU CÓDIGO PYTHON ESTÁ AQUI
│   ├── 📁 agents/                   # 🤖 TODOS OS AGENTES AQUI
│   │   ├── orchestrator.py         # ⭐ Coordenador principal
│   │   ├── mcp_manager.py          # Gerenciador MCP
│   │   ├── mcp_manager_ui.py       # UI do MCP Manager
│   │   ├── mcp_docker_integration.py      # Integração Docker
│   │   ├── mcp_neo4j_integration.py       # Integração Neo4j
│   │   ├── mcp_obsidian_integration.py    # Integração Obsidian
│   │   ├── mcp_kestra_integration.py      # Integração Kestra
│   │   ├── kestra_langchain_master.py     # Master Agent
│   │   ├── agent_helper_system.py         # Helper System
│   │   └── git_integration.py             # 🔥 NOVO: Agente Git/GitHub
│   │
│   └── 📁 apps/                     # 💻 Aplicações existentes
│       ├── bot.py                   # Support Bot
│       ├── loader.py                # Stack Overflow Loader
│       ├── pdf_bot.py               # PDF Bot
│       ├── api.py                   # API
│       ├── chains.py                # LangChain chains
│       └── utils.py                 # Utilitários
│
├── 📁 scripts/                      # 🔧 Scripts utilitários
│   ├── git_sync_simple.py          # Sincronizar Git/GitHub
│   ├── git_sync.py                 # Sincronização completa
│   ├── master_demo.py              # Demo do Master Agent
│   ├── sync_obsidian_docs.py       # Sincronizar Obsidian
│   ├── verificar_integracao_obsidian.py
│   └── rename_project.py           # Renomear projeto
│
├── 📁 docs/                         # 📚 Documentação técnica
│   ├── ARCHITECTURE.md             # Arquitetura
│   ├── ENGINEERING_GUIDE.md        # Guia para engenheiros
│   ├── ARCHITECTURE_DEEP_DIVE.md   # Análise profunda
│   ├── GIT_INTEGRATION_README.md   # 🔥 NOVO: Doc Git Agent
│   └── ...
│
├── 📁 Obsidian_guardar aqui/        # 📝 Documentação Obsidian
│   ├── 00-MAPA-DE-AGENTES.md
│   ├── Agentes/
│   └── ...
│
├── 📁 docker/                       # 🐳 Dockerfiles
│   ├── api.Dockerfile
│   ├── bot.Dockerfile
│   └── ...
│
├── 📁 examples/                     # 💡 Exemplos
│   └── example_docker_agent_usage.py
│
├── 📁 config/                       # ⚙️ Configurações
│   ├── docker-compose.yml          # Docker Compose
│   ├── env.example                 # Exemplo de variáveis
│   └── requirements.txt            # Dependências Python
│
└── 📁 front-end/                    # 🌐 Frontend (Svelte)
    └── src/
```

## 🔍 Onde Está Cada Tipo de Arquivo?

### 🤖 Agentes (Agents)

**Localização:** `src/agents/`

**Principais arquivos:**
- `orchestrator.py` - Coordenador central ⭐
- `mcp_manager.py` - Gerenciador de servidores MCP
- `git_integration.py` - Agente Git/GitHub 🔥 NOVO
- `kestra_langchain_master.py` - Master Agent
- `agent_helper_system.py` - Helper System

**Como importar:**
```python
from src.agents import get_orchestrator, AgentType, get_git_agent
# ou
from src.agents.orchestrator import get_orchestrator
from src.agents.git_integration import get_git_agent
```

### 💻 Aplicações (Apps)

**Localização:** `src/apps/`

**Arquivos:**
- `bot.py` - Support Bot
- `loader.py` - Stack Overflow Loader
- `pdf_bot.py` - PDF Bot
- `api.py` - API
- `chains.py` - LangChain chains
- `utils.py` - Utilitários

**Como importar:**
```python
from src.apps.bot import Bot
from src.apps.chains import get_chain
from src.apps.utils import helper_function
```

### 🔧 Scripts Utilitários

**Localização:** `scripts/`

**Principais scripts:**
- `git_sync_simple.py` - Sincronizar com GitHub (usar este)
- `master_demo.py` - Demo do Master Agent
- `sync_obsidian_docs.py` - Sincronizar documentação

**Como executar:**
```bash
python scripts/git_sync_simple.py
python scripts/master_demo.py
```

### 📚 Documentação

**Técnica:** `docs/`
**Obsidian:** `Obsidian_guardar aqui/`

**Principais documentos:**
- `README.md` (raiz) - README principal
- `docs/ENGINEERING_GUIDE.md` - Guia para engenheiros
- `Obsidian_guardar aqui/00-MAPA-DE-AGENTES.md` - Mapa de agentes

### ⚙️ Configurações

**Localização:** `config/`

**Arquivos:**
- `docker-compose.yml` - Orquestração Docker
- `env.example` - Variáveis de ambiente (copiar para `.env`)
- `requirements.txt` - Dependências Python

**Como usar:**
```bash
cd config
cp env.example .env
# Edite o .env com suas configurações
pip install -r requirements.txt
```

## 🔗 Como Importar Corretamente

### ✅ Forma Correta (Após Reorganização)

```python
# Agentes
from src.agents import get_orchestrator, AgentType
from src.agents.mcp_manager import get_mcp_manager
from src.agents.git_integration import get_git_agent

# Apps
from src.apps.bot import Bot
from src.apps.chains import get_chain

# Exemplos de uso
orchestrator = get_orchestrator()
git_agent = get_git_agent()
```

### ❌ Forma Antiga (NÃO USAR MAIS)

```python
# ERRADO - Não funciona mais
from mcp_manager import get_mcp_manager
from bot import Bot
from orchestrator import get_orchestrator
```

## 📋 Arquivos Temporários Removidos

Estes arquivos eram temporários e foram removidos/desnecessários:
- ❌ `fix_imports.py` - Script temporário (já executado)
- ❌ `organizar_projeto.py` - Script temporário (já executado)
- ⚠️ `readme.md` - Duplicado (usar `README.md` em maiúsculas)

**Nota:** Se você ainda vê esses arquivos na raiz, pode removê-los com segurança.

## 🚀 Início Rápido

### 1. Trabalhar com Agentes

```python
# Em qualquer arquivo Python
from src.agents import get_orchestrator, AgentType

orchestrator = get_orchestrator()

# Criar tarefa
task = orchestrator.create_task(
    AgentType.GIT_INTEGRATION,
    "Verificar status Git",
    {"action": "status"}
)

# Executar
result = orchestrator.execute_task(task)
```

### 2. Trabalhar com Apps

```python
from src.apps.bot import Bot

bot = Bot()
# usar bot...
```

### 3. Executar Scripts

```bash
# Na raiz do projeto
python scripts/git_sync_simple.py
python scripts/master_demo.py
```

### 4. Configurar Docker

```bash
# Na raiz do projeto
docker compose -f config/docker-compose.yml up
```

## 🔍 Procurar Arquivos Específicos

### Agente Específico?
```bash
# Todos os agentes estão em:
ls src/agents/

# Exemplo: Procurar por "git"
find src/agents -name "*git*"
```

### Script Específico?
```bash
# Todos os scripts estão em:
ls scripts/

# Exemplo: Procurar por "sync"
find scripts -name "*sync*"
```

### Documentação Específica?
```bash
# Documentação técnica:
ls docs/

# Documentação Obsidian:
ls "Obsidian_guardar aqui/"
```

## 🛠️ Correções Aplicadas

### ✅ Imports Corrigidos

Arquivos corrigidos:
- ✅ `src/agents/orchestrator.py` - Import do MCPServer
- ✅ `src/agents/mcp_manager_ui.py` - Import do Neo4j
- ✅ `src/agents/mcp_docker_integration.py` - Imports relativos
- ✅ `examples/example_docker_agent_usage.py` - Imports atualizados

### ✅ Estrutura Organizada

- ✅ Todos os agentes em `src/agents/`
- ✅ Todas as aplicações em `src/apps/`
- ✅ Todos os scripts em `scripts/`
- ✅ Todas as documentações organizadas

## 📞 Ajuda Rápida

### "Onde está o orchestrator.py?"
👉 `src/agents/orchestrator.py`

### "Onde está o bot.py?"
👉 `src/apps/bot.py`

### "Como importar o Git Agent?"
```python
from src.agents.git_integration import get_git_agent
```

### "Como executar scripts?"
```bash
python scripts/nome_do_script.py
```

### "Onde está o docker-compose.yml?"
👉 `config/docker-compose.yml`

## 🎯 Resumo Visual

```
📁 ONDE ESTÁ CADA COISA:

🤖 AGENTES      → src/agents/
💻 APPS         → src/apps/
🔧 SCRIPTS      → scripts/
📚 DOCS TÉCNICA → docs/
📝 DOCS OBSIDIAN → Obsidian_guardar aqui/
🐳 DOCKER       → docker/
⚙️ CONFIG       → config/
💡 EXEMPLOS     → examples/
```

## ✅ Checklist de Verificação

Use este checklist para garantir que está no caminho certo:

- [ ] Agentes estão em `src/agents/`
- [ ] Apps estão em `src/apps/`
- [ ] Scripts estão em `scripts/`
- [ ] Documentação técnica em `docs/`
- [ ] Configurações em `config/`
- [ ] Dockerfiles em `docker/`
- [ ] Imports usam `from src.agents...` ou `from src.apps...`
- [ ] Scripts são executados com `python scripts/...`

## 📖 Próximos Passos

1. **Explorar agentes:** Veja `src/agents/`
2. **Ler documentação:** Veja `docs/ENGINEERING_GUIDE.md`
3. **Executar scripts:** Veja `scripts/`
4. **Configurar projeto:** Veja `config/`

---

**💡 Dica:** Use este guia como referência rápida sempre que se perder na estrutura do projeto!

**📝 Última atualização:** Agora com Git Agent integrado

