#!/usr/bin/env python3
"""
Script para organizar a estrutura do projeto e mapear para Obsidian.

Este script:
1. Consolida a pasta IA-test/IA-test/ para a raiz
2. Remove duplicações
3. Organiza a estrutura
4. Cria mapeamento para Obsidian
"""

import os
import shutil
import json
from pathlib import Path
from typing import Dict, List, Set
from datetime import datetime

# Cores para output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def print_colored(text: str, color: str = Colors.RESET):
    """Print com cor."""
    try:
        print(f"{color}{text}{Colors.RESET}")
    except UnicodeEncodeError:
        # Fallback para Windows sem suporte a emojis
        text_clean = text.encode('ascii', 'ignore').decode('ascii')
        print(f"{color}{text_clean}{Colors.RESET}")

def get_project_root() -> Path:
    """Obtém a raiz do projeto."""
    current = Path(__file__).resolve()
    # Sobe até encontrar a raiz (onde está IA-test/)
    while current.parent != current:
        if (current / "IA-test").exists() and (current / "IA-test" / "IA-test").exists():
            return current / "IA-test"
        current = current.parent
    # Fallback: assume que estamos em IA-test/scripts/
    return Path(__file__).parent.parent

def consolidate_ia_test_folder(root: Path, ia_test_sub: Path):
    """Consolida a pasta IA-test/IA-test/ para a raiz."""
    print_colored("\n📦 Consolidando pasta IA-test/IA-test/...", Colors.YELLOW)
    
    folders_to_move = {
        "docker": "docker",
        "config": "config",
        "docs": "docs",
        "scripts": "scripts",
        "src": "src",
        "examples": "examples",
    }
    
    files_to_move = {
        "GUIA_NAVEGACAO.md": "GUIA_NAVEGACAO.md",
        "CORRECOES_APLICADAS.md": "CORRECOES_APLICADAS.md",
        "README_DOCKER.md": "README_DOCKER.md",
        "readme.md": "readme.md",
        "RESUMO_GIT_AGENT.md": "RESUMO_GIT_AGENT.md",
        "running_on_wsl.md": "running_on_wsl.md",
        "install_ollama.sh": "install_ollama.sh",
        "LICENSE": "LICENSE",
    }
    
    moved = []
    skipped = []
    errors = []
    
    # Move pastas
    for source_name, dest_name in folders_to_move.items():
        source = ia_test_sub / source_name
        dest = root / dest_name
        
        if not source.exists():
            skipped.append(f"{source_name}/ (não existe)")
            continue
        
        try:
            if dest.exists():
                # Mescla conteúdo
                print_colored(f"  ⚠️  {dest_name}/ já existe, mesclando...", Colors.YELLOW)
                merge_directories(source, dest)
            else:
                # Move pasta inteira
                shutil.move(str(source), str(dest))
                print_colored(f"  ✅ Movido: {source_name}/ -> {dest_name}/", Colors.GREEN)
            
            moved.append(f"{source_name}/ -> {dest_name}/")
        except Exception as e:
            errors.append(f"{source_name}/: {str(e)}")
            print_colored(f"  ❌ Erro ao mover {source_name}/: {e}", Colors.RED)
    
    # Move arquivos
    for source_name, dest_name in files_to_move.items():
        source = ia_test_sub / source_name
        dest = root / dest_name
        
        if not source.exists():
            skipped.append(f"{source_name} (não existe)")
            continue
        
        try:
            if dest.exists():
                # Compara conteúdo
                if source.read_bytes() != dest.read_bytes():
                    # Backup do destino
                    backup = dest.with_suffix(dest.suffix + ".backup")
                    shutil.copy2(dest, backup)
                    print_colored(f"  ⚠️  Backup criado: {backup}", Colors.YELLOW)
                
                # Substitui se diferente
                if source.read_bytes() != dest.read_bytes():
                    shutil.copy2(source, dest)
                    print_colored(f"  ✅ Atualizado: {dest_name}", Colors.GREEN)
                else:
                    print_colored(f"  ⏭️  Ignorado (idêntico): {dest_name}", Colors.BLUE)
            else:
                shutil.move(str(source), str(dest))
                print_colored(f"  ✅ Movido: {source_name} -> {dest_name}", Colors.GREEN)
            
            moved.append(f"{source_name} -> {dest_name}")
        except Exception as e:
            errors.append(f"{source_name}: {str(e)}")
            print_colored(f"  ❌ Erro ao mover {source_name}: {e}", Colors.RED)
    
    # Remove duplicações
    duplicates_to_remove = ["front-end", "embedding_model"]
    for dup in duplicates_to_remove:
        dup_path = ia_test_sub / dup
        if dup_path.exists():
            try:
                shutil.rmtree(dup_path)
                print_colored(f"  🗑️  Removido duplicado: {dup}/", Colors.GREEN)
            except Exception as e:
                print_colored(f"  ❌ Erro ao remover {dup}/: {e}", Colors.RED)
    
    # Move Obsidian_guardar aqui se não existir na raiz
    obsidian_source = ia_test_sub / "Obsidian_guardar aqui"
    obsidian_dest = root / "Obsidian_guardar aqui"
    
    if obsidian_source.exists():
        if obsidian_dest.exists():
            # Mescla conteúdo
            print_colored(f"  ⚠️  Obsidian_guardar aqui/ já existe, mesclando...", Colors.YELLOW)
            merge_directories(obsidian_source, obsidian_dest)
        else:
            shutil.move(str(obsidian_source), str(obsidian_dest))
            print_colored(f"  ✅ Movido: Obsidian_guardar aqui/", Colors.GREEN)
    
    # Move images se não existir na raiz
    images_source = ia_test_sub / "images"
    images_dest = root / "images"
    
    if images_source.exists():
        if images_dest.exists():
            # Mescla conteúdo
            merge_directories(images_source, images_dest)
        else:
            shutil.move(str(images_source), str(images_dest))
            print_colored(f"  ✅ Movido: images/", Colors.GREEN)
    
    return moved, skipped, errors

