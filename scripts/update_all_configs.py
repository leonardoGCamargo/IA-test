"""
Script para atualizar todas as configurações do .env
"""

import os
import sys
import re
from pathlib import Path

def update_env_file():
    """Atualiza o arquivo .env com todas as novas configurações."""
    project_root = Path(__file__).parent.parent
    env_file = project_root / ".env"
    
    # Todas as novas configurações
    new_configs = {
        # Google API Key
        "GOOGLE_API_KEY": "AIzaSyD7lSqUzy-xvlP3sQHf0IaqAnemtgOqoeM",
        
        # Neon
        "NEON_PROJECT_ID": "napi_jyp0h0270gydb0xvzyei2msvd5dcyv2uvb7l4lig665dx4rgd1cjh9znfw3h5x8s",
        
        # MongoDB
        "MONGODB_URI": "mongodb+srv://DBLEONARDO:<@1Leonardo0409>@lgian.ru8ds53.mongodb.net/",
        "MONGODB_DATABASE": "default",  # Pode ser ajustado depois
        "MONGODB_ATLAS": "true",  # É Atlas (mongodb+srv://)
    }
    
    # Configurações para comentar (AWS - não vai usar)
    configs_to_comment = [
        "AWS_ACCESS_KEY_ID",
        "AWS_SECRET_ACCESS_KEY",
        "AWS_DEFAULT_REGION"
    ]
    
    # Lê arquivo existente
    env_lines = []
    if env_file.exists():
        with open(env_file, 'r', encoding='utf-8') as f:
            env_lines = f.readlines()
    else:
        # Se não existe, cria a partir do exemplo
        example_file = project_root / "config" / "env.example"
        if example_file.exists():
            with open(example_file, 'r', encoding='utf-8') as f:
                env_lines = f.readlines()
    
    # Rastreia quais foram atualizadas
    updated = {key: False for key in new_configs.keys()}
    commented = {key: False for key in configs_to_comment}
    
    new_lines = []
    
    for line in env_lines:
        line_stripped = line.strip()
        
        # Atualiza variáveis existentes
        updated_line = False
        for key, value in new_configs.items():
            # Verifica se a linha começa com a chave (com ou sem espaços)
            if re.match(rf'^\s*{re.escape(key)}\s*=', line):
                new_lines.append(f"{key}={value}\n")
                updated[key] = True
                updated_line = True
                break
        
        # Comenta variáveis AWS se não atualizadas
        if not updated_line:
            for key in configs_to_comment:
                if re.match(rf'^\s*{re.escape(key)}\s*=', line) and not line.strip().startswith('#'):
                    new_lines.append(f"#{line}")
                    commented[key] = True
                    updated_line = True
                    break
        
        if not updated_line:
            new_lines.append(line)
    
    # Adiciona variáveis que não existiam
    if not all(updated.values()):
        # Encontra seções apropriadas para inserir
        insert_positions = {}
        
        for i, line in enumerate(new_lines):
            # Google
            if "# GOOGLE" in line.upper() or "#*****************************************************************\n# GOOGLE" in line.upper():
                insert_positions["GOOGLE"] = i + 1
            # Neon
            elif "# NEON" in line.upper():
                insert_positions["NEON"] = i + 1
            # MongoDB
            elif "# MONGODB" in line.upper():
                insert_positions["MONGODB"] = i + 1
        
        # Insere variáveis faltantes
        for key, value in new_configs.items():
            if not updated[key]:
                section = None
                if "GOOGLE" in key:
                    section = "GOOGLE"
                elif "NEON" in key:
                    section = "NEON"
                elif "MONGODB" in key:
                    section = "MONGODB"
                
                if section and section in insert_positions:
                    # Encontra o final da seção
                    pos = insert_positions[section]
                    for j in range(pos, len(new_lines)):
                        if new_lines[j].strip() and not new_lines[j].startswith("#") and section not in new_lines[j].upper():
                            pos = j
                            break
                    new_lines.insert(pos, f"{key}={value}\n")
                    updated[key] = True
                else:
                    # Adiciona no final se não encontrou seção
                    new_lines.append(f"{key}={value}\n")
                    updated[key] = True
    
    # Salva arquivo
    with open(env_file, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print("=" * 70)
    print("✅ Arquivo .env atualizado com sucesso!")
    print("=" * 70)
    print()
    print("📋 Configurações aplicadas:")
    print()
    
    for key, value in new_configs.items():
        if updated[key]:
            if "PASSWORD" in key.upper() or "KEY" in key.upper() or "URI" in key.upper():
                display_value = value[:20] + "..." if len(value) > 20 else value
                print(f"   ✅ {key}={display_value}")
            else:
                print(f"   ✅ {key}={value}")
        else:
            print(f"   ⚠️  {key} (não encontrado, adicionado no final)")
    
    print()
    print("📋 Configurações comentadas (AWS - não será usado):")
    for key in configs_to_comment:
        if commented[key]:
            print(f"   ✅ {key} (comentado)")
        else:
            print(f"   ⚠️  {key} (não encontrado para comentar)")
    
    return True

if __name__ == "__main__":
    try:
        update_env_file()
        print()
        print("=" * 70)
        print("✅ Todas as configurações foram aplicadas!")
        print("=" * 70)
        print()
        print("💡 Próximos passos:")
        print("   1. Verifique o arquivo .env")
        print("   2. Execute: python scripts/check_missing_keys.py")
        print("   3. Teste as conexões conforme necessário")
        print()
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

