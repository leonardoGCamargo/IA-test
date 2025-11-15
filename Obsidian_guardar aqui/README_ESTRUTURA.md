# 📁 Estrutura do Projeto

## 📂 Organização

```
projeto/
├── src/
│   ├── agents/          # Agentes principais
│   │   ├── orchestrator.py
│   │   ├── kestra_langchain_master.py
│   │   ├── agent_helper_system.py
│   │   ├── mcp_manager.py
│   │   └── ...
│   └── apps/            # Aplicações existentes
│       ├── bot.py
│       ├── loader.py
│       ├── pdf_bot.py
│       └── api.py
├── scripts/             # Scripts utilitários
│   ├── master_demo.py
│   ├── sync_obsidian_docs.py
│   └── verificar_integracao_obsidian.py
├── docs/                # Documentação geral
│   ├── ARCHITECTURE.md
│   ├── EXECUTION_PLAN.md
│   └── ...
├── Obsidian_guardar aqui/  # Documentação Obsidian
│   ├── 00-MAPA-DE-AGENTES.md
│   ├── Agentes/
│   └── ...
├── docker/              # Dockerfiles
├── examples/            # Exemplos
├── config/              # Configurações
└── front-end/           # Frontend (Svelte)
```

## 🚀 Início Rápido

### 1. Configuração
```bash
cd config
cp env.example .env
# Edite o .env com suas configurações
```

### 2. Instalar Dependências
```bash
pip install -r config/requirements.txt
```

### 3. Iniciar Sistema
```bash
docker compose -f config/docker-compose.yml up
```

## 📚 Documentação

- **Mapa de Agentes**: `Obsidian_guardar aqui/00-MAPA-DE-AGENTES.md`
- **Arquitetura**: `docs/ARCHITECTURE.md`
- **Guia do Obsidian**: `Obsidian_guardar aqui/01-Guia-Obsidian.md`

## 🤖 Agentes

Ver `src/agents/` para código dos agentes.

## 📝 Scripts

Ver `scripts/` para scripts utilitários.

---
**Estrutura organizada para fácil navegação e manutenção**
