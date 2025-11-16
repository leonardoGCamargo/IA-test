#!/usr/bin/env python3
"""
Script para executar o Agent Dashboard.

Uso:
    python scripts/run_dashboard.py
    ou
    streamlit run src/apps/agent_dashboard.py --server.port=8508
"""

import sys
import os
from pathlib import Path

# Adiciona o diretório raiz ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Muda para o diretório raiz
os.chdir(project_root)

if __name__ == "__main__":
    import subprocess
    
    # Executa o Streamlit
    subprocess.run([
        sys.executable,
        "-m",
        "streamlit",
        "run",
        "src/apps/agent_dashboard.py",
        "--server.port=8508",
        "--server.address=0.0.0.0"
    ])

