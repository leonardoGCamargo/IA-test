# 📁 Organização do Projeto - Documentação

> **Guia sobre a organização profissional dos arquivos do projeto**

## 🎯 Visão Geral

O projeto foi reorganizado em uma estrutura profissional e limpa para facilitar navegação, manutenção e desenvolvimento.

## 📂 Estrutura de Diretórios

```
projeto/
├── src/
│   ├── agents/          # Agentes principais do sistema
│   │   ├── orchestrator.py           # Coordenador central
│   │   ├── kestra_langchain_master.py # Master Agent
│   │   ├── agent_helper_system.py    # Helper System
│   │   ├── mcp_manager.py            # MCP Manager
│   │   ├── mcp_manager_ui.py         # UI do MCP Manager
│   │   ├── mcp_docker_integration.py # Integração Docker
│   │   ├── mcp_neo4j_integration.py  # Integração Neo4j
│   │   ├── mcp_obsidian_integration.py # Integração Obsidian
│   │   └── mcp_kestra_integration.py # Integração Kestra
│   └── apps/            # Aplicações existentes
│       ├── bot.py        # Support Bot
│       ├── loader.py     # Stack Overflow Loader
│       ├── pdf_bot.py    # PDF Bot
│       ├── api.py        # API
│       ├── chains.py     # LangChain chains
│       └── utils.py      # Utilitários
├── scripts/             # Scripts utilitários
│   ├── master_demo.py                # Demo do Master Agent
│   ├── sync_obsidian_docs.py         # Sincronização Obsidian
│   └── verificar_integracao_obsidian.py # Verificação de integração
├── docs/                # Documentação técnica
│   ├── ARCHITECTURE.md              # Arquitetura do sistema
│   ├── ENGINEERING_GUIDE.md         # Guia para engenheiros
│   ├── ARCHITECTURE_DEEP_DIVE.md    # Análise técnica profunda
│   ├── EXECUTION_PLAN.md            # Plano de execução
│   ├── ORCHESTRATOR_SUMMARY.md      # Resumo do Orchestrator
│   ├── SURPRISE_PROJECT.md          # Projeto surpresa
│   ├── MASTER_AGENT_README.md       # Manual do Master Agent
│   ├── MCP_README.md                # Manual do MCP
│   ├── MCP_ARCHITECTURE.md          # Arquitetura MCP
│   ├── DOCKER_INTEGRATION_README.md # Integração Docker
│   └── README.md                    # Índice da documentação
├── Obsidian_guardar aqui/  # Documentação Obsidian
│   ├── 00-MAPA-DE-AGENTES.md        # Mapa de agentes
│   ├── 01-Guia-Obsidian.md          # Guia do Obsidian
│   ├── 02-Guia-Cursor.md            # Guia do Cursor
│   ├── 03-Manual-Sistema-Agentes.md # Manual do sistema
│   ├── 04-Como-Criar-Agentes.md     # Como criar agentes
│   ├── RESUMO-MAPA-AGENTES.md       # Resumo do mapa
│   ├── OBSIDIAN-MCP-INTEGRATION.md  # Integração Obsidian-MCP
│   ├── README_SYNC_OBSIDIAN.md      # README sincronização
│   └── Agentes/                     # Documentação individual
│       ├── Orchestrator.md
│       ├── Master-Agent.md
│       ├── Helper-System.md
│       ├── MCP-Manager.md
│       ├── Docker-Integration.md
│       ├── Neo4j-GraphRAG.md
│       ├── Obsidian-Integration.md
│       └── Kestra-Agent.md
├── docker/              # Dockerfiles
│   ├── api.Dockerfile
│   ├── bot.Dockerfile
│   ├── loader.Dockerfile
│   ├── pdf_bot.Dockerfile
│   ├── front-end.Dockerfile
│   ├── pull_model.Dockerfile
│   ├── mcp_manager.Dockerfile
│   └── mcp_docker_integration.Dockerfile
├── examples/            # Exemplos de uso
│   └── example_docker_agent_usage.py
├── config/              # Configurações
│   ├── docker-compose.yml
│   ├── env.example
│   └── requirements.txt
└── front-end/           # Frontend (Svelte)
    ├── src/
    ├── public/
    └── ...
```

## 🗂️ Organização por Categoria

### Agentes (`src/agents/`)
Todos os agentes principais do sistema:
- **Orchestrator**: Coordenador central
- **Master Agent**: Planejamento inteligente
- **Helper System**: Monitoramento e otimização
- **MCP Manager**: Gerenciamento de servidores MCP
- **Integrações**: Docker, Neo4j, Obsidian, Kestra

### Aplicações (`src/apps/`)
Aplicações existentes que não são agentes:
- Bots (Support, PDF)
- Loader (Stack Overflow)
- API
- Utilitários

### Scripts (`scripts/`)
Scripts utilitários para tarefas específicas:
- Demos
- Sincronização
- Verificação

### Documentação (`docs/`)
Documentação técnica completa:
- Arquitetura
- Guias de engenharia
- Manuais técnicos

### Obsidian (`Obsidian_guardar aqui/`)
Documentação formatada para Obsidian:
- Mapas de agentes
- Guias de uso
- Documentação individual

### Docker (`docker/`)
Todos os Dockerfiles organizados em uma pasta.

### Configuração (`config/`)
Arquivos de configuração:
- `docker-compose.yml`
- `env.example`
- `requirements.txt`

## 🧹 Limpeza Realizada

### Arquivos Removidos
- `criar_notas_obsidian.py` - Substituído por `sync_obsidian_docs.py`

### Arquivos Mantidos
- Todos os arquivos de código fonte
- Toda a documentação
- Todos os exemplos úteis

## 📝 Imports Corrigidos

Após a reorganização, todos os imports foram corrigidos:

```python
# Antes
from mcp_manager import get_mcp_manager

# Depois
from src.agents.mcp_manager import get_mcp_manager
```

## 🔧 Docker Compose Atualizado

O `docker-compose.yml` foi atualizado para usar os novos caminhos:

```yaml
services:
  bot:
    build:
      context: ..
      dockerfile: docker/bot.Dockerfile
```

## 📚 Benefícios da Organização

### Para Desenvolvedores
- ✅ Fácil localização de arquivos
- ✅ Estrutura clara e intuitiva
- ✅ Imports organizados
- ✅ Separação clara de responsabilidades

### Para Engenheiros
- ✅ Código profissional
- ✅ Fácil manutenção
- ✅ Escalabilidade
- ✅ Documentação organizada

### Para o Projeto
- ✅ Melhor navegação
- ✅ Facilita onboarding
- ✅ Facilita colaboração
- ✅ Facilita testes

## 🚀 Próximos Passos

1. **Testar a Estrutura:**
   ```bash
   python -c "from src.agents import get_orchestrator; print('OK')"
   ```

2. **Verificar Docker:**
   ```bash
   docker compose -f config/docker-compose.yml config
   ```

3. **Sincronizar Obsidian:**
   ```bash
   python scripts/sync_obsidian_docs.py
   ```

## 📖 Referências

- [[README|README Principal]]
- [[../docs/README|Documentação Técnica]]
- [[../Obsidian_guardar aqui/00-MAPA-DE-AGENTES|Mapa de Agentes]]

## 🏷️ Tags

#organização #estrutura #desenvolvimento #engenharia

---

**Última atualização:** {{date}}  
**Versão:** 1.0.0