def merge_directories(source: Path, dest: Path):
    """Mescla conteúdo de source em dest."""
    for item in source.iterdir():
        dest_item = dest / item.name
        
        if item.is_dir():
            if dest_item.exists():
                merge_directories(item, dest_item)
            else:
                shutil.move(str(item), str(dest_item))
        else:
            if dest_item.exists():
                # Compara e substitui se diferente
                if item.read_bytes() != dest_item.read_bytes():
                    backup = dest_item.with_suffix(dest_item.suffix + ".backup")
                    shutil.copy2(dest_item, backup)
                    shutil.copy2(item, dest_item)
                    print_colored(f"    ✅ Atualizado: {item.name}", Colors.GREEN)
            else:
                shutil.move(str(item), str(dest_item))
                print_colored(f"    ✅ Movido: {item.name}", Colors.GREEN)

def remove_duplicate_files(root: Path):
    """Remove arquivos duplicados da raiz."""
    print_colored("\n🗑️  Removendo arquivos duplicados da raiz...", Colors.YELLOW)
    
    # Arquivos que devem estar apenas em src/apps/
    files_to_remove = [
        "api.py",
        "bot.py",
        "chains.py",
        "loader.py",
        "pdf_bot.py",
        "utils.py",
    ]
    
    # Dockerfiles que devem estar apenas em docker/
    dockerfiles_to_remove = [
        "api.Dockerfile",
        "bot.Dockerfile",
        "front-end.Dockerfile",
        "loader.Dockerfile",
        "pdf_bot.Dockerfile",
        "pull_model.Dockerfile",
    ]
    
    removed = []
    errors = []
    
    for file_name in files_to_remove + dockerfiles_to_remove:
        file_path = root / file_name
        if file_path.exists():
            try:
                # Verifica se existe em src/apps/ ou docker/
                if file_name.endswith(".py"):
                    dest = root / "src" / "apps" / file_name
                else:
                    dest = root / "docker" / file_name
                
                if dest.exists():
                    # Compara conteúdo
                    if file_path.read_bytes() == dest.read_bytes():
                        file_path.unlink()
                        print_colored(f"  ✅ Removido duplicado: {file_name}", Colors.GREEN)
                        removed.append(file_name)
                    else:
                        print_colored(f"  ⚠️  {file_name} difere, mantendo ambos", Colors.YELLOW)
                else:
                    # Move para destino
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(file_path), str(dest))
                    print_colored(f"  ✅ Movido: {file_name} -> {dest.relative_to(root)}", Colors.GREEN)
                    removed.append(file_name)
            except Exception as e:
                errors.append(f"{file_name}: {str(e)}")
                print_colored(f"  ❌ Erro ao processar {file_name}: {e}", Colors.RED)
    
    # Remove docker-compose.yml da raiz se existe em config/
    compose_root = root / "docker-compose.yml"
    compose_config = root / "config" / "docker-compose.yml"
    
    if compose_root.exists() and compose_config.exists():
        try:
            # Compara conteúdo
            if compose_root.read_bytes() != compose_config.read_bytes():
                backup = compose_root.with_suffix(".backup")
                shutil.copy2(compose_root, backup)
                print_colored(f"  ⚠️  Backup criado: docker-compose.yml.backup", Colors.YELLOW)
            
            compose_root.unlink()
            print_colored(f"  ✅ Removido: docker-compose.yml (usar config/docker-compose.yml)", Colors.GREEN)
            removed.append("docker-compose.yml")
        except Exception as e:
            print_colored(f"  ❌ Erro ao remover docker-compose.yml: {e}", Colors.RED)
    
    return removed, errors

