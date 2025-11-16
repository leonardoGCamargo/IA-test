# 📁 Como Sincronizar com Google Drive para NotebookLM

> **Guia Completo de Sincronização**

---

## 🎯 Objetivo

Sincronizar a pasta `NotebookLM/` com o Google Drive para usar no **Google NotebookLM**.

---

## 📋 Passo a Passo

### Opção 1: Pasta do Projeto Já Está no Drive

Se a pasta `IA-test/` já está sincronizada com o Google Drive:

1. ✅ **A pasta `NotebookLM/` será sincronizada automaticamente**
2. ✅ Aguarde a sincronização completa (verifique no Google Drive)
3. ✅ No NotebookLM, adicione a pasta `NotebookLM/` como fonte

---

### Opção 2: Mover Apenas a Pasta NotebookLM

Se você quer apenas a pasta `NotebookLM/` no Drive:

1. **Copie a pasta `NotebookLM/` para seu Google Drive:**
   ```
   C:\Users\Gianmarino L\Documents\IA\IA-test\NotebookLM
   ↓
   Google Drive\NotebookLM
   ```

2. **Aguarde sincronização completa**

3. **No NotebookLM, adicione a pasta do Drive**

---

### Opção 3: Usar Google Drive Desktop

1. **Instale Google Drive Desktop** (se ainda não tiver)
   - Baixe em: https://www.google.com/drive/download/

2. **Configure sincronização:**
   - Abra Google Drive Desktop
   - Vá em Preferências → Meu Computador
   - Adicione a pasta `NotebookLM/`
   - Ative sincronização

3. **Aguarde sincronização**

---

## 🔄 Manter Sincronizado

### Sincronização Automática

Execute quando adicionar/modificar documentos:

```bash
python scripts/sincronizar_notebooklm.py
```

Este script:
- ✅ Verifica documentos novos/modificados
- ✅ Atualiza pasta NotebookLM
- ✅ Mantém estrutura organizada

---

## 📱 Usar no NotebookLM

### 1. Acessar NotebookLM

- URL: https://notebooklm.google.com/
- Faça login com sua conta Google

### 2. Criar Novo Notebook

- Clique em "New Notebook" ou "Novo Notebook"

### 3. Adicionar Fonte

- Clique em "Add Source" ou "Adicionar Fonte"
- Selecione "Google Drive"
- Navegue até a pasta `NotebookLM/`
- Selecione a pasta inteira

### 4. Aguardar Indexação

- O NotebookLM vai indexar todos os documentos
- Isso pode levar alguns minutos
- Você verá o progresso na tela

---

## 💡 Perguntas Úteis no NotebookLM

### Sobre LangChain e LangGraph

- "Como funciona o LangChain?"
- "Como criar um workflow com LangGraph?"
- "Quais são os padrões de LangGraph?"
- "Como integrar Neo4j com LangChain?"
- "Como criar agentes com LangGraph?"

### Sobre o Projeto

- "Como funciona o Orchestrator?"
- "Quais agentes temos no projeto?"
- "Como configurar o Neo4j?"
- "Como usar GraphRAG?"

### Sobre Configuração

- "Quais configurações estão faltando?"
- "Como configurar o Google Gemini?"
- "Como conectar ao MongoDB?"

---

## 📁 Estrutura no NotebookLM

```
NotebookLM/
├── README.md (este arquivo)
├── INDICE-PRINCIPAL.md (índice completo)
├── 01-Fundamentos/ (4 documentos)
├── 02-LangChain-LangGraph/ (10 documentos)
├── 03-Agentes/ (9 documentos)
├── 04-Configuracao/ (4 documentos)
├── 05-Exemplos/ (2 documentos)
└── 06-Referencias/ (2 documentos)
```

**Total: 31 documentos organizados**

---

## ✅ Verificação

### Verificar Sincronização

1. **No Google Drive:**
   - Abra Google Drive no navegador
   - Verifique se a pasta `NotebookLM/` está lá
   - Confirme que todos os arquivos foram sincronizados

2. **No NotebookLM:**
   - Adicione a pasta como fonte
   - Verifique se todos os documentos aparecem
   - Teste fazendo uma pergunta

---

## 🔄 Atualizações Futuras

Quando adicionar novos documentos no Obsidian:

1. Execute: `python scripts/sincronizar_notebooklm.py`
2. Aguarde sincronização no Drive
3. O NotebookLM vai re-indexar automaticamente

---

## 🏷️ Tags

#notebooklm #google-drive #sincronizacao #documentacao

---

**Última atualização:** 2025-01-27

