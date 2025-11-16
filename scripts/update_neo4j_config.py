"""
Script para atualizar configurações do Neo4j Aura no .env
"""

import os
import sys
from pathlib import Path

def update_env_file():
    """Atualiza o arquivo .env com as novas configurações do Neo4j Aura."""
    project_root = Path(__file__).parent.parent
    env_file = project_root / ".env"
    
    # Novas configurações
    new_config = {
        "NEO4J_URI": "neo4j+s://71de7683.databases.neo4j.io",
        "NEO4J_USERNAME": "neo4j",
        "NEO4J_PASSWORD": "zoit_O9j_sV80eNIuvU3OKXVYWAmCmaoAdBzOhBdWgM",
        "NEO4J_DATABASE": "neo4j",
        "AURA_INSTANCEID": "71de7683",
        "AURA_INSTANCENAME": "My instance"
    }
    
    # Lê arquivo existente
    env_lines = []
    if env_file.exists():
        with open(env_file, 'r', encoding='utf-8') as f:
            env_lines = f.readlines()
    
    # Atualiza ou adiciona variáveis
    updated = {key: False for key in new_config.keys()}
    
    new_lines = []
    in_neo4j_section = False
    
    for line in env_lines:
        # Detecta seção Neo4j
        if "# Neo4j" in line or "#*****************************************************************\n# Neo4j" in line:
            in_neo4j_section = True
        
        # Atualiza variáveis existentes
        updated_line = False
        for key, value in new_config.items():
            if line.startswith(f"{key}="):
                new_lines.append(f"{key}={value}\n")
                updated[key] = True
                updated_line = True
                break
        
        if not updated_line:
            new_lines.append(line)
    
    # Adiciona variáveis que não existiam
    if not all(updated.values()):
        # Encontra onde inserir (após seção Neo4j ou no final)
        insert_pos = len(new_lines)
        for i, line in enumerate(new_lines):
            if "# Neo4j" in line or "NEO4J_" in line:
                # Encontra o final da seção Neo4j
                for j in range(i, len(new_lines)):
                    if new_lines[j].strip() and not new_lines[j].startswith("#") and "NEO4J_" not in new_lines[j]:
                        insert_pos = j
                        break
                break
        
        # Adiciona variáveis faltantes
        missing_vars = [f"{key}={value}\n" for key, value in new_config.items() if not updated[key]]
        if missing_vars:
            # Adiciona comentário se necessário
            if insert_pos == len(new_lines) or not new_lines[insert_pos-1].startswith("#"):
                new_lines.insert(insert_pos, "# Neo4j Aura DB Configuration\n")
                insert_pos += 1
            # Insere variáveis
            for var in missing_vars:
                new_lines.insert(insert_pos, var)
                insert_pos += 1
    
    # Salva arquivo
    with open(env_file, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"✅ Arquivo .env atualizado: {env_file}")
    print()
    print("📋 Configurações aplicadas:")
    for key, value in new_config.items():
        if key == "NEO4J_PASSWORD":
            print(f"   {key}={value[:10]}...")
        else:
            print(f"   {key}={value}")
    
    return True

if __name__ == "__main__":
    try:
        update_env_file()
        print()
        print("🧪 Testando conexão...")
        print()
        
        # Testa conexão
        import subprocess
        result = subprocess.run(
            [sys.executable, str(Path(__file__).parent.parent / "scripts" / "test_neo4j_connection.py")],
            cwd=Path(__file__).parent.parent
        )
        
        if result.returncode == 0:
            print()
            print("=" * 60)
            print("✅ Configuração concluída com sucesso!")
            print("=" * 60)
        else:
            print()
            print("⚠️ Configuração salva, mas teste de conexão falhou.")
            print("   Verifique se a biblioteca neo4j está instalada:")
            print("   pip install neo4j")
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


