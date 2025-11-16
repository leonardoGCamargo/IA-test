# -*- coding: utf-8 -*-
"""
Script para reorganizar arquivos duplicados.
Usa os agentes para ajudar na decisão.
"""

import os
import shutil
from pathlib import Path
from typing import List, Dict

project_root = Path(__file__).parent.parent

def verificar_duplicatas():
    """Verifica arquivos duplicados."""
    duplicatas = []
    
    # Arquivos que podem estar duplicados
    arquivos_raiz = ["api.py", "bot.py", "chains.py", "loader.py", "pdf_bot.py"]
    
    for arquivo in arquivos_raiz:
        raiz_path = project_root / arquivo
        src_path = project_root / "src" / "apps" / arquivo
        
        if raiz_path.exists() and src_path.exists():
            # Compara tamanhos
            raiz_size = raiz_path.stat().st_size
            src_size = src_path.stat().st_size
            
            duplicatas.append({
                "arquivo": arquivo,
                "raiz": str(raiz_path),
                "src": str(src_path),
                "raiz_size": raiz_size,
                "src_size": src_size,
                "sugestao": "src/apps" if src_size >= raiz_size else "raiz"
            })
    
    return duplicatas

def verificar_estrutura_duplicada():
    """Verifica estrutura IA-test/IA-test/."""
    ia_test_path = project_root / "IA-test"
    problemas = []
    
    if ia_test_path.exists() and ia_test_path.is_dir():
        # Verifica se há duplicação
        sub_ia_test = ia_test_path / "IA-test"
        if sub_ia_test.exists():
            problemas.append({
                "tipo": "Estrutura duplicada",
                "caminho": "IA-test/IA-test/",
                "acao": "Verificar conteúdo e possivelmente remover"
            })
    
    return problemas

def main():
    """Função principal."""
    print("=" * 70)
    print("ANALISE DE ARQUIVOS DUPLICADOS")
    print("=" * 70)
    print()
    
    # Verifica duplicatas
    duplicatas = verificar_duplicatas()
    
    if duplicatas:
        print("Arquivos duplicados encontrados:\n")
        for dup in duplicatas:
            print(f"  {dup['arquivo']}:")
            print(f"    Raiz: {dup['raiz_size']} bytes")
            print(f"    src/apps: {dup['src_size']} bytes")
            print(f"    Sugestao: Manter em {dup['sugestao']}")
            print()
    else:
        print("Nenhum arquivo duplicado encontrado.")
    
    # Verifica estrutura
    problemas = verificar_estrutura_duplicada()
    
    if problemas:
        print("\nProblemas de estrutura:\n")
        for prob in problemas:
            print(f"  {prob['tipo']}: {prob['caminho']}")
            print(f"    Acao: {prob['acao']}")
            print()
    
    print("\n" + "=" * 70)
    print("ANALISE CONCLUIDA")
    print("=" * 70)
    print("\nRecomendacao:")
    print("  - Manter arquivos em src/apps/ (estrutura correta)")
    print("  - Remover duplicatas da raiz se src/apps/ for mais recente")
    print("  - Verificar estrutura IA-test/IA-test/ antes de remover")

if __name__ == "__main__":
    main()

