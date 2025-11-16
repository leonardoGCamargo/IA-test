#!/usr/bin/env python3
"""
Script para mapear toda a estrutura do projeto no Obsidian.
Cria notas organizadas com links e estrutura completa.
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from dotenv import load_dotenv

# Adiciona o diretório raiz ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.agents.mcp_obsidian_integration import ObsidianManager

# Carrega .env
load_dotenv()

def get_project_structure(root: Path) -> Dict:
    """Mapeia a estrutura completa do projeto."""
    structure = {
        "root": str(root),
        "folders": {},
        "files": {},
        "agents": [],
        "apps": [],
        "docs": [],
        "scripts": [],
        "configs": [],
    }
    
    # Mapeia pastas principais
    main_folders = ["src", "docs", "scripts", "config", "docker", "examples", "front-end"]
    for folder in main_folders:
        folder_path = root / folder
        if folder_path.exists():
            structure["folders"][folder] = {
                "path": str(folder_path),
                "files": list_files_recursive(folder_path),
            }
    
    # Mapeia agentes
    agents_path = root / "src" / "agents"
    if agents_path.exists():
        for agent_file in agents_path.glob("*.py"):
            if agent_file.name != "__init__.py":
                structure["agents"].append({
                    "name": agent_file.stem,
                    "path": str(agent_file),
                    "module": f"src.agents.{agent_file.stem}",
                })
    
    # Mapeia apps
    apps_path = root / "src" / "apps"
    if apps_path.exists():
        for app_file in apps_path.glob("*.py"):
            if app_file.name != "__init__.py":
                structure["apps"].append({
                    "name": app_file.stem,
                    "path": str(app_file),
                    "module": f"src.apps.{app_file.stem}",
                })
    
    # Mapeia documentação
    docs_path = root / "docs"
    if docs_path.exists():
        for doc_file in docs_path.glob("*.md"):
            structure["docs"].append({
                "name": doc_file.stem,
                "path": str(doc_file),
                "title": doc_file.stem.replace("_", " ").replace("-", " ").title(),
            })
    
    # Mapeia scripts
    scripts_path = root / "scripts"
    if scripts_path.exists():
        for script_file in scripts_path.glob("*.py"):
            structure["scripts"].append({
                "name": script_file.stem,
                "path": str(script_file),
            })
    
    return structure

def list_files_recursive(path: Path) -> List[Dict]:
    """Lista arquivos recursivamente."""
    files = []
    for item in path.rglob("*"):
        if item.is_file() and not item.name.startswith("."):
            files.append({
                "name": item.name,
                "path": str(item),
                "relative": str(item.relative_to(path)),
            })
    return files

def create_project_map_note(obsidian: ObsidianManager, structure: Dict) -> str:
    """Cria nota principal com mapa do projeto."""
    content = f"""# 🗺️ Mapa Completo do Projeto IA-Test

> **Última atualização:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 📋 Visão Geral

Este é o mapa completo da estrutura do projeto IA-Test, incluindo todos os agentes, aplicações, documentação e scripts.

## 📁 Estrutura de Pastas

```
{structure['root']}
├── src/
│   ├── agents/          # Agentes especializados
│   └── apps/            # Aplicações principais
├── docs/                # Documentação técnica
├── scripts/             # Scripts utilitários
├── config/              # Configurações
├── docker/              # Dockerfiles
├── front-end/           # Front-end Svelte
└── examples/            # Exemplos de uso
```

## 🤖 Agentes ({len(structure['agents'])})

"""
    
    for agent in structure["agents"]:
        agent_name = agent["name"].replace("_", "-").title()
        content += f"- [[{agent_name}]] - `{agent['module']}`\n"
    
    content += f"""
## 📱 Aplicações ({len(structure['apps'])})

"""
    
    for app in structure["apps"]:
        app_name = app["name"].replace("_", "-").title()
        content += f"- [[{app_name}]] - `{app['module']}`\n"
    
    content += f"""
## 📚 Documentação ({len(structure['docs'])})

"""
    
    for doc in structure["docs"]:
        doc_name = doc["title"]
        content += f"- [[{doc_name}]]\n"
    
    content += f"""
## 🔧 Scripts ({len(structure['scripts'])})

"""
    
    for script in structure["scripts"]:
        script_name = script["name"].replace("_", "-").title()
        content += f"- `{script['name']}.py`\n"
    
    content += """
## 🔗 Links Rápidos

- [[00-MAPA-DE-AGENTES]] - Mapa detalhado dos agentes
- [[01-Guia-Obsidian]] - Guia de uso do Obsidian
- [[02-Guia-Cursor]] - Guia de uso do Cursor
- [[03-Manual-Sistema-Agentes]] - Manual completo do sistema

