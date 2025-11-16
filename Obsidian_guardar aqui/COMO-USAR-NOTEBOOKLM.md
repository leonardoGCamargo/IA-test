# 📚 Como Usar Documentos no NotebookLM

> **Guia para Sincronizar e Usar no Google NotebookLM**

---

## 🎯 Objetivo

Sincronizar a documentação do Obsidian para uma pasta que o **Google NotebookLM** possa usar como fonte de conhecimento.

---

## 📋 Passo a Passo

### 1. Preparar Documentos

Execute o script de preparação:

```bash
python scripts/preparar_para_notebooklm.py
```

Isso vai:
- ✅ Criar pasta `NotebookLM/` organizada
- ✅ Copiar documentos do Obsidian
- ✅ Organizar por categorias
- ✅ Criar índices

---

### 2. Sincronizar com Google Drive

**Opção A: Pasta já está no Drive**
- Se a pasta do projeto já está linkada ao Drive
- A pasta `NotebookLM/` será sincronizada automaticamente

**Opção B: Mover pasta NotebookLM para Drive**
1. Copie a pasta `NotebookLM/` para seu Google Drive
2. Aguarde sincronização completa
3. Certifique-se de que todos os arquivos foram sincronizados

---

### 3. Adicionar no NotebookLM

1. **Abra o NotebookLM**
   - Acesse: https://notebooklm.google.com/

2. **Crie um novo Notebook**
   - Clique em "New Notebook"

3. **Adicione Fonte**
   - Clique em "Add Source"
   - Selecione "Google Drive"
   - Escolha a pasta `NotebookLM/`

4. **Aguarde Indexação**
   - O NotebookLM vai indexar todos os documentos
   - Isso pode levar alguns minutos

---

## 📁 Estrutura Criada

```
NotebookLM/
├── README.md (explicação)
├── INDICE-PRINCIPAL.md (índice completo)
├── 01-Fundamentos/
│   ├── PROJETO-IA-TEST.md
│   ├── 00-MAPA-DE-AGENTES.md
│   └── ...
├── 02-LangChain-LangGraph/
│   ├── LANGCHAIN-LANGGRAPH-GUIA.md
│   ├── LANGCHAIN-FUNDAMENTOS.md
│   └── ...
├── 03-Agentes/
│   ├── Orchestrator.md
│   ├── System-Health.md
│   └── ...
├── 04-Configuracao/
│   └── ...
├── 05-Exemplos/
│   └── ...
└── 06-Referencias/
    └── ...
```

---

## 💡 Dicas de Uso no NotebookLM

### Perguntas Úteis

1. **Sobre LangChain:**
   - "Como funciona o LangChain?"
   - "Como criar um workflow com LangGraph?"
   - "Quais são os padrões de LangGraph?"

2. **Sobre o Projeto:**
   - "Como funciona o Orchestrator?"
   - "Quais agentes temos no projeto?"
   - "Como configurar o Neo4j?"

3. **Sobre Integrações:**
   - "Como integrar Neo4j com LangChain?"
   - "Como usar GraphRAG?"
   - "Como criar agentes com LangGraph?"

---

## 🔄 Sincronização Automática

### Script de Sincronização

Crie um script para manter sincronizado:

```bash
python scripts/sincronizar_notebooklm.py
```

Isso vai:
- Verificar documentos novos/modificados
- Atualizar pasta NotebookLM
- Manter estrutura organizada

---

## 📝 Notas Importantes

1. **Formato Markdown**
   - NotebookLM lê bem arquivos .md
   - Mantém formatação e links

2. **Estrutura Organizada**
   - Pastas ajudam NotebookLM a entender contexto
   - Índices facilitam navegação

3. **Atualizações**
   - Execute o script quando adicionar novos documentos
   - NotebookLM vai re-indexar automaticamente

---

## 🔗 Links Relacionados

- [[PROJETO-IA-TEST|Projeto Principal]]
- [[LANGCHAIN-LANGGRAPH-GUIA|Guia LangChain]]
- [[ESTRUTURA-PROJETO|Estrutura do Projeto]]

---

## 🏷️ Tags

#notebooklm #google-drive #sincronizacao #documentacao

---

**Última atualização:** 2025-01-27

