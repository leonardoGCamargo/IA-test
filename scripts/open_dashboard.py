#!/usr/bin/env python3
"""
Script para abrir o dashboard no navegador automaticamente.
"""
import webbrowser
import time
import subprocess
import sys
from pathlib import Path

def open_dashboard():
    """Abre o dashboard no navegador."""
    url = "http://localhost:8508"
    
    print(f"🌐 Abrindo dashboard: {url}")
    
    # Tenta abrir no navegador padrão
    try:
        webbrowser.open(url)
        print(f"✅ Dashboard aberto no navegador!")
        print(f"📱 URL: {url}")
    except Exception as e:
        print(f"❌ Erro ao abrir navegador: {e}")
        print(f"💡 Abra manualmente: {url}")

def check_dashboard_running():
    """Verifica se o dashboard está rodando."""
    import requests
    try:
        response = requests.get("http://localhost:8508", timeout=2)
        return response.status_code == 200
    except:
        return False

def start_and_open_dashboard():
    """Inicia o dashboard e abre no navegador."""
    project_root = Path(__file__).parent.parent
    
    print("🚀 Iniciando Dashboard de Agentes...")
    print(f"📁 Diretório: {project_root}")
    
    # Muda para o diretório raiz
    import os
    os.chdir(project_root)
    
    # Inicia o dashboard em background
    print("⏳ Aguardando dashboard iniciar...")
    
    process = subprocess.Popen([
        sys.executable, "-m", "streamlit", "run",
        "src/apps/agent_dashboard.py",
        "--server.port=8508",
        "--server.address=0.0.0.0"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Aguarda alguns segundos para o dashboard iniciar
    time.sleep(5)
    
    # Verifica se está rodando
    if check_dashboard_running():
        print("✅ Dashboard iniciado com sucesso!")
        open_dashboard()
    else:
        print("⚠️ Dashboard pode estar iniciando...")
        print("💡 Aguarde alguns segundos e abra manualmente: http://localhost:8508")
        open_dashboard()
    
    print("\n💡 Pressione Ctrl+C para parar o dashboard\n")
    
    try:
        process.wait()
    except KeyboardInterrupt:
        print("\n\n👋 Encerrando dashboard...")
        process.terminate()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "open":
        # Apenas abre, não inicia
        open_dashboard()
    else:
        # Inicia e abre
        start_and_open_dashboard()

