#!/usr/bin/env python3
"""
Script para organizar a estrutura do projeto.
Move arquivos da raiz para estrutura organizada e remove redundâncias.
"""

import os
import shutil
from pathlib import Path
from typing import List, Tuple

def get_project_root() -> Path:
    """Retorna a raiz do projeto."""
    return Path(__file__).parent.parent

def organize_files():
    """Organiza os arquivos do projeto."""
    root = get_project_root()
    
    print("="*70)
    print("📁 ORGANIZAÇÃO DO PROJETO")
    print("="*70)
    
    # Arquivos da raiz que devem ser movidos
    files_to_move = {
        # Python files -> src/apps/
        "api.py": "src/apps/api.py",
        "bot.py": "src/apps/bot.py",
        "chains.py": "src/apps/chains.py",
        "loader.py": "src/apps/loader.py",
        "pdf_bot.py": "src/apps/pdf_bot.py",
        "utils.py": "src/apps/utils.py",
        
        # Dockerfiles -> docker/
        "api.Dockerfile": "docker/api.Dockerfile",
        "bot.Dockerfile": "docker/bot.Dockerfile",
        "front-end.Dockerfile": "docker/front-end.Dockerfile",
        "loader.Dockerfile": "docker/loader.Dockerfile",
        "pdf_bot.Dockerfile": "docker/pdf_bot.Dockerfile",
        "pull_model.Dockerfile": "docker/pull_model.Dockerfile",
        
        # Config files -> config/
        "docker-compose.yml": "config/docker-compose.yml",
        "requirements.txt": "config/requirements.txt",
        "env.example": "config/env.example",
        
        # Scripts -> scripts/
        "install_ollama.sh": "scripts/install_ollama.sh",
        
        # Docs -> docs/
        "readme.md": "docs/README_PROJECT.md",
        "running_on_wsl.md": "docs/running_on_wsl.md",
    }
    
    # Pastas que devem ser movidas/consolidadas
    dirs_to_handle = {
        "front-end": None,  # Manter na raiz
        "embedding_model": None,  # Manter na raiz
        "images": None,  # Manter na raiz
        "IA-test": "CONSOLIDATE",  # Consolidar conteúdo
    }
    
    moved = []
    skipped = []
    errors = []
    
    # Move arquivos
    for source, dest in files_to_move.items():
        source_path = root / source
        dest_path = root / dest
        
        if not source_path.exists():
            skipped.append(f"{source} (não existe)")
            continue
        
        try:
            # Cria diretório de destino se não existir
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Se destino existe, compara
            if dest_path.exists():
                # Verifica se são diferentes
                if source_path.read_bytes() != dest_path.read_bytes():
                    # Backup do destino
                    backup_path = dest_path.with_suffix(dest_path.suffix + ".backup")
                    shutil.copy2(dest_path, backup_path)
                    print(f"⚠️  Backup criado: {backup_path}")
            
            # Move arquivo
            shutil.move(str(source_path), str(dest_path))
            moved.append(f"{source} -> {dest}")
            print(f"✅ Movido: {source} -> {dest}")
        except Exception as e:
            errors.append(f"{source}: {str(e)}")
            print(f"❌ Erro ao mover {source}: {e}")
    
    # Consolida pasta IA-test/IA-test/
    ia_test_sub = root / "IA-test"
    if ia_test_sub.exists() and ia_test_sub.is_dir():
        print("\n📦 Consolidando pasta IA-test/IA-test/...")
        consolidate_ia_test_folder(root, ia_test_sub)
    
    # Remove front-end duplicado
    frontend_dup = root / "IA-test" / "front-end"
    if frontend_dup.exists():
        print(f"\n🗑️  Removendo front-end duplicado: {frontend_dup}")
        try:
            shutil.rmtree(frontend_dup)
            print(f"✅ Removido: {frontend_dup}")
        except Exception as e:
            print(f"❌ Erro ao remover {frontend_dup}: {e}")
    
    # Remove embedding_model duplicado
    embedding_dup = root / "IA-test" / "embedding_model"
    if embedding_dup.exists() and embedding_dup.is_dir():
        print(f"\n🗑️  Removendo embedding_model duplicado: {embedding_dup}")
        try:
            shutil.rmtree(embedding_dup)
            print(f"✅ Removido: {embedding_dup}")
        except Exception as e:
            print(f"❌ Erro ao remover {embedding_dup}: {e}")
    
    # Resumo
    print("\n" + "="*70)
    print("📊 RESUMO")
    print("="*70)
    print(f"✅ Arquivos movidos: {len(moved)}")
    print(f"⏭️  Arquivos ignorados: {len(skipped)}")
    print(f"❌ Erros: {len(errors)}")
    
    if moved:
        print("\n📝 Arquivos movidos:")
        for item in moved:
            print(f"   - {item}")
    
    if errors:
        print("\n❌ Erros:")
        for error in errors:
            print(f"   - {error}")

