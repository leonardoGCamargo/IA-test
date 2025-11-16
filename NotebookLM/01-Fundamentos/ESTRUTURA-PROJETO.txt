# 📁 Estrutura Completa do Projeto IA-Test

> **Última atualização:** 2025-01-27

## 📋 Visão Geral

Este documento descreve a estrutura completa do projeto IA-Test após organização.

## 🗂️ Estrutura de Diretórios

```
IA-test/
├── src/                          # Código-fonte principal
│   ├── agents/                   # 14 agentes especializados
│   │   ├── agent_dashboard_ui.py
│   │   ├── agent_helper_system.py
│   │   ├── db_manager.py
│   │   ├── diagnostic_agent.py
│   │   ├── git_integration.py
│   │   ├── kestra_langchain_master.py
│   │   ├── mcp_docker_integration.py
│   │   ├── mcp_kestra_integration.py
│   │   ├── mcp_manager.py
│   │   ├── mcp_manager_ui.py
│   │   ├── mcp_neo4j_integration.py
│   │   ├── mcp_obsidian_integration.py
│   │   ├── orchestrator.py
│   │   └── resolution_agent.py
│   └── apps/                     # 6 aplicações principais
│       ├── api.py
│       ├── bot.py
│       ├── chains.py
│       ├── loader.py
│       ├── pdf_bot.py
│       └── utils.py
│
├── front-end/                    # Front-end Svelte
│   ├── src/
│   ├── public/
│   └── package.json
│
├── docker/                       # 9 Dockerfiles
│   ├── agent_dashboard.Dockerfile
│   ├── api.Dockerfile
│   ├── bot.Dockerfile
│   ├── front-end.Dockerfile
│   ├── loader.Dockerfile
│   ├── mcp_docker_integration.Dockerfile
│   ├── mcp_manager.Dockerfile
│   ├── pdf_bot.Dockerfile
│   └── pull_model.Dockerfile
│
├── config/                       # Configurações
│   ├── docker-compose.yml        # Docker Compose otimizado
│   ├── docker-compose.optimized.yml
│   ├── docker-compose.stacks.yml
│   ├── requirements.txt          # Dependências Python
│   └── env.example               # Exemplo de variáveis de ambiente
│
├── docs/                         # 21 documentos técnicos
│   ├── AGENT_DASHBOARD_README.md
│   ├── ARCHITECTURE.md
│   ├── ARCHITECTURE_DEEP_DIVE.md
│   ├── DASHBOARD_RESUMO.md
│   ├── DASHBOARD_SETUP.md
│   ├── DB_MANAGER_README.md
│   ├── DOCKER_CLEANUP_SUMMARY.md
│   ├── DOCKER_INTEGRATION_README.md
│   ├── DOCKER_OPTIMIZATION.md
│   ├── ENGINEERING_GUIDE.md
│   ├── EXECUTION_PLAN.md
│   ├── GIT_INTEGRATION_README.md
│   ├── MASTER_AGENT_README.md
│   ├── MCP_ARCHITECTURE.md
│   ├── MCP_README.md
│   ├── ORCHESTRATOR_SUMMARY.md
│   ├── ORGANIZACAO_COMPLETA.md
│   ├── ORGANIZACAO_FINALIZADA.md
│   ├── ORGANIZACAO_PROJETO.md
│   ├── README.md
│   └── REDUNDANCIAS_RELATORIO.md
│
├── scripts/                      # 13 scripts utilitários
│   ├── cleanup_containers.ps1
│   ├── cleanup_containers.sh
│   ├── consolidate_structure.ps1
│   ├── create_obsidian_map.py
│   ├── finalize_organization.py
│   ├── git_sync_simple.py
│   ├── git_sync.py
│   ├── map_to_obsidian.py
│   ├── master_demo.py
│   ├── organize_and_map.py
│   ├── organize_project.py
│   ├── run_dashboard.py
│   └── stop_random_containers.ps1
│
├── examples/                     # Exemplos de uso
│   └── example_docker_agent_usage.py
│
├── embedding_model/              # Modelos de embedding
│
├── images/                       # Imagens
│   └── datamodel.png
│
└── Obsidian_guardar aqui/        # Documentação Obsidian
    ├── PROJETO-IA-TEST.md        # Mapeamento principal
    ├── project_mapping.json      # Mapeamento JSON
    ├── ESTRUTURA-PROJETO.md      # Este arquivo
    ├── 00-MAPA-DE-AGENTES.md
    ├── 01-Guia-Obsidian.md
    ├── 02-Guia-Cursor.md
    ├── 03-Manual-Sistema-Agentes.md
    ├── 04-Como-Criar-Agentes.md
    └── Agentes/                  # Notas dos agentes
        ├── Docker-Integration.md
        ├── Helper-System.md
        ├── Kestra-Agent.md
        ├── Master-Agent.md
        ├── MCP-Manager.md
        ├── Neo4j-GraphRAG.md
        ├── Obsidian-Integration.md
        └── Orchestrator.md
```

## 📊 Estatísticas

- **Agentes:** 14
- **Aplicações:** 6
- **Documentos:** 21
- **Scripts:** 13
- **Dockerfiles:** 9

## 🔗 Links Relacionados

- [[PROJETO-IA-TEST]] - Mapeamento completo do projeto
- [[00-MAPA-DE-AGENTES]] - Mapa detalhado dos agentes
- [[01-Guia-Obsidian]] - Guia de uso do Obsidian

---
*Última atualização: 2025-01-27*

