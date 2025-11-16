"""
Script interativo para configurar Linear API
"""

import os
from pathlib import Path

def setup_linear():
    """Configuração interativa do Linear"""
    print("🔧 Configuração do Linear API\n")
    
    # Verificar se .env existe
    env_path = Path(".env")
    if not env_path.exists():
        env_path = Path("config/.env")
        if not env_path.exists():
            print("❌ Arquivo .env não encontrado")
            print("   Crie um arquivo .env na raiz do projeto ou em config/")
            return
    
    print(f"📝 Usando arquivo: {env_path}\n")
    
    # Ler .env atual
    env_vars = {}
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    env_vars[key] = value
    
    # Solicitar API Key
    print("1️⃣ Linear API Key")
    print("   Obtenha em: https://linear.app/settings/api")
    print("   Formato: lin_api_xxxxxxxxxxxxx\n")
    
    current_key = env_vars.get("LINEAR_API_KEY", "")
    if current_key:
        print(f"   API Key atual: {current_key[:10]}...{current_key[-4:]}")
        use_current = input("   Usar API key atual? (s/n): ").lower().strip()
        if use_current != "s":
            new_key = input("   Nova API Key: ").strip()
            if new_key:
                env_vars["LINEAR_API_KEY"] = new_key
    else:
        new_key = input("   API Key: ").strip()
        if new_key:
            env_vars["LINEAR_API_KEY"] = new_key
    
    # Team ID (opcional)
    print("\n2️⃣ Team ID (Opcional)")
    print("   Deixe em branco para detectar automaticamente\n")
    
    current_team = env_vars.get("LINEAR_TEAM_ID", "")
    if current_team:
        print(f"   Team ID atual: {current_team}")
        use_current = input("   Usar Team ID atual? (s/n): ").lower().strip()
        if use_current != "s":
            new_team = input("   Novo Team ID (ou deixe em branco): ").strip()
            if new_team:
                env_vars["LINEAR_TEAM_ID"] = new_team
            elif "LINEAR_TEAM_ID" in env_vars:
                del env_vars["LINEAR_TEAM_ID"]
    else:
        new_team = input("   Team ID (ou deixe em branco): ").strip()
        if new_team:
            env_vars["LINEAR_TEAM_ID"] = new_team
    
    # Project ID (opcional)
    print("\n3️⃣ Project ID (Opcional)")
    print("   Deixe em branco se não usar projetos\n")
    
    current_project = env_vars.get("LINEAR_PROJECT_ID", "")
    if current_project:
        print(f"   Project ID atual: {current_project}")
        use_current = input("   Usar Project ID atual? (s/n): ").lower().strip()
        if use_current != "s":
            new_project = input("   Novo Project ID (ou deixe em branco): ").strip()
            if new_project:
                env_vars["LINEAR_PROJECT_ID"] = new_project
            elif "LINEAR_PROJECT_ID" in env_vars:
                del env_vars["LINEAR_PROJECT_ID"]
    else:
        new_project = input("   Project ID (ou deixe em branco): ").strip()
        if new_project:
            env_vars["LINEAR_PROJECT_ID"] = new_project
    
    # Salvar .env
    print(f"\n💾 Salvando configurações em {env_path}...")
    
    # Ler arquivo completo para preservar comentários
    lines = []
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    
    # Atualizar ou adicionar variáveis
    updated_keys = set()
    new_lines = []
    
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and "=" in stripped:
            key = stripped.split("=")[0]
            if key.startswith("LINEAR_"):
                if key in env_vars:
                    new_lines.append(f"{key}={env_vars[key]}\n")
                    updated_keys.add(key)
                continue
        new_lines.append(line)
    
    # Adicionar variáveis novas
    linear_section_found = False
    for i, line in enumerate(new_lines):
        if "LINEAR" in line.upper() and "#" in line:
            linear_section_found = True
        elif linear_section_found and line.strip().startswith("#") and "LINEAR" not in line.upper():
            # Adicionar antes desta linha
            for key in ["LINEAR_API_KEY", "LINEAR_TEAM_ID", "LINEAR_PROJECT_ID"]:
                if key not in updated_keys and key in env_vars:
                    new_lines.insert(i, f"{key}={env_vars[key]}\n")
                    updated_keys.add(key)
            break
    
    # Se não encontrou seção LINEAR, adicionar no final
    if not linear_section_found:
        new_lines.append("\n#*****************************************************************\n")
        new_lines.append("# LINEAR\n")
        new_lines.append("#*****************************************************************\n")
        for key in ["LINEAR_API_KEY", "LINEAR_TEAM_ID", "LINEAR_PROJECT_ID"]:
            if key in env_vars:
                new_lines.append(f"{key}={env_vars[key]}\n")
    
    # Escrever arquivo
    with open(env_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    
    print("✅ Configuração salva!")
    print(f"\n📋 Variáveis configuradas:")
    print(f"   LINEAR_API_KEY: {'✅' if env_vars.get('LINEAR_API_KEY') else '❌'}")
    print(f"   LINEAR_TEAM_ID: {'✅' if env_vars.get('LINEAR_TEAM_ID') else '⚠️ (opcional)'}")
    print(f"   LINEAR_PROJECT_ID: {'✅' if env_vars.get('LINEAR_PROJECT_ID') else '⚠️ (opcional)'}")
    
    print("\n🚀 Próximo passo:")
    print("   python scripts/send_issues_to_linear.py")

if __name__ == "__main__":
    setup_linear()

