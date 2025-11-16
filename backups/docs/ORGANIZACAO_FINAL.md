# 📁 Organização Final do Projeto

## Data: 2025-01-27

## Estrutura Recomendada

Após análise, a estrutura final recomendada é:

```
IA-test/
├── src/
│   ├── agents/          # Todos os agentes
│   └── apps/            # Aplicações principais
├── front-end/           # Front-end Svelte (manter na raiz)
├── docker/              # Todos os Dockerfiles
├── config/              # Configurações (docker-compose.yml, env.example, requirements.txt)
├── docs/                # Documentação técnica
├── scripts/             # Scripts utilitários
├── examples/            # Exemplos de uso
├── embedding_model/     # Modelos de embedding (manter na raiz)
├── images/              # Imagens (manter na raiz)
├── Obsidian_guardar aqui/  # Documentação Obsidian
└── README.md            # README principal
```

## Ações Necessárias

### 1. Consolidar Pasta IA-test/IA-test/

A pasta `IA-test/IA-test/` contém a estrutura organizada. Devemos:

1. **Mover conteúdo de `IA-test/IA-test/` para a raiz:**
   - `IA-test/IA-test/docker/` → `IA-test/docker/`
   - `IA-test/IA-test/config/` → `IA-test/config/`
   - `IA-test/IA-test/docs/` → `IA-test/docs/`
   - `IA-test/IA-test/scripts/` → `IA-test/scripts/`
   - `IA-test/IA-test/src/` → `IA-test/src/`
   - `IA-test/IA-test/examples/` → `IA-test/examples/`

2. **Remover duplicações:**
   - Remover `IA-test/IA-test/front-end/` (manter na raiz)
   - Remover `IA-test/IA-test/embedding_model/` (manter na raiz)
   - Remover `IA-test/IA-test/images/` (manter na raiz se já existir)

3. **Mover arquivos da raiz:**
   - `api.py`, `bot.py`, etc. → `src/apps/` (se não existirem)
   - Dockerfiles da raiz → `docker/` (se não existirem)
   - `docker-compose.yml` → `config/` (se não existir)
   - `requirements.txt` → `config/` (se não existir)
   - `env.example` → `config/` (se não existir)

### 2. Remover Pasta IA-test/IA-test/

Após consolidar tudo, remover a pasta `IA-test/IA-test/`.

## Script de Organização

Execute o script `scripts/organize_project.py` para fazer a organização automaticamente.

## Mapeamento Obsidian

Após organizar, execute `scripts/map_to_obsidian.py` para criar o mapeamento completo no Obsidian.