def consolidate_ia_test_folder(root: Path, ia_test_sub: Path):
    """Consolida conteúdo da pasta IA-test/IA-test/ na estrutura principal."""
    
    # Estrutura de consolidação
    consolidation_map = {
        "docker": "docker",
        "config": "config",
        "docs": "docs",
        "scripts": "scripts",
        "examples": "examples",
        "src": "src",
        "images": "images",  # Se não existir na raiz
    }
    
    for source_dir, dest_dir in consolidation_map.items():
        source_path = ia_test_sub / source_dir
        dest_path = root / dest_dir
        
        if not source_path.exists():
            continue
        
        print(f"\n📦 Consolidando {source_dir}/...")
        
        if source_path.is_dir():
            # Se destino existe, mescla
            if dest_path.exists():
                print(f"   ⚠️  {dest_dir}/ já existe, mesclando...")
                merge_directories(source_path, dest_path)
            else:
                # Move diretório inteiro
                try:
                    shutil.move(str(source_path), str(dest_path))
                    print(f"   ✅ Movido: {source_dir}/ -> {dest_dir}/")
                except Exception as e:
                    print(f"   ❌ Erro ao mover {source_dir}/: {e}")
        elif source_path.is_file():
            # Move arquivo
            try:
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                if dest_path.exists():
                    # Backup
                    backup = dest_path.with_suffix(dest_path.suffix + ".backup")
                    shutil.copy2(dest_path, backup)
                    print(f"   ⚠️  Backup: {backup}")
                shutil.move(str(source_path), str(dest_path))
                print(f"   ✅ Movido: {source_dir} -> {dest_dir}/")
            except Exception as e:
                print(f"   ❌ Erro ao mover {source_dir}: {e}")
    
    # Move arquivos soltos
    for item in ia_test_sub.iterdir():
        if item.name in ["docker", "config", "docs", "scripts", "examples", "src", "images", "__pycache__"]:
            continue
        
        if item.is_file():
            dest = root / item.name
            if not dest.exists():
                try:
                    shutil.move(str(item), str(dest))
                    print(f"   ✅ Movido arquivo: {item.name}")
                except Exception as e:
                    print(f"   ❌ Erro ao mover {item.name}: {e}")

def merge_directories(source: Path, dest: Path):
    """Mescla dois diretórios."""
    for item in source.iterdir():
        dest_item = dest / item.name
        
        if item.is_dir():
            if dest_item.exists():
                merge_directories(item, dest_item)
            else:
                try:
                    shutil.move(str(item), str(dest_item))
                    print(f"      ✅ Movido: {item.name}/")
                except Exception as e:
                    print(f"      ❌ Erro ao mover {item.name}/: {e}")
        else:
            if dest_item.exists():
                # Compara conteúdo
                if item.read_bytes() != dest_item.read_bytes():
                    backup = dest_item.with_suffix(dest_item.suffix + ".backup")
                    shutil.copy2(dest_item, backup)
                    print(f"      ⚠️  Backup: {backup}")
                try:
                    shutil.move(str(item), str(dest_item))
                    print(f"      ✅ Atualizado: {item.name}")
                except Exception as e:
                    print(f"      ❌ Erro ao atualizar {item.name}: {e}")
            else:
                try:
                    shutil.move(str(item), str(dest_item))
                    print(f"      ✅ Movido: {item.name}")
                except Exception as e:
                    print(f"      ❌ Erro ao mover {item.name}: {e}")

if __name__ == "__main__":
    organize_files()

