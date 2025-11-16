"""
Script para instalar Playwright e seus navegadores.

Execute: python scripts/install_playwright.py
"""

import subprocess
import sys

def install_playwright():
    """Instala Playwright e os navegadores necessários."""
    print("📦 Instalando Playwright...")
    
    # Instala playwright via pip
    subprocess.run([sys.executable, "-m", "pip", "install", "playwright", "pytest-playwright"], check=True)
    
    print("✅ Playwright instalado!")
    print("🌐 Instalando navegadores...")
    
    # Instala navegadores
    subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
    
    print("✅ Navegadores instalados!")
    print("\n💡 Para executar os testes E2E:")
    print("   pytest tests/test_dashboard_e2e.py -v")

if __name__ == "__main__":
    install_playwright()

