#!/usr/bin/env python3
"""
Script final para completar a organização e criar mapeamento Obsidian completo.
"""

import os
import shutil
import json
from pathlib import Path
from datetime import datetime

def get_project_root() -> Path:
    """Obtém a raiz do projeto."""
    current = Path(__file__).resolve()
    # Se estamos em IA-test/scripts/, a raiz é o pai
    if current.parent.name == "scripts" and current.parent.parent.name == "IA-test":
        return current.parent.parent
    # Caso contrário, procura
    while current.parent != current:
        if current.name == "IA-test" and (current / "src").exists():
            return current
        current = current.parent
    return Path(__file__).parent.parent

def move_remaining_files(root: Path):
    """Move arquivos restantes da pasta IA-test/IA-test/."""
    ia_test_sub = root / "IA-test"
    
    if not ia_test_sub.exists():
        return
    
    print("Movendo arquivos restantes...")
    
    # Arquivos para mover
    files_to_move = {
        "CONTRIBUTING.md": "docs/CONTRIBUTING.md",
        "readme.md": "docs/README_LEGACY.md",
        "running_on_wsl.md": "docs/running_on_wsl.md",
        "install_ollama.sh": "scripts/install_ollama.sh",
    }
    
    for source_name, dest_name in files_to_move.items():
        source = ia_test_sub / source_name
        dest = root / dest_name
        
        if source.exists() and source.is_file():
            try:
                dest.parent.mkdir(parents=True, exist_ok=True)
                if dest.exists():
                    if source.read_bytes() != dest.read_bytes():
                        backup = dest.with_suffix(dest.suffix + ".backup")
                        shutil.copy2(dest, backup)
                shutil.move(str(source), str(dest))
                print(f"  ✅ Movido: {source_name} -> {dest_name}")
            except Exception as e:
                print(f"  ❌ Erro ao mover {source_name}: {e}")
    
    # Move .dockerignore, .gitignore se não existirem na raiz
    for dotfile in [".dockerignore", ".gitignore"]:
        source = ia_test_sub / dotfile
        dest = root / dotfile
        
        if source.exists() and not dest.exists():
            try:
                shutil.move(str(source), str(dest))
                print(f"  ✅ Movido: {dotfile}")
            except Exception as e:
                print(f"  ❌ Erro ao mover {dotfile}: {e}")

