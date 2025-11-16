# 🔗 Git Integration Agent - Documentação

> **Agente para gerenciamento de Git e GitHub**

## 📋 Visão Geral

O **Git Integration Agent** fornece integração completa com Git e GitHub, permitindo gerenciar repositórios, fazer commits, push, pull e sincronizar automaticamente com GitHub.

## 🚀 Recursos

- ✅ **Status do Repositório** - Verifica estado atual
- ✅ **Add/Commit** - Adiciona arquivos e cria commits
- ✅ **Push/Pull** - Sincroniza com GitHub
- ✅ **Branch Management** - Cria e gerencia branches
- ✅ **Tag Management** - Cria e gerencia tags
- ✅ **Remote Management** - Gerencia remotes
- ✅ **Commit History** - Visualiza histórico de commits

## 📚 Uso

### Importação

```python
from src.agents.git_integration import get_git_agent

git_agent = get_git_agent()
```

### Verificar Status

```python
status = git_agent.get_status()
print(f"Branch: {status.branch}")
print(f"Limpo: {status.is_clean}")
print(f"Arquivos modificados: {len(status.modified_files)}")
```

### Adicionar Arquivos

```python
# Adicionar arquivos específicos
git_agent.add_files(files=["arquivo1.py", "arquivo2.py"])

# Adicionar todos os arquivos
git_agent.add_files(all_files=True)
```

### Criar Commit

```python
git_agent.commit(
    message="Adiciona nova funcionalidade",
    author="Nome <email@exemplo.com>"  # opcional
)
```

### Push para GitHub

```python
# Push para branch atual
git_agent.push()

# Push para branch específica
git_agent.push(branch="main")

# Force push (cuidado!)
git_agent.push(force=True)
```

### Pull do GitHub

```python
# Pull da branch atual
git_agent.pull()

# Pull de branch específica
git_agent.pull(branch="main")
```

### Criar Branch

```python
# Criar e fazer checkout
git_agent.create_branch("nova-feature", checkout=True)

# Apenas criar
git_agent.create_branch("nova-feature", checkout=False)
```

### Checkout de Branch

```python
git_agent.checkout("main")
```

### Criar Tag

```python
# Tag simples
git_agent.tag("v1.0.0")

# Tag com mensagem
git_agent.tag("v1.0.0", message="Release v1.0.0")

# Tag e push
git_agent.tag("v1.0.0", message="Release v1.0.0", push=True)
```

### Ver Commits Recentes

```python
commits = git_agent.get_recent_commits(limit=10)
for commit in commits:
    print(f"{commit.hash} - {commit.message} - {commit.author}")
```

### Ver Remotes

```python
remotes = git_agent.get_remotes()
print(remotes)  # {'origin': 'https://github.com/user/repo.git'}
```

## 🔧 Integração com Orchestrator

### Via Orchestrator

```python
from src.agents import get_orchestrator, AgentType

orchestrator = get_orchestrator()

# Criar tarefa Git
task = orchestrator.create_task(
    AgentType.GIT_INTEGRATION,
    "Verificar status do repositório",
    {"action": "status"}
)

# Executar
result = orchestrator.execute_task(task)
```

### Ações Disponíveis

| Ação | Descrição | Parâmetros |
|------|-----------|------------|
| `status` | Verifica status | - |
| `add` | Adiciona arquivos | `files` (lista) ou `all_files` (bool) |
| `commit` | Cria commit | `message`, `author` (opcional) |
| `push` | Push para GitHub | `remote`, `branch`, `force` (opcional) |
| `pull` | Pull do GitHub | `remote`, `branch` (opcional) |
| `create_branch` | Cria branch | `branch_name`, `checkout` (opcional) |
| `checkout` | Checkout branch | `branch_name` |
| `tag` | Cria tag | `tag_name`, `message` (opcional), `push` (opcional) |
| `remotes` | Lista remotes | - |
| `recent_commits` | Commits recentes | `limit` (opcional, default: 10) |
| `full_sync` | Add + Commit + Push | `message`, `remote` (opcional) |

### Exemplo Completo

```python
# Via Orchestrator - Full Sync
task = orchestrator.create_task(
    AgentType.GIT_INTEGRATION,
    "Sincronizar repositório completo",
    {
        "action": "full_sync",
        "message": "Atualizações automáticas do sistema",
        "remote": "origin"
    }
)

result = orchestrator.execute_task(task)
```

## 📝 Scripts Utilitários

### `scripts/git_sync_simple.py`

Script simples para sincronizar repositório:

```bash
python scripts/git_sync_simple.py
```

Este script:
1. Verifica status do Git
2. Adiciona todas as mudanças
3. Cria commit
4. Faz push para GitHub

### `scripts/git_sync.py`

Script completo usando o Git Agent:

```bash
python scripts/git_sync.py
```

## 🏗️ Arquitetura

### Classes Principais

- **`GitIntegrationAgent`**: Classe principal do agente
- **`GitStatus`**: Dataclass para status do repositório
- **`CommitInfo`**: Dataclass para informações de commit
- **`GitAction`**: Enum de ações disponíveis

### Métodos Principais

- `get_status()` - Obtém status do repositório
- `add_files()` - Adiciona arquivos ao staging
- `commit()` - Cria commit
- `push()` - Push para remoto
- `pull()` - Pull do remoto
- `create_branch()` - Cria branch
- `checkout()` - Checkout de branch
- `tag()` - Cria tag
- `get_remotes()` - Lista remotes
- `get_recent_commits()` - Commits recentes
- `execute_action()` - Executa ação genérica

## 🔒 Segurança

### Credenciais

O Git Agent usa as credenciais configuradas no Git local:
- **HTTPS**: Usa credenciais salvas ou prompt
- **SSH**: Usa chave SSH configurada

### Recomendações

1. **Não force push em branches principais** sem confirmação
2. **Valide commits** antes de fazer push
3. **Use branches** para features experimentais
4. **Configure .gitignore** adequadamente

## 📖 Exemplos

### Exemplo 1: Status Básico

```python
from src.agents import get_git_agent

git = get_git_agent()
status = git.get_status()

print(f"Branch: {status.branch}")
print(f"Limpo: {status.is_clean}")
```

### Exemplo 2: Commit Automático

```python
git = get_git_agent()

if not git.get_status().is_clean:
    git.add_files(all_files=True)
    git.commit("Atualizações automáticas")
    git.push()
```

### Exemplo 3: Criar Release

```python
git = get_git_agent()

# Criar tag de release
git.tag("v1.0.0", message="Release v1.0.0", push=True)

# Push para GitHub
git.push()
```

## 🔗 Referências

- [[../README|README Principal]]
- [[../src/agents/git_integration.py|Código do Agente]]
- [[ENGINEERING_GUIDE|Engineering Guide]]

## 🏷️ Tags

#git #github #integração #agente #documentação

---

**Última atualização:** {{date}}  
**Versão:** 1.0.0

