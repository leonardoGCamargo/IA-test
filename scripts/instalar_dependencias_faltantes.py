# -*- coding: utf-8 -*-
"""
Script para instalar dependências faltantes do sistema
"""

import subprocess
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent

def instalar_dependencias():
    """Instala dependências faltantes."""
    
    dependencias_criticas = [
        "langsmith>=0.1.0",
        "redis>=5.0.0",
        "celery>=5.3.0",
        "slowapi>=0.1.9",
    ]
    
    dependencias_importantes = [
        "fastapi-users>=12.0.0",
        "python-jose[cryptography]>=3.3.0",
        "sentry-sdk>=2.0.0",
    ]
    
    dependencias_opcionais = [
        "structlog>=23.2.0",
        "prometheus-client>=0.19.0",
    ]
    
    print("=" * 70)
    print("INSTALANDO DEPENDENCIAS FALTANTES")
    print("=" * 70)
    print()
    
    print("1. Dependencias CRITICAS:")
    for dep in dependencias_criticas:
        print(f"   Instalando: {dep}")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", dep], check=True)
            print(f"   OK: {dep}")
        except subprocess.CalledProcessError:
            print(f"   ERRO: {dep}")
    print()
    
    print("2. Dependencias IMPORTANTES:")
    for dep in dependencias_importantes:
        print(f"   Instalando: {dep}")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", dep], check=True)
            print(f"   OK: {dep}")
        except subprocess.CalledProcessError:
            print(f"   ERRO: {dep}")
    print()
    
    print("3. Dependencias OPCIONAIS:")
    for dep in dependencias_opcionais:
        print(f"   Instalando: {dep}")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", dep], check=True)
            print(f"   OK: {dep}")
        except subprocess.CalledProcessError:
            print(f"   ERRO: {dep}")
    print()
    
    print("=" * 70)
    print("INSTALACAO CONCLUIDA!")
    print("=" * 70)
    print()
    print("Proximos passos:")
    print("1. Configurar LangSmith no .env")
    print("2. Instalar Redis (Docker ou local)")
    print("3. Configurar cache no código")
    print()
    print("Veja: Obsidian_guardar aqui/RESUMO-O-QUE-FALTA.md")

if __name__ == "__main__":
    instalar_dependencias()

