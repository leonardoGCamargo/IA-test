# 📋 Como Enviar Issues para o Linear

## 🔑 Configuração

### 1. Obter API Key do Linear

1. Acesse: https://linear.app/settings/api
2. Clique em "Create API Key"
3. Copie a chave gerada

### 2. Obter Team ID

**Opção 1: Via Script (Automático)**
- O script tentará obter automaticamente o primeiro time disponível

**Opção 2: Manual**
1. Acesse o Linear
2. Vá em Settings → Teams
3. Copie o ID do time (ou use a key do time, ex: "IA-TEST")

### 3. Configurar Variáveis de Ambiente

Adicione ao `.env`:

```bash
# Linear API
LINEAR_API_KEY=lin_api_xxxxxxxxxxxxx
LINEAR_TEAM_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx  # Opcional
LINEAR_PROJECT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx  # Opcional
```

## 🚀 Executar

```bash
python scripts/send_issues_to_linear.py
```

## 📋 O que o Script Faz

1. ✅ Verifica configuração (API key, Team ID)
2. ✅ Obtém/cria labels necessárias
3. ✅ Lê `LINEAR_ISSUES.md`
4. ✅ Cria todas as 47 issues no Linear
5. ✅ Salva resultado em `linear_issues_created.json`

## 📊 Resultado

O script criará:
- **47 issues** no Linear
- **Labels** automaticamente criadas se não existirem
- **Arquivo JSON** com links das issues criadas

## 🔗 Links Úteis

- **Linear API Docs:** https://developers.linear.app/docs/graphql
- **API Key:** https://linear.app/settings/api
- **Issues Format:** `LINEAR_ISSUES.md`