def create_obsidian_mapping(root: Path):
    """Cria mapeamento do projeto para Obsidian."""
    print_colored("\n📝 Criando mapeamento para Obsidian...", Colors.YELLOW)
    
    obsidian_dir = root / "Obsidian_guardar aqui"
    obsidian_dir.mkdir(exist_ok=True)
    
    mapping = {
        "project_name": "IA-Test",
        "created_at": datetime.now().isoformat(),
        "structure": {},
        "agents": [],
        "apps": [],
        "docs": [],
        "scripts": [],
    }
    
    # Mapeia estrutura
    structure = {
        "src/agents": "Agentes do sistema",
        "src/apps": "Aplicações principais",
        "docker": "Configurações Docker",
        "config": "Configurações do projeto",
        "docs": "Documentação técnica",
        "scripts": "Scripts utilitários",
        "examples": "Exemplos de uso",
        "front-end": "Frontend Svelte",
        "Obsidian_guardar aqui": "Documentação Obsidian",
    }
    
    for folder, description in structure.items():
        folder_path = root / folder
        if folder_path.exists():
            files = []
            for file in folder_path.rglob("*"):
                if file.is_file() and not file.name.startswith("."):
                    rel_path = file.relative_to(root)
                    files.append({
                        "name": file.name,
                        "path": str(rel_path),
                        "size": file.stat().st_size,
                    })
            
            mapping["structure"][folder] = {
                "description": description,
                "files": files[:50],  # Limita a 50 arquivos por pasta
            }
    
    # Mapeia agentes
    agents_dir = root / "src" / "agents"
    if agents_dir.exists():
        for agent_file in agents_dir.glob("*.py"):
            if agent_file.name != "__init__.py":
                mapping["agents"].append({
                    "name": agent_file.stem,
                    "file": str(agent_file.relative_to(root)),
                })
    
    # Mapeia apps
    apps_dir = root / "src" / "apps"
    if apps_dir.exists():
        for app_file in apps_dir.glob("*.py"):
            if app_file.name != "__init__.py":
                mapping["apps"].append({
                    "name": app_file.stem,
                    "file": str(app_file.relative_to(root)),
                })
    
    # Mapeia docs
    docs_dir = root / "docs"
    if docs_dir.exists():
        for doc_file in docs_dir.glob("*.md"):
            mapping["docs"].append({
                "name": doc_file.stem,
                "file": str(doc_file.relative_to(root)),
            })
    
    # Mapeia scripts
    scripts_dir = root / "scripts"
    if scripts_dir.exists():
        for script_file in scripts_dir.glob("*.py"):
            mapping["scripts"].append({
                "name": script_file.stem,
                "file": str(script_file.relative_to(root)),
            })
    
    # Salva mapeamento JSON
    mapping_file = obsidian_dir / "project_mapping.json"
    with open(mapping_file, "w", encoding="utf-8") as f:
        json.dump(mapping, f, indent=2, ensure_ascii=False)
    
    print_colored(f"  ✅ Mapeamento salvo: {mapping_file.relative_to(root)}", Colors.GREEN)
    
    # Cria nota principal do projeto
    create_project_note(root, obsidian_dir, mapping)
    
    return mapping_file

