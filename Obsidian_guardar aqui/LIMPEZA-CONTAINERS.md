# 🧹 Limpeza de Containers Docker

> **Data:** 2025-01-27  
> **Status:** ✅ Limpeza executada

---

## 📊 SITUAÇÃO INICIAL

- **Total de containers:** 57
- **Rodando:** 50
- **Parados:** 7
- **Do projeto IA-Test:** 2 (parados)

---

## ✅ AÇÕES EXECUTADAS

### 1. Containers Parados Removidos
- ✅ Removidos containers com status "Exited"
- ✅ Removidos containers com status "Created"

### 2. Containers do Projeto Otimizados
- ✅ Parados containers desnecessários
- ✅ Mantidos apenas essenciais:
  - Neo4j
  - Agent Dashboard
  - API

### 3. Imagens Não Utilizadas
- ✅ Limpeza de imagens órfãs
- ✅ Liberação de espaço em disco

### 4. Volumes Não Utilizados
- ✅ Limpeza de volumes órfãos

---

## 📋 CONTAINERS ESSENCIAIS DO PROJETO

### Devem Continuar Rodando
1. **ia-test-neo4j** - Banco de dados Neo4j
2. **ia-test-agent-dashboard** - Dashboard Streamlit
3. **ia-test-api** - API FastAPI

### Podem Ser Parados (usar profiles)
- `bot`, `loader`, `pdf_bot` (profile: streamlit)
- `mcp-manager` (profile: tools)
- `kestra` (profile: tools)
- `ollama` (profile: ollama)

---

## 🎯 COMO USAR PROFILES

### Iniciar apenas serviços essenciais
```bash
docker compose --profile core up
```

### Iniciar com Streamlit apps
```bash
docker compose --profile core --profile streamlit up
```

### Iniciar com ferramentas
```bash
docker compose --profile core --profile tools up
```

### Parar tudo
```bash
docker compose down
```

---

## 📊 RESULTADO

### Antes
- 57 containers
- 50 rodando
- 7 parados

### Depois
- Redução significativa
- Apenas containers essenciais rodando
- Sistema mais limpo

---

## 🔧 SCRIPTS CRIADOS

1. **`scripts/analisar_containers.py`** - Analisa containers
2. **`scripts/limpar_containers_automatico.py`** - Limpeza automática
3. **`scripts/limpar_containers.ps1`** - Script PowerShell

---

## 💡 DICAS

### Ver containers rodando
```bash
docker ps
```

### Ver todos os containers
```bash
docker ps -a
```

### Parar container específico
```bash
docker stop <nome>
```

### Remover container
```bash
docker rm <nome>
```

### Limpar tudo (cuidado!)
```bash
docker system prune -a
```

---

## 🔗 Links Relacionados

- [[PROJETO-IA-TEST|Projeto Principal]]
- [[SISTEMA-OTIMIZADO-FINAL|Sistema Otimizado]]

---

## 🏷️ Tags

#docker #containers #limpeza #otimizacao

---

**Última atualização:** 2025-01-27

