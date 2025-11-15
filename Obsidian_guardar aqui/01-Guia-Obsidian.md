# 📝 Guia de Uso do Obsidian

> **Como usar o Obsidian para documentar e navegar pelo sistema de agentes**

## 🎯 O que é o Obsidian

O Obsidian é um editor de markdown poderoso que funciona como um **segundo cérebro** para suas notas. Ele usa links entre notas (wikilinks) para criar uma rede de conhecimento.

## 🔗 Links no Obsidian

### Formato de Links
- `[[nome-do-arquivo]]` - Cria um link para outra nota
- `[[nome-do-arquivo|texto visível]]` - Link com texto personalizado
- `[[nome-do-arquivo#seção]]` - Link para seção específica

### Exemplos
```markdown
Veja o [[Orchestrator]] para mais detalhes.
Consulte [[MCP-Manager|Gerenciador MCP]].
Leia a seção [[Master-Agent#como-usar]].
```

## 📁 Estrutura de Pastas Recomendada

```
vault/
├── 00-MAPA-DE-AGENTES.md          # Ponto de entrada
├── 01-Guia-Obsidian.md            # Este arquivo
├── 02-Guia-Cursor.md              # Guia do Cursor
├── 03-Manual-Sistema-Agentes.md   # Manual do sistema
├── 04-Como-Criar-Agentes.md       # Como criar agentes
├── Agentes/                       # Documentação dos agentes
│   ├── Orchestrator.md
│   ├── Master-Agent.md
│   ├── Helper-System.md
│   ├── MCP-Manager.md
│   ├── Docker-Integration.md
│   ├── Neo4j-GraphRAG.md
│   ├── Obsidian-Integration.md
│   └── Kestra-Agent.md
└── Documentação/                  # Documentação adicional
    ├── ARCHITECTURE.md
    ├── EXECUTION_PLAN.md
    └── ...
```

## 🔍 Navegação no Obsidian

### 1. Graph View (Visualização de Grafo)
- **Atalho:** `Ctrl+G` (Windows) / `Cmd+G` (Mac)
- **Uso:** Visualiza conexões entre notas
- **Dica:** Filtre por tags para focar em agentes específicos

### 2. Search (Busca)
- **Atalho:** `Ctrl+Shift+F` (Windows) / `Cmd+Shift+F` (Mac)
- **Uso:** Busca em todas as notas
- **Filtros:** Use `tag:#agente` para buscar por tags

### 3. Backlinks (Links de Volta)
- **Painel:** Abra o painel lateral direito
- **Uso:** Veja todas as notas que linkam para a nota atual
- **Útil:** Descobre quais notas mencionam um agente

### 4. Outline (Estrutura)
- **Painel:** Abra o painel lateral direito
- **Uso:** Veja a estrutura de títulos da nota atual
- **Útil:** Navegação rápida em documentos longos

## 🏷️ Usando Tags

### Tags Recomendadas
- `#agente` - Para todos os agentes
- `#orchestrator` - Específico do Orchestrator
- `#mcp` - MCP Manager e integrações
- `#neo4j` - Neo4j GraphRAG
- `#obsidian` - Obsidian Integration
- `#kestra` - Kestra Agent
- `#langchain` - LangChain e Master Agent
- `#docker` - Docker Integration
- `#documentação` - Documentação geral
- `#tutorial` - Tutoriais e guias
- `#exemplo` - Exemplos de código

### Como Usar Tags
```markdown
---
tags: #agente #orchestrator #documentação
---

# Título da Nota
Conteúdo...
```

## 📊 Templates Úteis

### Template para Nova Nota de Agente
```markdown
# Nome do Agente

> **Tipo:** Tipo do agente  
> **Arquivo:** `nome_arquivo.py`  
> **Status:** ✅ Funcional / ⚠️ Em desenvolvimento / ❌ Não disponível

## 📋 Descrição

Breve descrição do agente...

## 🎯 Funcionalidades

- Funcionalidade 1
- Funcionalidade 2

## 💻 Como Usar

\`\`\`python
# Exemplo de código
from modulo import função
resultado = função()
\`\`\`

## 🔗 Links Relacionados

- [[Orchestrator]] - Como usar via Orchestrator
- [[Outro-Agente]] - Relacionado

## 🏷️ Tags

#agente #tipo #documentação
```

### Template para Nota de Tutorial
```markdown
# Título do Tutorial

## Objetivo

O que você vai aprender...

## Pré-requisitos

- Requisito 1
- Requisito 2

## Passo a Passo

### Passo 1: ...
Descrição...

### Passo 2: ...
Descrição...

## Resultado Esperado

O que você deve ver ao final...

## 🔗 Próximos Passos

- [[Próximo-Tutorial]]

## 🏷️ Tags

#tutorial #exemplo
```

## 🎨 Formatação Avançada

### Callouts (Caixas de Destacar)
```markdown
> [!info] Informação
> Texto informativo

> [!tip] Dica
> Dica útil

> [!warning] Aviso
> Cuidado!

> [!error] Erro
> Algo está errado

> [!note] Nota
> Observação importante
```

### Código com Syntax Highlighting
```python
from orchestrator import get_orchestrator

orchestrator = get_orchestrator()
status = orchestrator.get_system_status()
```

### Tabelas
| Coluna 1 | Coluna 2 | Coluna 3 |
|----------|----------|----------|
| Dado 1   | Dado 2   | Dado 3   |

### Checklist
- [ ] Tarefa não concluída
- [x] Tarefa concluída

## 🔗 Integração com o Sistema

### Criar Nota sobre um Agente
O sistema pode criar notas automaticamente:

```python
from mcp_obsidian_integration import ObsidianManager

obsidian = ObsidianManager()
obsidian.create_mcp_note("Nome-Agente", {
    "command": "...",
    "description": "..."
})
```

### Importar Notas para Neo4j
Todas as notas do Obsidian podem ser importadas para o Neo4j:

```python
from mcp_neo4j_integration import get_neo4j_manager

neo4j = get_neo4j_manager()
neo4j.import_obsidian_vault(Path("caminho/para/vault"))
```

## 🎯 Dicas de Produtividade

### 1. Use o Daily Notes
- Atalho: `Ctrl+N` e digite "Daily"
- Use para anotações diárias sobre o sistema

### 2. Crie MOC (Map of Content)
- Crie notas que são índices para outras notas
- Exemplo: [[00-MAPA-DE-AGENTES]] é um MOC

### 3. Use Aliases
```yaml
---
aliases: [Orquestrador, Coordenador]
---
```
Permite acessar a nota por múltiplos nomes

### 4. Use o Canvas
- Visualize conexões entre agentes
- Arrume notas em um canvas visual

## 📱 Plugins Recomendados

1. **Dataview** - Query e visualização de dados
2. **Templater** - Templates avançados
3. **Calendar** - Integração com calendário
4. **Excalidraw** - Diagramas e desenhos
5. **Graph Analysis** - Análise de grafo

## 🔗 Links Úteis

- [[00-MAPA-DE-AGENTES|Voltar ao Mapa de Agentes]]
- [[02-Guia-Cursor|Próximo: Guia do Cursor]]
- [[03-Manual-Sistema-Agentes|Manual do Sistema]]

## 🏷️ Tags

#obsidian #guia #tutorial #documentação #formatação

---

**Dica:** Este guia está vivo! Adicione suas próprias dicas e truques aqui.

