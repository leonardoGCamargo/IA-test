# 📋 Instruções - Enviar Issues para Linear

## ✅ Scripts Criados

1. ✅ `scripts/send_issues_to_linear.py` - Script principal para enviar issues
2. ✅ `scripts/setup_linear.py` - Script interativo de configuração
3. ✅ `GUIA_RAPIDO_LINEAR.md` - Guia rápido

## 🚀 Como Enviar Issues

### Passo 1: Obter API Key do Linear

1. Acesse: **https://linear.app/settings/api**
2. Clique em **"Create API Key"**
3. Dê um nome (ex: "IA-Test Integration")
4. Copie a chave (formato: `lin_api_xxxxxxxxxxxxx`)

### Passo 2: Configurar

**Opção A: Script Interativo (Mais Fácil)**
```bash
python scripts/setup_linear.py
```
Siga as instruções na tela.

**Opção B: Manual**
Adicione ao `.env` (na raiz ou em `config/`):
```bash
LINEAR_API_KEY=lin_api_xxxxxxxxxxxxx
LINEAR_TEAM_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx  # Opcional
```

**Opção C: Via Argumento**
```bash
python scripts/send_issues_to_linear.py lin_api_xxxxxxxxxxxxx
```

### Passo 3: Enviar Issues

```bash
python scripts/send_issues_to_linear.py
```

## 📊 O que Acontece

O script irá:
1. ✅ Verificar sua API key
2. ✅ Detectar seu Team ID automaticamente (ou usar o configurado)
3. ✅ Criar 24 labels automaticamente (se não existirem)
4. ✅ Ler `LINEAR_ISSUES.md` (47 issues)
5. ✅ Criar todas as issues no Linear
6. ✅ Salvar resultado em `linear_issues_created.json`

## 📋 Issues que Serão Criadas

- **P0 (Crítico):** 8 issues
- **P1 (Importante):** 15 issues  
- **P2 (Melhorias):** 24 issues

**Total:** 47 issues

## ✅ Resultado Esperado

```
🚀 Enviando issues para o Linear...

✅ Usando Team ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

📋 Obtendo/criando labels...
✅ 24 labels disponíveis

📖 Lendo arquivo LINEAR_ISSUES.md...
✅ 47 issues encontradas

📝 Criando issues no Linear...

Criando L-001: Observabilidade Incompleta...
  ✅ Criada: IA-TEST-1 - https://linear.app/...

...

============================================================
✅ 47 issues criadas com sucesso
============================================================

📄 Resultado salvo em: linear_issues_created.json
```

## 🔗 Links

- **API Key:** https://linear.app/settings/api
- **Linear API Docs:** https://developers.linear.app/docs/graphql
- **Guia Rápido:** `GUIA_RAPIDO_LINEAR.md`

## ❓ Problemas?

### "LINEAR_API_KEY não configurada"
- Execute: `python scripts/setup_linear.py`
- Ou adicione manualmente ao `.env`

### "Não foi possível obter o Team ID"
- Configure `LINEAR_TEAM_ID` no `.env`
- Ou certifique-se de ter acesso a um time no Linear

### Erro de autenticação
- Verifique se a API key está correta
- Certifique-se de que não expirou
- Verifique permissões

---

**Pronto para começar?** Execute:
```bash
python scripts/setup_linear.py
```

