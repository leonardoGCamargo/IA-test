"""
Script para testar conexão com Neo4j (local ou Aura DB).

Uso:
    python scripts/test_neo4j_connection.py
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Adiciona o diretório raiz ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Carrega variáveis de ambiente
# Prioridade:
# 1) .env na raiz do projeto
# 2) config/.env (modo Docker / Modo B)
root_env = project_root / ".env"
config_env = project_root / "config" / ".env"

if root_env.exists():
    load_dotenv(root_env)
elif config_env.exists():
    load_dotenv(config_env)
else:
    load_dotenv()

try:
    from neo4j import GraphDatabase
    NEO4J_AVAILABLE = True
except ImportError:
    print("ERRO: Biblioteca neo4j não instalada. Instale com: pip install neo4j")
    NEO4J_AVAILABLE = False
    sys.exit(1)

def test_connection():
    """Testa conexão com Neo4j."""
    uri = os.getenv("NEO4J_URI")
    username = os.getenv("NEO4J_USERNAME", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "password")
    
    if not uri:
        print("ERRO: NEO4J_URI não configurado nas variáveis de ambiente (.env)")
        print("\nExemplos de configuração:")
        print("   # Modo B - Neo4j em container Docker (usado dentro dos containers):")
        print("   NEO4J_URI=neo4j://database:7687")
        print("   NEO4J_USERNAME=neo4j")
        print("   NEO4J_PASSWORD=sua_senha")
        print("\n   # Para scripts locais / Neo4j Desktop conectando no container:")
        print("   NEO4J_URI=neo4j://localhost:7687")
        print("   NEO4J_USERNAME=neo4j")
        print("   NEO4J_PASSWORD=sua_senha")
        return False
    
    print("Testando conexão com Neo4j...")
    print(f"   URI: {uri}")
    print(f"   Username: {username}")
    print(f"   Password: {'*' * len(password) if password else 'não configurado'}")
    print()
    
    driver = None
    try:
        # Cria driver
        driver = GraphDatabase.driver(uri, auth=(username, password))
        
        # Testa conexão
        with driver.session() as session:
            result = session.run("RETURN 1 as test, 'Conexão OK' as message")
            record = result.single()
            
            if record:
                print("Conexao com Neo4j bem-sucedida!")
                print(f"   Teste: {record['test']}")
                print(f"   Mensagem: {record['message']}")
                
                # Tenta obter informações do servidor
                try:
                    server_info = driver.get_server_info()
                    print("\nInformacoes do Servidor:")
                    print(f"   Versao: {server_info.get('version', 'N/A')}")
                    print(f"   Protocolo: {server_info.get('protocol_version', 'N/A')}")
                except Exception:
                    pass
                
                # Conta nós e relacionamentos
                try:
                    node_count = session.run("MATCH (n) RETURN count(n) as count").single()['count']
                    rel_count = session.run("MATCH ()-[r]->() RETURN count(r) as count").single()['count']
                    print("\nEstatisticas do Grafo:")
                    print(f"   Nos: {node_count}")
                    print(f"   Relacionamentos: {rel_count}")
                except Exception as e:
                    print(f"\nAviso: nao foi possivel obter estatisticas: {e}")
                
                return True
            else:
                print("Aviso: Conexao estabelecida, mas nao retornou resultado")
                return False
                
    except Exception as e:
        print(f"ERRO na conexao: {e}")
        print()
        print("Verifique:")
        print("   1. Se a URI está correta")
        print("   2. Se o username e password estão corretos")
        print("   3. Se o Neo4j está rodando (local) ou Aura DB está ativo")
        print("   4. Se há firewall/proxy bloqueando a conexão")
        
        if "certificate" in str(e).lower() or "ssl" in str(e).lower():
            print()
            print("Para Aura DB, tente usar neo4j+ssc:// ao inves de neo4j+s:// (self-signed certificate)")
        
        return False
        
    finally:
        if driver:
            driver.close()

def test_aura_connection():
    """Testa especificamente conexão com Aura DB."""
    uri = os.getenv("NEO4J_URI", "")
    
    if "aura" in uri.lower() or "databases.neo4j.io" in uri.lower():
        print("Detectado Neo4j Aura DB")
        print("   Verificando configuracao...")
        
        if not uri.startswith("neo4j+s://") and not uri.startswith("neo4j+ssc://"):
            print("Aviso: URI do Aura DB geralmente usa neo4j+s:// ou neo4j+ssc://")
        
        return True
    return False

if __name__ == "__main__":
    print("=" * 60)
    print("TESTE DE CONEXAO NEO4J")
    print("=" * 60)
    print()
    
    # Detecta tipo de conexão
    test_aura_connection()
    print()
    
    # Testa conexão
    success = test_connection()
    
    print()
    print("=" * 60)
    if success:
        print("Teste concluido com sucesso!")
    else:
        print("Teste falhou. Verifique as configuracoes.")
    print("=" * 60)
    
    sys.exit(0 if success else 1)