## 📝 Notas

- Este mapa é gerado automaticamente
- Use os links para navegar entre as notas
- Atualize este mapa quando adicionar novos componentes
"""
    
    return content

def create_agent_notes(obsidian: ObsidianManager, agents: List[Dict], root: Path):
    """Cria notas individuais para cada agente."""
    for agent in agents:
        agent_name = agent["name"].replace("_", "-").title()
        agent_file = Path(agent["path"])
        
        # Lê o arquivo do agente
        try:
            with open(agent_file, "r", encoding="utf-8") as f:
                agent_code = f.read()
        except Exception as e:
            print(f"⚠️  Erro ao ler {agent_file}: {e}")
            continue
        
        # Extrai docstring
        docstring = ""
        if '"""' in agent_code:
            parts = agent_code.split('"""')
            if len(parts) > 1:
                docstring = parts[1].strip()
        
        # Cria conteúdo da nota
        content = f"""# 🤖 {agent_name}

> **Módulo:** `{agent['module']}`  
> **Arquivo:** `{agent['path']}`

## 📝 Descrição

{docstring if docstring else "Documentação do agente."}

## 🔗 Links

- [[00-MAPA-DE-AGENTES]] - Voltar ao mapa principal
- [[MAPA-PROJETO]] - Mapa completo do projeto

## 📂 Estrutura

```python
{agent['module']}
```

## 📝 Notas

- Adicione suas notas sobre este agente aqui
- Use links para conectar com outros agentes
"""
        
        # Cria nota
        try:
            obsidian.create_note(agent_name, content, folder="Agentes")
            print(f"✅ Nota criada: Agentes/{agent_name}.md")
        except Exception as e:
            print(f"❌ Erro ao criar nota {agent_name}: {e}")

def create_docs_index(obsidian: ObsidianManager, docs: List[Dict]):
    """Cria índice da documentação."""
    content = """# 📚 Índice da Documentação

> Documentação técnica completa do projeto

## 📖 Documentos Disponíveis

"""
    
    for doc in docs:
        doc_name = doc["title"]
        content += f"- [[{doc_name}]]\n"
    
    content += """
## 🔗 Links

- [[MAPA-PROJETO]] - Mapa completo do projeto
- [[00-MAPA-DE-AGENTES]] - Mapa dos agentes
"""
    
    try:
        obsidian.create_note("Índice-Documentação", content, folder="")
        print("✅ Índice de documentação criado")
    except Exception as e:
        print(f"❌ Erro ao criar índice: {e}")

def main():
    print("="*70)
    print("🗺️  MAPEAMENTO COMPLETO DO PROJETO NO OBSIDIAN")
    print("="*70)
    
    # Detecta vault
    vault_path = os.getenv("OBSIDIAN_VAULT_PATH")
    if not vault_path:
        vault_path = input("Caminho do vault Obsidian: ").strip().strip('"')
    
    if not vault_path or not Path(vault_path).exists():
        print("❌ Vault não encontrado")
        return
    
    # Inicializa Obsidian Manager
    obsidian = ObsidianManager()
    if not obsidian.set_vault_path(vault_path):
        print("❌ Erro ao configurar vault")
        return
    
    print(f"✅ Vault configurado: {vault_path}\n")
    
    # Mapeia estrutura
    print("📁 Mapeando estrutura do projeto...")
    root = Path(__file__).parent.parent
    structure = get_project_structure(root)
    
    print(f"✅ Encontrados:")
    print(f"   - {len(structure['agents'])} agentes")
    print(f"   - {len(structure['apps'])} aplicações")
    print(f"   - {len(structure['docs'])} documentos")
    print(f"   - {len(structure['scripts'])} scripts\n")
    
    # Cria nota principal
    print("📝 Criando nota principal do projeto...")
    map_content = create_project_map_note(obsidian, structure)
    try:
        obsidian.create_note("MAPA-PROJETO", map_content, folder="")
        print("✅ Nota principal criada: MAPA-PROJETO.md\n")
    except Exception as e:
        print(f"❌ Erro ao criar nota principal: {e}\n")
    
    # Cria notas dos agentes
    print("🤖 Criando notas dos agentes...")
    create_agent_notes(obsidian, structure["agents"], root)
    print()
    
    # Cria índice de documentação
    print("📚 Criando índice de documentação...")
    create_docs_index(obsidian, structure["docs"])
    print()
    
    print("="*70)
    print("✅ MAPEAMENTO CONCLUÍDO!")
    print("="*70)
    print(f"\n📁 Vault: {vault_path}")
    print("💡 Abra o Obsidian para ver o mapeamento completo!")

if __name__ == "__main__":
    main()

