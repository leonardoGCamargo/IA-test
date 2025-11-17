# -*- coding: utf-8 -*-
"""Script para aplicar configurações no .env"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Configurações - Use variáveis de ambiente ou .env
# NUNCA hardcode secrets aqui!
configs = {
    "GOOGLE_API_KEY": os.getenv("GOOGLE_API_KEY", ""),
    "NEON_PROJECT_ID": os.getenv("NEON_PROJECT_ID", ""),
    "MONGODB_URI": os.getenv("MONGODB_URI", ""),
    "MONGODB_DATABASE": os.getenv("MONGODB_DATABASE", "default"),
    "MONGODB_ATLAS": os.getenv("MONGODB_ATLAS", "false"),
}

project_root = Path(__file__).parent.parent
env_file = project_root / ".env"

lines = []
if env_file.exists():
    with open(env_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

new_lines = []
updated = {k: False for k in configs.keys()}

for line in lines:
    found = False
    for key, value in configs.items():
        if line.strip().startswith(f"{key}="):
            new_lines.append(f"{key}={value}\n")
            updated[key] = True
            found = True
            break
    if not found:
        new_lines.append(line)

for key, value in configs.items():
    if not updated[key]:
        new_lines.append(f"{key}={value}\n")

with open(env_file, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Configuracoes atualizadas!")
for key, value in configs.items():
    if "KEY" in key or "URI" in key:
        print(f"  {key}={value[:30]}...")
    else:
        print(f"  {key}={value}")

