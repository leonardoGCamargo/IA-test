"""
Script para organizar o projeto em estrutura profissional.
Move arquivos para pastas apropriadas e remove arquivos inúteis.
"""

import os
import shutil
from pathlib import Path

def criar_estrutura():
    """Cria a estrutura de pastas do projeto."""
    estrutura = {
        # Agentes e código principal
        "src/agents": [
            "orchestrator.py",
            "kestra_langchain_master.py",
            "agent_helper_system.py",
            "mcp_manager.py",
            "mcp_manager_ui.py",
            "mcp_docker_integration.py",
            "mcp_neo4j_integration.py",
            "mcp_obsidian_integration.py",
            "mcp_kestra_integration.py",
        ],
        # Aplicações existentes
        "src/apps": [
            "bot.py",
            "loader.py",
            "pdf_bot.py",
            "api.py",
            "chains.py",
            "utils.py",
        ],
        # Scripts utilitários
        "scripts": [
            "master_demo.py",
            "sync_obsidian_docs.py",
            "verificar_integracao_obsidian.py",
        ],
        # Documentação Obsidian
        "Obsidian_guardar aqui": [
            "00-MAPA-DE-AGENTES.md",
            "01-Guia-Obsidian.md",
            "02-Guia-Cursor.md",
            "03-Manual-Sistema-Agentes.md",
            "04-Como-Criar-Agentes.md",
            "RESUMO-MAPA-AGENTES.md",
            "OBSIDIAN-MCP-INTEGRATION.md",
            "README_SYNC_OBSIDIAN.md",
            "Agentes/",
        ],
        # Documentação geral
        "docs": [
            "ARCHITECTURE.md",
            "EXECUTION_PLAN.md",
            "ORCHESTRATOR_SUMMARY.md",
            "SURPRISE_PROJECT.md",
            "MASTER_AGENT_README.md",
            "MCP_README.md",
            "MCP_ARCHITECTURE.md",
            "DOCKER_INTEGRATION_README.md",
        ],
        # Docker files
        "docker": [
            "api.Dockerfile",
            "bot.Dockerfile",
            "loader.Dockerfile",
            "pdf_bot.Dockerfile",
            "front-end.Dockerfile",
            "pull_model.Dockerfile",
            "mcp_manager.Dockerfile",
            "mcp_docker_integration.Dockerfile",
        ],
        # Exemplos (manter)
        "examples": [
            "example_docker_agent_usage.py",
        ],
        # Configuração
        "config": [
            "env.example",
            "docker-compose.yml",
            "requirements.txt",
        ],
    }
    return estrutura

def mover_arquivo(origem: Path, destino: Path):
    """Move arquivo criando diretório se necessário."""
    try:
        destino.parent.mkdir(parents=True, exist_ok=True)
        if origem.exists():
            if destino.exists():
                print(f"⚠️  Arquivo já existe: {destino.name} (sobrescrevendo)")
            shutil.move(str(origem), str(destino))
            print(f"✅ Movido: {origem.name} → {destino.parent.name}/{destino.name}")
            return True
        else:
            print(f"⚠️  Arquivo não encontrado: {origem}")
            return False
    except Exception as e:
        print(f"❌ Erro ao mover {origem.name}: {e}")
        return False

def mover_pasta(origem: Path, destino: Path):
    """Move pasta completa."""
    try:
        destino.parent.mkdir(parents=True, exist_ok=True)
        if origem.exists():
            if destino.exists():
                print(f"⚠️  Pasta já existe: {destino.name} (mesclando)")
                # Move arquivos dentro da pasta
                for item in origem.iterdir():
                    item_dest = destino / item.name
                    if item.is_dir():
                        mover_pasta(item, item_dest)
                    else:
                        mover_arquivo(item, item_dest)
                # Remove pasta origem se vazia
                try:
                    origem.rmdir()
                except:
                    pass
            else:
                shutil.move(str(origem), str(destino))
                print(f"✅ Movido: {origem.name} → {destino.parent.name}/{destino.name}")
            return True
        else:
            print(f"⚠️  Pasta não encontrada: {origem}")
            return False
    except Exception as e:
        print(f"❌ Erro ao mover pasta {origem.name}: {e}")
        return False

def limpar_arquivos_temporarios():
    """Remove arquivos temporários e inúteis."""
    arquivos_para_remover = [
        "criar_notas_obsidian.py",  # Substituído por sync_obsidian_docs.py
        "__pycache__/",
        "*.pyc",
        "*.pyo",
        ".DS_Store",
    ]
    
    removidos = 0
    for item in arquivos_para_remover:
        if "*" in item:
            continue  # Ignora padrões com wildcards
        path = Path(item)
        if path.exists():
            try:
                if path.is_dir():
                    shutil.rmtree(path)
                else:
                    path.unlink()
                print(f"🗑️  Removido: {item}")
                removidos += 1
            except Exception as e:
                print(f"⚠️  Erro ao remover {item}: {e}")
    
    return removidos

