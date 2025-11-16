# 🚀 Guia Rápido - Enviar Issues para Linear

## 📋 Passo a Passo

### 1. Obter API Key do Linear

1. Acesse: **https://linear.app/settings/api**
2. Clique em **"Create API Key"**
3. Dê um nome (ex: "IA-Test Integration")
4. Copie a chave gerada (formato: `lin_api_xxxxxxxxxxxxx`)

### 2. Configurar

**Opção A: Script Interativo (Recomendado)**
```bash
python scripts/setup_linear.py
```

**Opção B: Manual**
Adicione ao `.env`:
```bash
LINEAR_API_KEY=lin_api_xxxxxxxxxxxxx
LINEAR_TEAM_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx  # Opcional
LINEAR_PROJECT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx  # Opcional
```

### 3. Enviar Issues

```bash
python scripts/send_issues_to_linear.py
```

## ✅ O que o Script Faz

1. ✅ Verifica API key
2. ✅ Obtém Team ID (se não configurado)
3. ✅ Cria labels automaticamente (se não existirem)
4. ✅ Lê `LINEAR_ISSUES.md`
5. ✅ Cria todas as 47 issues no Linear
6. ✅ Salva resultado em `linear_issues_created.json`

## 📊 Resultado Esperado

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

## 🔗 Links Úteis

- **API Key:** https://linear.app/settings/api
- **Linear API Docs:** https://developers.linear.app/docs/graphql
- **Issues Format:** `LINEAR_ISSUES.md`

## ❓ Troubleshooting

### "LINEAR_API_KEY não configurada"
- Execute `python scripts/setup_linear.py`
- Ou adicione manualmente ao `.env`

### "Não foi possível obter o Team ID"
- Configure `LINEAR_TEAM_ID` no `.env`
- Ou certifique-se de ter acesso a pelo menos um time no Linear

### Erro de autenticação
- Verifique se a API key está correta
- Certifique-se de que a API key não expirou
- Verifique permissões da API key

## 📝 Notas

- O script cria labels automaticamente se não existirem
- Issues são criadas com prioridades corretas (P0, P1, P2)
- Estimativas são convertidas para pontos (1 dia = 1 ponto)
- Todas as issues ficam no status "Todo"

---

**Pronto para começar?** Execute:
```bash
python scripts/setup_linear.py
```

