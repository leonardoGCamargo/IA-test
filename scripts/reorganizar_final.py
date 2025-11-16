# -*- coding: utf-8 -*-
"""
Script final para reorganizar:
1. Remove arquivos duplicados da raiz
2. Move conteúdo de IA-test/ para raiz (se necessário)
3. Renomeia pasta IA-test/ para nome melhor
"""

import os
import shutil
from pathlib import Path

project_root = Path(__file__).parent.parent

def reorganizar():
    """Reorganiza o projeto."""
    print("=" * 70)
    print("REORGANIZACAO FINAL DO PROJETO")
    print("=" * 70)
    print()
    
    # 1. Remove arquivos duplicados da raiz
    print("1. Removendo arquivos duplicados da raiz...")
    print()
    
    arquivos_raiz = ["api.py", "bot.py", "chains.py", "loader.py", "pdf_bot.py"]
    
    for arquivo in arquivos_raiz:
        raiz_path = project_root / arquivo
        src_path = project_root / "src" / "apps" / arquivo
        
        if raiz_path.exists() and src_path.exists():
            raiz_path.unlink()
            print(f"  Removido: {arquivo} (mantido em src/apps/)")
    
    print()
    
    # 2. Verifica pasta IA-test/
    ia_test_pasta = project_root / "IA-test"
    
    if not ia_test_pasta.exists():
        print("Pasta IA-test/ nao encontrada.")
        return
    
    print("2. Movendo conteudo unico de IA-test/ para raiz...")
    print()
    
    # Itens para não mover (já existem na raiz ou são específicos)
    itens_ignorar = {
        '.git', '.github', '__pycache__', '.venv', 'node_modules',
        'IA-test'  # Não mover a si mesmo
    }
    
    # Itens que já existem na raiz (não mover)
    itens_existentes = {
        'src', 'scripts', 'docs', 'config', 'docker', 'front-end',
        'Obsidian_guardar aqui', 'tests', 'examples', 'embedding_model'
    }
    
    movidos = 0
    ignorados = 0
    
    for item in ia_test_pasta.iterdir():
        if item.name in itens_ignorar:
            continue
        
        destino = project_root / item.name
        
        if item.is_file():
            if destino.exists():
                # Compara tamanhos - se interno é maior, substitui
                if item.stat().st_size > destino.stat().st_size:
                    destino.unlink()
                    shutil.move(str(item), str(destino))
                    print(f"  Movido (substituiu): {item.name}")
                    movidos += 1
                else:
                    item.unlink()
                    print(f"  Removido (destino maior): {item.name}")
                    ignorados += 1
            else:
                shutil.move(str(item), str(destino))
                print(f"  Movido: {item.name}")
                movidos += 1
        
        elif item.is_dir():
            if item.name in itens_existentes:
                # Move conteúdo da pasta se não existir na raiz
                for subitem in item.rglob('*'):
                    if subitem.is_file():
                        rel_path = subitem.relative_to(item)
                        dest_file = destino / rel_path
                        if not dest_file.exists():
                            dest_file.parent.mkdir(parents=True, exist_ok=True)
                            shutil.move(str(subitem), str(dest_file))
                            print(f"  Movido: {item.name}/{rel_path}")
                            movidos += 1
                # Tenta remover pasta vazia
                try:
                    if not any(item.iterdir()):
                        item.rmdir()
                except:
                    pass
            else:
                if not destino.exists():
                    shutil.move(str(item), str(destino))
                    print(f"  Movido pasta: {item.name}")
                    movidos += 1
                else:
                    # Move conteúdo
                    for subitem in item.rglob('*'):
                        if subitem.is_file():
                            rel_path = subitem.relative_to(item)
                            dest_file = destino / rel_path
                            if not dest_file.exists():
                                dest_file.parent.mkdir(parents=True, exist_ok=True)
                                shutil.move(str(subitem), str(dest_file))
                                print(f"  Movido: {item.name}/{rel_path}")
                                movidos += 1
                    try:
                        if not any(item.iterdir()):
                            item.rmdir()
                    except:
                        pass
    
    print()
    print(f"  Total movidos: {movidos}")
    print(f"  Total ignorados/removidos: {ignorados}")
    print()
    
    # 3. Renomeia pasta IA-test/ para nome melhor
    print("3. Renomeando pasta IA-test/...")
    print()
    
    if ia_test_pasta.exists():
        # Verifica se está vazia ou quase vazia
        conteudo_restante = [x for x in ia_test_pasta.iterdir() 
                            if x.name not in ['.git', '.github', '__pycache__']]
        
        if len(conteudo_restante) == 0:
            # Pasta vazia, remove
            try:
                ia_test_pasta.rmdir()
                print("  Removida pasta vazia: IA-test/")
            except:
                print("  Nao foi possivel remover pasta (pode ter conteudo oculto)")
        else:
            # Renomeia para nome melhor
            novo_nome = "legacy-backup"
            novo_path = project_root / novo_nome
            
            if novo_path.exists():
                print(f"  Pasta {novo_nome}/ ja existe, mantendo IA-test/")
            else:
                ia_test_pasta.rename(novo_path)
                print(f"  Renomeado: IA-test/ -> {novo_nome}/")
    
    print()
    
    # 4. Limpa pasta Obsidian duplicada
    print("4. Limpando pasta Obsidian duplicada...")
    print()
    
    obsidian_raiz = project_root / "Obsidian_guardar aqui"
    obsidian_duplicado = obsidian_raiz / "Obsidian_guardar aqui"
    
    if obsidian_duplicado.exists():
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
    print()
    print("Estrutura final:")
    print("  - Arquivos duplicados removidos da raiz")
    print("  - Conteudo de IA-test/ movido para raiz")
    print("  - Pasta IA-test/ renomeada ou removida")
    print("  - Pasta Obsidian duplicada limpa")

if __name__ == "__main__":
    try:
        reorganizar()
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()

