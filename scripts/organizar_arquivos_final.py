# -*- coding: utf-8 -*-
"""
Script para organizar arquivos finais:
- .md -> Obsidian_guardar aqui/
- .yml/.yaml -> config/ ou docker/
- Outros arquivos -> pastas apropriadas
"""

import os
import shutil
from pathlib import Path
from typing import List, Dict

project_root = Path(__file__).parent.parent

def organizar_markdown():
    """Move arquivos .md para Obsidian."""
    print("1. Organizando arquivos .md...")
    print()
    
    obsidian_path = project_root / "Obsidian_guardar aqui"
    obsidian_path.mkdir(exist_ok=True)
    
    # Arquivos .md na raiz que devem ir para Obsidian
    md_files_raiz = list(project_root.glob("*.md"))
    
    # Exceções: arquivos que devem ficar na raiz
    manter_raiz = {
        "readme.md", "README.md", "README.md.backup"
    }
    
    movidos = 0
    
    for md_file in md_files_raiz:
        if md_file.name.lower() in manter_raiz:
            continue
        
        destino = obsidian_path / md_file.name
        
        if destino.exists():
            # Se destino existe, compara tamanhos
            if md_file.stat().st_size > destino.stat().st_size:
                destino.unlink()
                shutil.move(str(md_file), str(destino))
                print(f"  Movido (substituiu): {md_file.name}")
            else:
                md_file.unlink()
                print(f"  Removido (destino maior): {md_file.name}")
        else:
            shutil.move(str(md_file), str(destino))
            print(f"  Movido: {md_file.name}")
        
        movidos += 1
    
    print(f"  Total processados: {movidos}")
    print()

def organizar_yml():
    """Move arquivos .yml/.yaml para pastas apropriadas."""
    print("2. Organizando arquivos .yml/.yaml...")
    print()
    
    config_path = project_root / "config"
    docker_path = project_root / "docker"
    config_path.mkdir(exist_ok=True)
    docker_path.mkdir(exist_ok=True)
    
    # Arquivos .yml na raiz
    yml_files = list(project_root.glob("*.yml")) + list(project_root.glob("*.yaml"))
    
    movidos = 0
    
    for yml_file in yml_files:
        nome = yml_file.name.lower()
        
        # Decide destino baseado no nome
        if "docker" in nome or "compose" in nome:
            destino = config_path / yml_file.name
        elif "test" in nome or "pytest" in nome:
            # Mantém na raiz ou move para config
            destino = config_path / yml_file.name
        else:
            destino = config_path / yml_file.name
        
        if destino.exists():
            if yml_file.stat().st_size > destino.stat().st_size:
                destino.unlink()
                shutil.move(str(yml_file), str(destino))
                print(f"  Movido (substituiu): {yml_file.name} -> {destino.parent.name}/")
            else:
                yml_file.unlink()
                print(f"  Removido (destino maior): {yml_file.name}")
        else:
            shutil.move(str(yml_file), str(destino))
            print(f"  Movido: {yml_file.name} -> {destino.parent.name}/")
        
        movidos += 1
    
    print(f"  Total processados: {movidos}")
    print()

def organizar_outros():
    """Organiza outros arquivos."""
    print("3. Organizando outros arquivos...")
    print()
    
    config_path = project_root / "config"
    scripts_path = project_root / "scripts"
    
    # Arquivos de configuração
    config_files = {
        ".dockerignore": config_path,
        ".gitignore": project_root,  # Mantém na raiz
        ".testsprite.yml": config_path,
    }
    
    movidos = 0
    
    for arquivo, destino in config_files.items():
        origem = project_root / arquivo
        if origem.exists():
            dest_file = destino / arquivo
            if not dest_file.exists():
                if destino == project_root:
                    # Mantém na raiz
                    continue
                dest_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(origem), str(dest_file))
                print(f"  Movido: {arquivo} -> {destino.name}/")
                movidos += 1
    
    # Arquivos .sh (scripts)
    sh_files = list(project_root.glob("*.sh"))
    for sh_file in sh_files:
        destino = scripts_path / sh_file.name
        if not destino.exists():
            shutil.move(str(sh_file), str(destino))
            print(f"  Movido: {sh_file.name} -> scripts/")
            movidos += 1
    
    # Arquivos .backup
    backup_files = list(project_root.glob("*.backup"))
    backup_path = project_root / "backups"
    backup_path.mkdir(exist_ok=True)
    
    for backup_file in backup_files:
        destino = backup_path / backup_file.name
        if not destino.exists():
            shutil.move(str(backup_file), str(destino))
            print(f"  Movido: {backup_file.name} -> backups/")
            movidos += 1
    
    print(f"  Total processados: {movidos}")
    print()

def organizar_pastas():
    """Organiza pastas adicionais."""
    print("4. Organizando pastas...")
    print()
    
    # Pasta images/ -> docs/images/ ou assets/
    images_path = project_root / "images"
    if images_path.exists():
        docs_images = project_root / "docs" / "images"
        docs_images.mkdir(parents=True, exist_ok=True)
        
        for item in images_path.iterdir():
            destino = docs_images / item.name
            if not destino.exists():
                shutil.move(str(item), str(destino))
                print(f"  Movido: images/{item.name} -> docs/images/")
        
        try:
            images_path.rmdir()
            print("  Removida pasta vazia: images/")
        except:
            pass
    
    print()

def main():
    """Função principal."""
    print("=" * 70)
    print("ORGANIZACAO FINAL DE ARQUIVOS")
    print("=" * 70)
    print()
    
    organizar_markdown()
    organizar_yml()
    organizar_outros()
    organizar_pastas()
    
    print("=" * 70)
    print("ORGANIZACAO CONCLUIDA!")
    print("=" * 70)
    print()
    print("Estrutura final:")
    print("  - Arquivos .md -> Obsidian_guardar aqui/")
    print("  - Arquivos .yml -> config/")
    print("  - Scripts .sh -> scripts/")
    print("  - Backups -> backups/")
    print("  - Imagens -> docs/images/")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()