def create_complete_obsidian_mapping(root: Path):
    """Cria mapeamento completo para Obsidian."""
    print("\nCriando mapeamento completo para Obsidian...")
    
    obsidian_dir = root / "Obsidian_guardar aqui"
    obsidian_dir.mkdir(exist_ok=True)
    
    # Mapeia estrutura completa
    structure = {
        "agents": [],
        "apps": [],
        "docs": [],
        "scripts": [],
        "dockerfiles": [],
        "configs": [],
    }
    
    # Mapeia agentes
    agents_dir = root / "src" / "agents"
    if agents_dir.exists():
        for agent_file in sorted(agents_dir.glob("*.py")):
            if agent_file.name != "__init__.py":
                structure["agents"].append({
                    "name": agent_file.stem,
                    "file": str(agent_file.relative_to(root)),
                    "module": f"src.agents.{agent_file.stem}",
                })
    
    # Mapeia apps
    apps_dir = root / "src" / "apps"
    if apps_dir.exists():
        for app_file in sorted(apps_dir.glob("*.py")):
            if app_file.name != "__init__.py":
                structure["apps"].append({
                    "name": app_file.stem,
                    "file": str(app_file.relative_to(root)),
                    "module": f"src.apps.{app_file.stem}",
                })
    
    # Mapeia docs
    docs_dir = root / "docs"
    if docs_dir.exists():
        for doc_file in sorted(docs_dir.glob("*.md")):
            structure["docs"].append({
                "name": doc_file.stem,
                "file": str(doc_file.relative_to(root)),
                "title": doc_file.stem.replace("_", " ").replace("-", " ").title(),
            })
    
    # Mapeia scripts
    scripts_dir = root / "scripts"
    if scripts_dir.exists():
        for script_file in sorted(scripts_dir.glob("*.py")):
            structure["scripts"].append({
                "name": script_file.stem,
                "file": str(script_file.relative_to(root)),
            })
    
    # Mapeia dockerfiles
    docker_dir = root / "docker"
    if docker_dir.exists():
        for dockerfile in sorted(docker_dir.glob("*.Dockerfile")):
            structure["dockerfiles"].append({
                "name": dockerfile.stem,
                "file": str(dockerfile.relative_to(root)),
            })
    
    # Cria nota principal atualizada
    note_content = f"""# 🏗️ Projeto IA-Test - Mapeamento Completo

> **Última atualização:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 📋 Visão Geral

Este é o mapeamento completo do projeto IA-Test, incluindo todos os componentes, agentes, aplicações e documentação.

## 🤖 Agentes ({len(structure['agents'])})

"""
    
    for agent in structure["agents"]:
        agent_name = agent["name"].replace("_", "-").title()
        note_content += f"- [[{agent_name}]] - `{agent['module']}`\n"
        note_content += f"  - Arquivo: `{agent['file']}`\n"
    
    note_content += f"""
## 📱 Aplicações ({len(structure['apps'])})

"""
    
    for app in structure["apps"]:
        app_name = app["name"].replace("_", "-").title()
        note_content += f"- [[{app_name}]] - `{app['module']}`\n"
        note_content += f"  - Arquivo: `{app['file']}`\n"
    
    note_content += f"""
## 📚 Documentação ({len(structure['docs'])})

"""
    
    for doc in structure["docs"]:
        doc_name = doc["title"]
        note_content += f"- [[{doc_name}]] - `{doc['file']}`\n"
    
    note_content += f"""
## 🔧 Scripts ({len(structure['scripts'])})

"""
    
    for script in structure["scripts"]:
        script_name = script["name"].replace("_", "-").title()
        note_content += f"- `{script['name']}.py` - `{script['file']}`\n"
    
    note_content += f"""
## 🐳 Dockerfiles ({len(structure['dockerfiles'])})

"""
    
    for dockerfile in structure["dockerfiles"]:
        note_content += f"- `{dockerfile['name']}` - `{dockerfile['file']}`\n"
    
    note_content += """
## 🔗 Links Úteis

- [[00-MAPA-DE-AGENTES]] - Mapa detalhado dos agentes
- [[01-Guia-Obsidian]] - Guia de uso do Obsidian
- [[02-Guia-Cursor]] - Guia de uso do Cursor
- [[03-Manual-Sistema-Agentes]] - Manual completo do sistema

## 📊 Estatísticas

- **Total de Agentes:** """ + str(len(structure['agents'])) + """
- **Total de Aplicações:** """ + str(len(structure['apps'])) + """
- **Total de Documentos:** """ + str(len(structure['docs'])) + """
- **Total de Scripts:** """ + str(len(structure['scripts'])) + """
- **Total de Dockerfiles:** """ + str(len(structure['dockerfiles'])) + """

---
*Última atualização: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "*"
"""
    
    note_file = obsidian_dir / "PROJETO-IA-TEST.md"
    note_file.write_text(note_content, encoding="utf-8")
    
    print(f"  ✅ Nota atualizada: {note_file.relative_to(root)}")
    
    # Salva JSON atualizado
    mapping_file = obsidian_dir / "project_mapping.json"
    with open(mapping_file, "w", encoding="utf-8") as f:
        json.dump({
            "project_name": "IA-Test",
            "created_at": datetime.now().isoformat(),
            "structure": structure,
        }, f, indent=2, ensure_ascii=False)
    
    print(f"  ✅ Mapeamento JSON atualizado: {mapping_file.relative_to(root)}")

def main():
    root = get_project_root()
    print(f"Raiz do projeto: {root}")
    
    # Move arquivos restantes
    move_remaining_files(root)
    
    # Cria mapeamento completo
    create_complete_obsidian_mapping(root)
    
    print("\n✅ Organização finalizada!")

if __name__ == "__main__":
    main()

