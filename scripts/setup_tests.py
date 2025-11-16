#!/usr/bin/env python3
"""
Script para configurar o ambiente de testes do projeto IA-Test.
"""
import subprocess
import sys
from pathlib import Path

def install_requirements():
    """Instala as dependências de teste."""
    print("📦 Instalando dependências de teste...")
    
    requirements_file = Path(__file__).parent.parent / "config" / "requirements.txt"
    
    if not requirements_file.exists():
        print(f"❌ Arquivo {requirements_file} não encontrado!")
        return False
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
        ])
        print("✅ Dependências instaladas com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False

def verify_setup():
    """Verifica se o ambiente está configurado corretamente."""
    print("\n🔍 Verificando configuração...")
    
    # Verifica pytest
    try:
        import pytest
        print(f"✅ pytest instalado (versão {pytest.__version__})")
    except ImportError:
        print("❌ pytest não instalado")
        return False
    
    # Verifica se o diretório tests existe
    tests_dir = Path(__file__).parent.parent / "tests"
    if tests_dir.exists():
        print(f"✅ Diretório tests existe: {tests_dir}")
    else:
        print(f"❌ Diretório tests não existe: {tests_dir}")
        return False
    
    # Verifica arquivos de teste
    test_files = list(tests_dir.glob("test_*.py"))
    if test_files:
        print(f"✅ {len(test_files)} arquivo(s) de teste encontrado(s)")
    else:
        print("⚠️  Nenhum arquivo de teste encontrado")
    
    return True

def main():
    """Função principal."""
    print("="*60)
    print("🧪 CONFIGURAÇÃO DO AMBIENTE DE TESTES")
    print("="*60)
    
    # Instala dependências
    if not install_requirements():
        print("\n❌ Falha ao instalar dependências")
        sys.exit(1)
    
    # Verifica setup
    if not verify_setup():
        print("\n❌ Configuração incompleta")
        sys.exit(1)
    
    print("\n" + "="*60)
    print("✅ AMBIENTE DE TESTES CONFIGURADO!")
    print("="*60)
    print("\n📝 Próximos passos:")
    print("  1. Execute: pytest")
    print("  2. Ou: pytest tests/test_orchestrator.py")
    print("  3. Com cobertura: pytest --cov=src --cov-report=html")
    print("\n💡 Para usar TestSprite:")
    print("  1. Instale o MCP Server: npm install -g @testsprite/mcp-server")
    print("  2. Configure a API key no .env: TESTSPRITE_API_KEY=...")
    print("  3. Consulte: docs/TESTSPRITE_SETUP.md")

if __name__ == "__main__":
    main()

