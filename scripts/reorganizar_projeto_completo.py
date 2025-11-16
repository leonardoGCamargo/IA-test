# -*- coding: utf-8 -*-
"""
Script para reorganizar projeto completo:
1. Remove arquivos duplicados da raiz
2. Move conteúdo de IA-test/IA-test/ para raiz
3. Renomeia pasta interna para nome melhor
"""

import os
import shutil
from pathlib import Path
from typing import List, Dict, Set

project_root = Path(__file__).parent.parent

def get_unique_files(source: Path, dest: Path) -> List[Path]:
    """Retorna arquivos que existem apenas no source."""
    unique = []
    for item in source.iterdir():
        if item.is_file():
            dest_file = dest / item.name
            if not dest_file.exists():
                unique.append(item)
        elif item.is_dir() and item.name not in ['__pycache__', '.git', '.venv']:
            unique.append(item)
    return unique

def move_file_safe(source: Path, dest: Path):
    """Move arquivo com segurança."""
    if dest.exists():
        # Se destino existe, compara tamanhos
        if source.stat().st_size > dest.stat().st_size:
            # Source é maior, substitui
            dest.unlink()
            shutil.move(str(source), str(dest))
            print(f"  Movido (substituiu): {source.name}")
        else:
            # Destino é maior, remove source
            source.unlink()
            print(f"  Removido (destino maior): {source.name}")
    else:
        # Destino não existe, move normalmente
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(source), str(dest))
        print(f"  Movido: {source.name}")

def reorganizar():
    """Reorganiza o projeto."""
    print("=" * 70)
    print("REORGANIZACAO DO PROJETO")
    print("=" * 70)
    print()
    
    # 1. Verifica pasta IA-test/IA-test/
    ia_test_interno = project_root / "IA-test" / "IA-test"
    
    # Tenta caminho alternativo
    if not ia_test_interno.exists():
        # Verifica se existe como subdiretório
        ia_test_pai = project_root / "IA-test"
        if ia_test_pai.exists():
            for item in ia_test_pai.iterdir():
                if item.is_dir() and item.name == "IA-test":
                    ia_test_interno = item
                    break
    
    if not ia_test_interno.exists():
        print(f"Pasta IA-test/IA-test/ nao encontrada em: {ia_test_interno}")
        print("Verificando estrutura...")
        ia_test_pai = project_root / "IA-test"
        if ia_test_pai.exists():
            print(f"Conteudo de IA-test/:")
            for item in ia_test_pai.iterdir():
                print(f"  - {item.name} ({'dir' if item.is_dir() else 'file'})")
        return
    
    print("1. Movendo conteudo de IA-test/IA-test/ para raiz...")
    print()
    
    # Lista tudo na pasta interna
    itens = list(ia_test_interno.iterdir())
    
    for item in itens:
        if item.name in ['.git', '__pycache__', '.venv', 'node_modules']:
            continue
        
        destino = project_root / item.name
        
        if item.is_file():
            if destino.exists():
                # Compara tamanhos
                if item.stat().st_size > destino.stat().st_size:
                    destino.unlink()
                    shutil.move(str(item), str(destino))
                    print(f"  Movido (substituiu): {item.name}")
                else:
                    item.unlink()
                    print(f"  Removido (destino maior): {item.name}")
            else:
                shutil.move(str(item), str(destino))
                print(f"  Movido: {item.name}")
        
        elif item.is_dir():
            if destino.exists():
                # Move conteúdo da pasta
                for subitem in item.rglob('*'):
                    if subitem.is_file():
                        rel_path = subitem.relative_to(item)
                        dest_file = destino / rel_path
                        dest_file.parent.mkdir(parents=True, exist_ok=True)
                        if not dest_file.exists():
                            shutil.move(str(subitem), str(dest_file))
                            print(f"  Movido: {item.name}/{rel_path}")
                # Remove pasta vazia
                try:
                    item.rmdir()
                except:
                    pass
            else:
                shutil.move(str(item), str(destino))
                print(f"  Movido pasta: {item.name}")
    
    print()
    print("2. Removendo arquivos duplicados da raiz...")
    print()
    
    # Arquivos para remover da raiz (manter em src/apps/)
    arquivos_raiz = ["api.py", "bot.py", "chains.py", "loader.py", "pdf_bot.py"]
    
    for arquivo in arquivos_raiz:
        raiz_path = project_root / arquivo
        src_path = project_root / "src" / "apps" / arquivo
        
        if raiz_path.exists() and src_path.exists():
            raiz_path.unlink()
            print(f"  Removido: {arquivo} (mantido em src/apps/)")
    
    print()
    print("3. Renomeando pasta IA-test/IA-test/...")
    print()
    
    # Verifica se pasta ainda existe (pode ter sido esvaziada)
    if ia_test_interno.exists() and any(ia_test_interno.iterdir()):
        # Renomeia para algo melhor
        novo_nome = "legacy-backup"
        novo_path = project_root / "IA-test" / novo_nome
        
        if novo_path.exists():
            # Se já existe, move conteúdo
            for item in ia_test_interno.iterdir():
                shutil.move(str(item), str(novo_path / item.name))
            ia_test_interno.rmdir()
        else:
            ia_test_interno.rename(novo_path)
        
        print(f"  Renomeado: IA-test/IA-test/ -> IA-test/{novo_nome}/")
    else:
        # Pasta vazia, remove
        try:
            ia_test_interno.rmdir()
            print("  Removida pasta vazia: IA-test/IA-test/")
        except:
            pass
    
    print()
    print("4. Verificando pasta Obsidian duplicada...")
    print()
    
    obsidian_duplicado = project_root / "Obsidian_guardar aqui" / "Obsidian_guardar aqui"
    if obsidian_duplicado.exists():
        # Move conteúdo para raiz do Obsidian
        obsidian_raiz = project_root / "Obsidian_guardar aqui"
        for item in obsidian_duplicado.iterdir():
            destino = obsidian_raiz / item.name
            if not destino.exists():
                shutil.move(str(item), str(destino))
                print(f"  Movido: {item.name}")
        try:
            obsidian_duplicado.rmdir()
            print("  Removida pasta duplicada")
        except:
            pass
    
    print()
    print("=" * 70)
    print("REORGANIZACAO CONCLUIDA!")
    print("=" * 70)

if __name__ == "__main__":
    try:
        reorganizar()
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()