def main():
    print("\n" + "="*70)
    print("📁 ORGANIZAÇÃO DO PROJETO - ESTRUTURA PROFISSIONAL")
    print("="*70)
    
    # Cria estrutura
    estrutura = criar_estrutura()
    base_path = Path(".")
    
    # Cria todas as pastas
    print("\n📂 Criando estrutura de pastas...")
    for pasta, _ in estrutura.items():
        pasta_path = base_path / pasta
        pasta_path.mkdir(parents=True, exist_ok=True)
        print(f"✅ Pasta criada: {pasta}")
    
    # Move arquivos
    print("\n📦 Movendo arquivos...")
    movidos = 0
    falhas = 0
    
    for pasta_destino, arquivos in estrutura.items():
        print(f"\n📁 Movendo para {pasta_destino}/...")
        for arquivo in arquivos:
            origem = base_path / arquivo
            destino = base_path / pasta_destino / arquivo
            
            if arquivo.endswith("/"):
                # É uma pasta
                pasta_nome = arquivo.rstrip("/")
                origem = base_path / pasta_nome
                destino = base_path / pasta_destino / pasta_nome
                if mover_pasta(origem, destino):
                    movidos += 1
                else:
                    falhas += 1
            else:
                # É um arquivo
                if mover_arquivo(origem, destino):
                    movidos += 1
                else:
                    falhas += 1
    
    # Limpa arquivos temporários
    print("\n🧹 Limpando arquivos temporários...")
    removidos = limpar_arquivos_temporarios()
    
    # Cria README na raiz explicando estrutura
    readme_conteudo = """# 📁 Estrutura do Projeto

## 📂 Organização

```
projeto/
├── src/
│   ├── agents/          # Agentes principais
│   │   ├── orchestrator.py
│   │   ├── kestra_langchain_master.py
│   │   ├── agent_helper_system.py
│   │   ├── mcp_manager.py
│   │   └── ...
│   └── apps/            # Aplicações existentes
│       ├── bot.py
│       ├── loader.py
│       ├── pdf_bot.py
│       └── api.py
├── scripts/             # Scripts utilitários
│   ├── master_demo.py
│   ├── sync_obsidian_docs.py
│   └── verificar_integracao_obsidian.py
├── docs/                # Documentação geral
│   ├── ARCHITECTURE.md
│   ├── EXECUTION_PLAN.md
│   └── ...
├── Obsidian_guardar aqui/  # Documentação Obsidian
│   ├── 00-MAPA-DE-AGENTES.md
│   ├── Agentes/
│   └── ...
├── docker/              # Dockerfiles
├── examples/            # Exemplos
├── config/              # Configurações
└── front-end/           # Frontend (Svelte)
```

## 🚀 Início Rápido

### 1. Configuração
```bash
cd config
cp env.example .env
# Edite o .env com suas configurações
```

### 2. Instalar Dependências
```bash
pip install -r config/requirements.txt
```

### 3. Iniciar Sistema
```bash
docker compose -f config/docker-compose.yml up
```

## 📚 Documentação

- **Mapa de Agentes**: `Obsidian_guardar aqui/00-MAPA-DE-AGENTES.md`
- **Arquitetura**: `docs/ARCHITECTURE.md`
- **Guia do Obsidian**: `Obsidian_guardar aqui/01-Guia-Obsidian.md`

## 🤖 Agentes

Ver `src/agents/` para código dos agentes.

## 📝 Scripts

Ver `scripts/` para scripts utilitários.

---
**Estrutura organizada para fácil navegação e manutenção**
"""
    
    with open("README_ESTRUTURA.md", "w", encoding="utf-8") as f:
        f.write(readme_conteudo)
    print("\n✅ README_ESTRUTURA.md criado")
    
    print("\n" + "="*70)
    print("✅ ORGANIZAÇÃO CONCLUÍDA")
    print("="*70)
    print(f"📦 {movidos} arquivos/pastas movidos")
    print(f"🗑️  {removidos} arquivos temporários removidos")
    if falhas > 0:
        print(f"⚠️  {falhas} itens não encontrados (normal)")
    print("\n💡 Verifique a nova estrutura e ajuste conforme necessário!")

if __name__ == "__main__":
    main()

