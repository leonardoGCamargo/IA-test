# 🧹 Organização e Limpeza do Projeto - IA-Test

Este documento descreve a organização atual do projeto e identifica redundâncias.

## ✅ Limpezas Realizadas

### 1. Remoção do Linear MCP
- ✅ Removido de `mcp_servers.json` (já conectado via Cursor)
- ✅ Removido de `.cursor/mcp.json`
- ✅ Removido de `config/env.example`
- ✅ Removido `docs/LINEAR_SETUP.md`

**Motivo:** Linear agora está conectado diretamente pela conta do Cursor, não precisa mais do MCP.

## 📁 Estrutura de Diretórios

### Diretórios Principais

```
IA-test/
├── src/                    # Código fonte principal
│   ├── agents/            # 🤖 TODOS OS AGENTES AQUI
│   └── apps/              # Aplicações (API, Dashboard, etc.)
│
├── config/                # Configurações
│   ├── docker-compose.yml
│   ├── env.example
│   └── requirements.txt
│
├── docker/                # Dockerfiles
│
├── scripts/               # Scripts utilitários
│
├── docs/                  # Documentação
│
├── mcp_servers.json       # 🔌 CONFIGURAÇÃO DOS MCPS
│
├── .cursor/               # Configuração do Cursor
│   └── mcp.json          # 🔌 MCPs para uso no Cursor
│
├── backups/               # ⚠️ Backups (pode ser limpo)
│
└── legacy-backup/         # ⚠️ Backup legado (pode ser limpo)
```

## 🔍 Redundâncias Identificadas

### 1. Diretórios de Backup

#### `backups/`
- **Conteúdo:** Versões antigas de arquivos
- **Status:** ⚠️ Pode ser removido se não for mais necessário
- **Tamanho:** Múltiplos arquivos de documentação duplicados

#### `legacy-backup/`
- **Conteúdo:** Backup completo de versão antiga do projeto
- **Status:** ⚠️ Pode ser removido se não for mais necessário
- **Tamanho:** Inclui código antigo, frontend antigo, etc.

**Recomendação:** Se você tem certeza que não precisa mais desses backups, pode removê-los para limpar o projeto.

### 2. Arquivos Duplicados

#### Documentação Duplicada
- `backups/docs/` contém múltiplas versões de documentos que já estão em `docs/`
- Alguns arquivos podem estar desatualizados

#### Docker Compose
- `backups/docker-compose.backup` - Versão antiga
- `config/docker-compose-consolidado.yml` - Pode ser redundante com `docker-compose.yml`

### 3. Arquivos de Configuração

#### `config/config/`
- Diretório vazio ou com conteúdo redundante
- Verificar se é necessário

#### `config/src/`
- Diretório que pode conter código duplicado
- Verificar se é necessário

## 📋 Estrutura de Agentes e MCPs

### 🤖 Agentes
**Localização:** `src/agents/`

Todos os agentes estão em `src/agents/`:

1. `orchestrator.py` - Coordenador central
2. `system_health_agent.py` - Saúde do sistema
3. `db_manager.py` - Gerenciador de bancos
4. `mcp_manager.py` - Gerenciador MCP
5. `git_integration.py` - Integração Git
6. `mcp_neo4j_integration.py` - GraphRAG Neo4j
7. `mcp_obsidian_integration.py` - Integração Obsidian
8. `mcp_docker_integration.py` - Integração Docker
9. `mcp_kestra_integration.py` - Integração Kestra
10. `diagnostic_agent.py` - ⚠️ Deprecated
11. `resolution_agent.py` - ⚠️ Deprecated
12. `agent_helper_system.py` - ⚠️ Deprecated

**Ver:** `docs/ESTRUTURA_AGENTES_E_MCPS.md` para detalhes completos.

### 🔌 MCPs
**Localização:** `mcp_servers.json` (raiz do projeto)

MCPs configurados:
1. `neo4j` - GraphRAG e conhecimento estruturado ✅
2. `obsidian` - Gestão de notas ✅
3. `git` - Operações Git/GitHub ✅
4. `filesystem` - Acesso ao sistema de arquivos ❌ (desabilitado)

**MCPs no Cursor:** `.cursor/mcp.json`
- `neo4j-cypher` - Para uso direto no Cursor ✅

## 🎯 Recomendações de Limpeza

### Opção 1: Limpeza Conservadora (Recomendada)
Manter os backups por enquanto, mas organizar melhor:

```bash
# Criar um único diretório de backup consolidado
mkdir -p archive/backups
# Mover backups antigos para lá se necessário
```

### Opção 2: Limpeza Completa
Remover diretórios de backup se tiver certeza:

```bash
# ⚠️ CUIDADO: Isso remove permanentemente
rm -rf backups/
rm -rf legacy-backup/
```

### Opção 3: Verificação Manual
Revisar cada arquivo antes de remover:
- Verificar se há código útil em `legacy-backup/`
- Verificar se há documentação importante em `backups/docs/`

## 📊 Estatísticas do Projeto

### Agentes
- **Total:** 12 arquivos
- **Ativos:** 9
- **Deprecated:** 3 (mantidos para compatibilidade)

### MCPs
- **Total:** 4 configurados
- **Habilitados:** 3
- **Desabilitados:** 1

### Documentação
- **Total:** ~30 arquivos em `docs/`
- **Backups:** ~10 arquivos em `backups/docs/`

## 🔗 Referências

- **Estrutura de Agentes e MCPs:** `docs/ESTRUTURA_AGENTES_E_MCPS.md`
- **Melhorias Neo4j:** `docs/NEO4J_IMPROVEMENTS_SUMMARY.md`
- **Setup Neo4j MCP:** `docs/CURSOR_NEO4J_MCP_SETUP.md`

---

**Última atualização**: 2025-01-27
**Status:** Projeto organizado, redundâncias identificadas

