# 📄 Formatos Aceitos pelo NotebookLM

> **Informações sobre formatos de arquivo**

---

## ✅ Formatos Aceitos pelo NotebookLM

Baseado na documentação oficial do Google NotebookLM:

### Formatos de Texto
- ✅ **TXT** - Arquivos de texto simples
- ✅ **DOCX** - Documentos Microsoft Word
- ✅ **PDF** - Documentos PDF
- ✅ **MD** - Markdown (pode não funcionar em todos os casos)

### Outros Formatos
- ✅ **JSON** - Arquivos JSON estruturados
- ✅ **CSV** - Planilhas CSV

---

## 🔄 Solução: Converter .md para Formatos Aceitos

### Opção 1: TXT (Mais Simples)

**Vantagens:**
- ✅ Sem dependências extras
- ✅ Funciona sempre
- ✅ Mantém conteúdo completo

**Como usar:**
```bash
python scripts/converter_para_notebooklm.py --formato txt
```

---

### Opção 2: DOCX (Recomendado)

**Vantagens:**
- ✅ Formato nativo do NotebookLM
- ✅ Mantém formatação básica
- ✅ Melhor visualização

**Como usar:**
```bash
# Instalar dependência
pip install python-docx

# Converter
python scripts/converter_para_notebooklm.py --formato docx
```

---

### Opção 3: PDF (Profissional)

**Vantagens:**
- ✅ Formatação completa
- ✅ Visual profissional
- ✅ Compatível com todos os sistemas

**Como usar:**
```bash
# Instalar dependências
pip install markdown weasyprint

# Converter
python scripts/converter_para_notebooklm.py --formato pdf
```

---

## 📋 Script de Conversão

O script `converter_para_notebooklm.py` faz:

1. ✅ Lê todos os arquivos .md do Obsidian
2. ✅ Converte para o formato escolhido (TXT, DOCX, ou PDF)
3. ✅ Salva na pasta NotebookLM/ organizada
4. ✅ Mantém a estrutura de pastas

---

## 🚀 Uso Rápido

### Converter para TXT (Mais Rápido)
```bash
python scripts/converter_para_notebooklm.py --formato txt
```

### Converter para DOCX (Recomendado)
```bash
python scripts/converter_para_notebooklm.py --formato docx
```

### Instalar Dependências
```bash
python scripts/converter_para_notebooklm.py --instalar
```

---

## 📁 Estrutura Após Conversão

```
NotebookLM/
├── 01-Fundamentos/
│   ├── PROJETO-IA-TEST.txt (ou .docx, .pdf)
│   ├── 00-MAPA-DE-AGENTES.txt
│   └── ...
├── 02-LangChain-LangGraph/
│   ├── LANGCHAIN-LANGGRAPH-GUIA.txt
│   └── ...
└── ...
```

---

## ✅ Próximos Passos

1. **Converter arquivos:**
   ```bash
   python scripts/converter_para_notebooklm.py --formato docx
   ```

2. **Sincronizar com Google Drive:**
   - A pasta NotebookLM/ será sincronizada automaticamente

3. **Adicionar no NotebookLM:**
   - Adicione a pasta NotebookLM/ como fonte
   - O NotebookLM vai ler os arquivos convertidos

---

## 🏷️ Tags

#notebooklm #formatos #conversao #docx #pdf #txt

---

**Última atualização:** 2025-01-27

