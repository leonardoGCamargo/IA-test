"""
Script simples para atualizar configurações do .env
"""

import os
from pathlib import Path

# Configurações
configs = {
    "GOOGLE_API_KEY": "AIzaSyD7lSqUzy-xvlP3sQHf0IaqAnemtgOqoeM",
    "NEON_PROJECT_ID": "napi_jyp0h0270gydb0xvzyei2msvd5dcyv2uvb7l4lig665dx4rgd1cjh9znfw3h5x8s",
    "MONGODB_URI": "mongodb+srv://DBLEONARDO:<@1Leonardo0409>@lgian.ru8ds53.mongodb.net/",
    "MONGODB_DATABASE": "default",
    "MONGODB_ATLAS": "true",
}

project_root = Path(__file__).parent.parent
env_file = project_root / ".env"

# Lê arquivo
lines = []
if env_file.exists():
    with open(env_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

# Atualiza
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

# Adiciona faltantes
for key, value in configs.items():
    if not updated[key]:
        new_lines.append(f"{key}={value}\n")

# Salva
with open(env_file, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("✅ Configurações atualizadas!")
for key, value in configs.items():
    if "KEY" in key or "URI" in key:
        print(f"   {key}={value[:30]}...")
    else:
        print(f"   {key}={value}")

