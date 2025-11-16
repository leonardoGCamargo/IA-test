# 📚 Documentação para NotebookLM

Esta pasta contém toda a documentação do projeto organizada para uso no **Google NotebookLM**.

## ⚠️ IMPORTANTE: Formatos de Arquivo

O NotebookLM **aceita** os seguintes formatos:
- ✅ **TXT** - Arquivos de texto simples (já convertidos)
- ✅ **DOCX** - Documentos Microsoft Word (recomendado)
- ✅ **PDF** - Documentos PDF
- ❌ **MD** - Markdown pode não funcionar corretamente

**Arquivos já convertidos para TXT estão disponíveis!**

Para converter para DOCX (recomendado):
```bash
python scripts/converter_para_notebooklm.py --formato docx
```

## 📁 Estrutura

- **01-Fundamentos/** - Documentos base do projeto
- **02-LangChain-LangGraph/** - Guias completos de LangChain
- **03-Agentes/** - Documentação de cada agente
- **04-Configuracao/** - Guias de configuração
- **05-Exemplos/** - Exemplos práticos
- **06-Referencias/** - Referências e links

## 🚀 Como Usar

1. **Sincronize esta pasta no Google Drive**
   - Certifique-se de que está sincronizada

2. **No NotebookLM:**
   - Adicione esta pasta como fonte
   - O NotebookLM vai indexar todos os documentos

3. **Faça perguntas:**
   - Sobre LangChain e LangGraph
   - Sobre os agentes do projeto
   - Sobre configurações
   - Sobre exemplos práticos

## 📖 Índice

Veja **INDICE-PRINCIPAL.md** para lista completa de documentos.

## 🔄 Atualizar Documentos

Quando adicionar novos documentos no Obsidian:

```bash
# 1. Preparar documentos
python scripts/preparar_para_notebooklm.py

# 2. Converter para formato aceito
python scripts/converter_para_notebooklm.py --formato docx
```

---

**Última atualização:** 2025-01-27
