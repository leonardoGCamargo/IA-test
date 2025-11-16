# -*- coding: utf-8 -*-
"""
Script para verificar se cache está implementado no sistema
"""

import os
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent

def verificar_cache():
    """Verifica implementação de cache."""
    print("=" * 70)
    print("VERIFICANDO IMPLEMENTACAO DE CACHE")
    print("=" * 70)
    print()
    
    # Verifica imports de cache
    cache_keywords = [
        "cache",
        "Cache",
        "CACHE",
        "redis",
        "Redis",
        "lru_cache",
        "functools.lru_cache",
        "InMemoryCache",
        "RedisCache",
    ]
    
    encontrados = []
    
    # Busca em arquivos Python
    for py_file in project_root.rglob("*.py"):
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                conteudo = f.read()
                for keyword in cache_keywords:
                    if keyword in conteudo:
                        encontrados.append((py_file.relative_to(project_root), keyword))
        except Exception as e:
            pass
    
    if encontrados:
        print("Cache encontrado nos seguintes arquivos:")
        for arquivo, keyword in encontrados:
            print(f"  - {arquivo}: {keyword}")
    else:
        print("Nenhuma implementacao de cache encontrada.")
    
    print()
    
    # Verifica requirements.txt
    requirements = project_root / "config" / "requirements.txt"
    if requirements.exists():
        with open(requirements, 'r', encoding='utf-8') as f:
            req_content = f.read()
            if "redis" in req_content.lower():
                print("Redis encontrado em requirements.txt")
            else:
                print("Redis NAO encontrado em requirements.txt")
    
    print()
    print("=" * 70)
    print("VERIFICACAO CONCLUIDA")
    print("=" * 70)

if __name__ == "__main__":
    verificar_cache()

