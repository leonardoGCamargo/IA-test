"""
Script interativo para configurar conexão com Neo4j Aura DB.

Uso:
    python scripts/setup_aura_db.py
"""

import os
import sys
from pathlib import Path

def setup_aura_db():
    """Configura conexão com Aura DB interativamente."""
    print("=" * 60)
    print("🔗 Configuração do Neo4j Aura DB")
    print("=" * 60)
    print()
    print("Este script irá ajudá-lo a configurar a conexão com Neo4j Aura DB.")
    print()
    
    # Solicita informações
    print("📋 Informações necessárias:")
    print("   (Você pode encontrar essas informações no console do Neo4j Aura)")
    print()
    
    uri = input("🔗 Connection URI (ex: neo4j+s://xxxxx.databases.neo4j.io): ").strip()
    if not uri:
        print("❌ URI é obrigatória!")
        return False
    
    username = input("👤 Username (geralmente 'neo4j'): ").strip() or "neo4j"
    password = input("🔒 Password: ").strip()
    if not password:
        print("❌ Password é obrigatório!")
        return False
    
    print()
    print("📝 Configuração:")
    print(f"   URI: {uri}")
    print(f"   Username: {username}")
    print(f"   Password: {'*' * len(password)}")
    print()
    
    confirm = input("✅ Confirmar e salvar no .env? (s/n): ").strip().lower()
    if confirm != 's':
        print("❌ Cancelado.")
        return False
    
    # Lê .env existente ou cria novo
    project_root = Path(__file__).parent.parent
    env_file = project_root / ".env"
    
    env_lines = []
    if env_file.exists():
        with open(env_file, 'r', encoding='utf-8') as f:
            env_lines = f.readlines()
    
    # Atualiza ou adiciona variáveis
    updated = {
        'NEO4J_URI': False,
        'NEO4J_USERNAME': False,
        'NEO4J_PASSWORD': False
    }
    
    new_lines = []
    for line in env_lines:
        if line.startswith('NEO4J_URI='):
            new_lines.append(f'NEO4J_URI={uri}\n')
            updated['NEO4J_URI'] = True
        elif line.startswith('NEO4J_USERNAME='):
            new_lines.append(f'NEO4J_USERNAME={username}\n')
            updated['NEO4J_USERNAME'] = True
        elif line.startswith('NEO4J_PASSWORD='):
            new_lines.append(f'NEO4J_PASSWORD={password}\n')
            updated['NEO4J_PASSWORD'] = True
        else:
            new_lines.append(line)
    
    # Adiciona variáveis que não existiam
    if not updated['NEO4J_URI']:
        new_lines.append(f'\n# Neo4j Aura DB\n')
        new_lines.append(f'NEO4J_URI={uri}\n')
    if not updated['NEO4J_USERNAME']:
        new_lines.append(f'NEO4J_USERNAME={username}\n')
    if not updated['NEO4J_PASSWORD']:
        new_lines.append(f'NEO4J_PASSWORD={password}\n')
    
    # Salva arquivo
    with open(env_file, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"✅ Configuração salva em: {env_file}")
    print()
    print("🧪 Testando conexão...")
    print()
    
    # Testa conexão
    import subprocess
    result = subprocess.run(
        [sys.executable, str(project_root / "scripts" / "test_neo4j_connection.py")],
        cwd=project_root
    )
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ Configuração concluída com sucesso!")
        print("=" * 60)
        print()
        print("💡 Próximos passos:")
        print("   1. Abra o Neo4j Desktop")
        print("   2. Adicione uma conexão remota com as mesmas credenciais")
        print("   3. Visualize seus dados!")
        print()
        print("📚 Veja mais em: docs/NEO4J_AURA_SETUP.md")
        return True
    else:
        print()
        print("⚠️ Configuração salva, mas teste de conexão falhou.")
        print("   Verifique as credenciais e tente novamente.")
        return False

if __name__ == "__main__":
    try:
        setup_aura_db()
    except KeyboardInterrupt:
        print("\n\n❌ Cancelado pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        sys.exit(1)

