"""
Script para popular o Neo4j com dados iniciais do projeto.

Uso:
    python scripts/populate_neo4j_initial.py
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Adiciona o diretório raiz ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Carrega variáveis de ambiente
root_env = project_root / ".env"
if root_env.exists():
    load_dotenv(root_env)

try:
    from neo4j import GraphDatabase
    from src.agents.mcp_neo4j_integration import get_neo4j_manager
except ImportError as e:
    print(f"ERRO: Biblioteca não encontrada: {e}")
    print("Instale com: pip install neo4j langchain-neo4j")
    sys.exit(1)

def create_initial_data():
    """Cria dados iniciais no Neo4j."""
    print("=" * 70)
    print("POPULANDO NEO4J COM DADOS INICIAIS")
    print("=" * 70)
    print()
    
    # Conecta ao Neo4j
    uri = os.getenv("NEO4J_URI", "neo4j://localhost:7687")
    username = os.getenv("NEO4J_USERNAME", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "password")
    
    print(f"Conectando ao Neo4j...")
    print(f"  URI: {uri}")
    print(f"  Username: {username}")
    print()
    
    try:
        driver = GraphDatabase.driver(uri, auth=(username, password))
        
        with driver.session() as session:
            # 1. Criar nó do Projeto
            print("1. Criando nó do Projeto IA-Test...")
            session.run("""
                MERGE (p:Project {id: 'ia-test'})
                SET p.name = 'IA-Test',
                    p.description = 'Sistema de agentes IA com GraphRAG e integração Neo4j',
                    p.version = '1.0.0',
                    p.created_at = datetime()
                RETURN p.name as name
            """)
            print("   OK - Projeto criado")
            print()
            
            # 2. Criar nós dos principais agentes
            print("2. Criando nós dos Agentes...")
            agents = [
                {
                    "id": "orchestrator",
                    "name": "Orchestrator",
                    "description": "Coordenador central com planejamento inteligente",
                    "type": "orchestrator"
                },
                {
                    "id": "neo4j-graphrag",
                    "name": "Neo4j GraphRAG",
                    "description": "GraphRAG com Neo4j para busca semântica em grafos",
                    "type": "graphrag"
                },
                {
                    "id": "mcp-manager",
                    "name": "MCP Manager",
                    "description": "Gerenciamento de servidores MCP (Model Context Protocol)",
                    "type": "mcp_manager"
                },
                {
                    "id": "system-health",
                    "name": "System Health Agent",
                    "description": "Diagnóstico, monitoramento e resolução de problemas",
                    "type": "system_health"
                }
            ]
            
            for agent in agents:
                session.run("""
                    MERGE (a:Agent {id: $id})
                    SET a.name = $name,
                        a.description = $description,
                        a.type = $type,
                        a.created_at = datetime()
                    WITH a
                    MATCH (p:Project {id: 'ia-test'})
                    MERGE (p)-[:HAS_AGENT]->(a)
                    RETURN a.name as name
                """, agent)
                print(f"   OK - {agent['name']}")
            
            print()
            
            # 3. Criar nós dos serviços Docker
            print("3. Criando nós dos Serviços Docker...")
            services = [
                {
                    "id": "neo4j-service",
                    "name": "Neo4j Database",
                    "description": "Banco de dados de grafos Neo4j",
                    "port": 7687,
                    "type": "database"
                },
                {
                    "id": "api-service",
                    "name": "FastAPI",
                    "description": "API REST para o sistema",
                    "port": 8504,
                    "type": "api"
                },
                {
                    "id": "dashboard-service",
                    "name": "Agent Dashboard",
                    "description": "Dashboard Streamlit para gerenciamento de agentes",
                    "port": 8507,
                    "type": "dashboard"
                },
                {
                    "id": "kestra-service",
                    "name": "Kestra",
                    "description": "Orquestração de workflows",
                    "port": 8080,
                    "type": "workflow"
                }
            ]
            
            for service in services:
                session.run("""
                    MERGE (s:Service {id: $id})
                    SET s.name = $name,
                        s.description = $description,
                        s.port = $port,
                        s.type = $type,
                        s.created_at = datetime()
                    WITH s
                    MATCH (p:Project {id: 'ia-test'})
                    MERGE (p)-[:HAS_SERVICE]->(s)
                    RETURN s.name as name
                """, service)
                print(f"   OK - {service['name']} (porta {service['port']})")
            
            print()
            
            # 4. Criar relacionamentos entre agentes e serviços
            print("4. Criando relacionamentos...")
            relationships = [
                ("neo4j-graphrag", "neo4j-service", "USES"),
                ("orchestrator", "neo4j-service", "USES"),
                ("api-service", "neo4j-service", "CONNECTS_TO"),
                ("dashboard-service", "api-service", "CONNECTS_TO"),
                ("orchestrator", "kestra-service", "ORCHESTRATES")
            ]
            
            for source_id, target_id, rel_type in relationships:
                session.run(f"""
                    MATCH (source {{id: $source_id}})
                    MATCH (target {{id: $target_id}})
                    MERGE (source)-[:{rel_type}]->(target)
                """, {"source_id": source_id, "target_id": target_id})
            
            print(f"   OK - {len(relationships)} relacionamentos criados")
            print()
            
            # 5. Estatísticas finais
            print("5. Estatísticas do Grafo:")
            stats = session.run("""
                MATCH (n)
                RETURN labels(n)[0] as label, count(n) as count
                ORDER BY count DESC
            """).data()
            
            for stat in stats:
                print(f"   {stat['label']}: {stat['count']} nós")
            
            rel_count = session.run("MATCH ()-[r]->() RETURN count(r) as count").single()['count']
            print(f"   Relacionamentos: {rel_count}")
            print()
            
        driver.close()
        
        print("=" * 70)
        print("SUCESSO! Neo4j populado com dados iniciais")
        print("=" * 70)
        print()
        print("Acesse o Neo4j Browser em: http://localhost:7474")
        print("Execute a query: MATCH (n) RETURN n LIMIT 25")
        
    except Exception as e:
        print(f"ERRO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    create_initial_data()