def create_project_note(root: Path, obsidian_dir: Path, mapping: Dict):
    """Cria nota principal do projeto no Obsidian."""
    note_content = f"""# 🏗️ Projeto IA-Test - Mapeamento Completo

> **Criado em:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 📁 Estrutura do Projeto

"""
    
    for folder, info in mapping["structure"].items():
        note_content += f"### 📂 {folder}\n"
        note_content += f"**Descrição:** {info['description']}\n\n"
        note_content += f"**Arquivos:** {len(info['files'])}\n\n"
        note_content += "---\n\n"
    
    note_content += f"""
## 🤖 Agentes ({len(mapping['agents'])})

"""
    for agent in mapping["agents"]:
        note_content += f"- [[{agent['name']}]] - `{agent['file']}`\n"
    
    note_content += f"""
## 📱 Aplicações ({len(mapping['apps'])})

"""
    for app in mapping["apps"]:
        note_content += f"- [[{app['name']}]] - `{app['file']}`\n"
    
    note_content += f"""
## 📚 Documentação ({len(mapping['docs'])})

"""
    for doc in mapping["docs"]:
        note_content += f"- [[{doc['name']}]] - `{doc['file']}`\n"
    
    note_content += f"""
## 🔧 Scripts ({len(mapping['scripts'])})

"""
    for script in mapping["scripts"]:
        note_content += f"- [[{script['name']}]] - `{script['file']}`\n"
    
    note_content += """
## 🔗 Links Úteis

- [[00-MAPA-DE-AGENTES]]
- [[01-Guia-Obsidian]]
- [[02-Guia-Cursor]]
- [[03-Manual-Sistema-Agentes]]

## 📊 Estatísticas

- **Total de Agentes:** {len(mapping['agents'])}
- **Total de Aplicações:** {len(mapping['apps'])}
- **Total de Documentos:** {len(mapping['docs'])}
- **Total de Scripts:** {len(mapping['scripts'])}

---
*Última atualização: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""
    
    note_file = obsidian_dir / "PROJETO-IA-TEST.md"
    note_file.write_text(note_content, encoding="utf-8")
    
    print_colored(f"  ✅ Nota criada: {note_file.relative_to(root)}", Colors.GREEN)

def main():
    """Função principal."""
    print_colored("🚀 Iniciando organização do projeto...", Colors.BLUE)
    
    root = get_project_root()
    print_colored(f"📁 Raiz do projeto: {root}", Colors.BLUE)
    
    ia_test_sub = root / "IA-test"
    
    if not ia_test_sub.exists():
        print_colored("⚠️  Pasta IA-test/IA-test/ não encontrada!", Colors.YELLOW)
        return
    
    # Consolida estrutura
    moved, skipped, errors = consolidate_ia_test_folder(root, ia_test_sub)
    
    # Remove duplicações
    removed, remove_errors = remove_duplicate_files(root)
    
    # Cria mapeamento Obsidian
    mapping_file = create_obsidian_mapping(root)
    
    # Tenta remover pasta vazia
    try:
        if ia_test_sub.exists() and not any(ia_test_sub.iterdir()):
            ia_test_sub.rmdir()
            print_colored(f"\n✅ Pasta vazia removida: IA-test/", Colors.GREEN)
        elif ia_test_sub.exists():
            remaining = list(ia_test_sub.iterdir())
            print_colored(f"\n⚠️  Pasta IA-test/ ainda contém: {[f.name for f in remaining]}", Colors.YELLOW)
    except Exception as e:
        print_colored(f"\n⚠️  Não foi possível remover pasta IA-test/: {e}", Colors.YELLOW)
    
    # Resumo
    print_colored("\n" + "="*60, Colors.BLUE)
    print_colored("📊 RESUMO", Colors.BLUE)
    print_colored("="*60, Colors.BLUE)
    print_colored(f"✅ Arquivos/pastas movidos: {len(moved)}", Colors.GREEN)
    print_colored(f"⏭️  Ignorados: {len(skipped)}", Colors.YELLOW)
    print_colored(f"🗑️  Duplicados removidos: {len(removed)}", Colors.GREEN)
    if errors or remove_errors:
        print_colored(f"❌ Erros: {len(errors) + len(remove_errors)}", Colors.RED)
    print_colored(f"📝 Mapeamento: {mapping_file.relative_to(root)}", Colors.GREEN)
    print_colored("="*60, Colors.BLUE)

if __name__ == "__main__":
    main()

