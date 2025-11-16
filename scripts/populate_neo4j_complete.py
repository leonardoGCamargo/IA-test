"""
Script completo para popular o Neo4j com TODOS os dados do projeto IA-Test.

Este script mapeia:
- Agentes e suas configurações
- Serviços Docker e portas
- MCPs e suas configurações
- Relacionamentos entre componentes
- Configurações e parâmetros
- Itens que não conseguem ser conectados (lista de ignorados)

Uso:
    python scripts/populate_neo4j_complete.py
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
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
except ImportError:
    print("ERRO: Biblioteca neo4j não encontrada. Instale com: pip install neo4j")
    sys.exit(1)

# Lista de itens ignorados (não conectados)
ignored_items = {
    "agents": [],
    "services": [],
    "mcps": [],
    "configs": [],
    "files": [],
    "relationships": []
}

def log_ignored(category: str, item: Dict, reason: str):
    """Registra um item ignorado."""
    ignored_items[category].append({
        "item": item,
        "reason": reason,
        "timestamp": datetime.now().isoformat()
    })

def create_complete_graph():
    """Cria o grafo completo do projeto no Neo4j."""
    print("=" * 80)
    print("POPULANDO NEO4J COM DADOS COMPLETOS DO PROJETO IA-TEST")
    print("=" * 80)
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
            # ============================================
            # 1. PROJETO PRINCIPAL
            # ============================================
            print("1. Criando nó do Projeto IA-Test...")
            session.run("""
                MERGE (p:Project {id: 'ia-test'})
                SET p.name = 'IA-Test',
                    p.description = 'Sistema de agentes IA com GraphRAG e integração Neo4j',
                    p.version = '1.0.0',
                    p.created_at = datetime(),
                    p.repository = 'https://github.com/seu-usuario/IA-test',
                    p.architecture = 'Microservices com Docker Compose',
                    p.llm_framework = 'LangChain + LangGraph',
                    p.graph_database = 'Neo4j 5.26'
                RETURN p.name as name
            """)
            print("   OK - Projeto criado")
            print()
            
            # ============================================
            # 2. AGENTES DO SISTEMA
            # ============================================
            print("2. Criando nós dos Agentes...")
            agents_data = [
                {
                    "id": "orchestrator",
                    "name": "Orchestrator",
                    "description": "Coordenador central com planejamento inteligente",
                    "type": "orchestrator",
                    "file": "src/agents/orchestrator.py",
                    "uses_llm": True,
                    "llm_config": os.getenv("LLM", "llama2"),
                    "dependencies": ["langchain", "langgraph"],
                    "capabilities": ["Planejamento", "Coordenação", "Distribuição de tarefas"]
                },
                {
                    "id": "neo4j-graphrag",
                    "name": "Neo4j GraphRAG",
                    "description": "GraphRAG com Neo4j para busca semântica em grafos",
                    "type": "graphrag",
                    "file": "src/agents/mcp_neo4j_integration.py",
                    "uses_llm": True,
                    "llm_config": os.getenv("LLM", "llama2"),
                    "dependencies": ["langchain-neo4j", "neo4j"],
                    "capabilities": ["GraphRAG", "Busca semântica", "Consultas Cypher"]
                },
                {
                    "id": "mcp-manager",
                    "name": "MCP Manager",
                    "description": "Gerenciamento de servidores MCP (Model Context Protocol)",
                    "type": "mcp_manager",
                    "file": "src/agents/mcp_manager.py",
                    "uses_llm": False,
                    "dependencies": ["mcp"],
                    "capabilities": ["Gerenciamento MCP", "Health checks", "Listagem de recursos"]
                },
                {
                    "id": "system-health",
                    "name": "System Health Agent",
                    "description": "Diagnóstico, monitoramento e resolução de problemas",
                    "type": "system_health",
                    "file": "src/agents/system_health_agent.py",
                    "uses_llm": False,
                    "dependencies": [],
                    "capabilities": ["Diagnóstico", "Monitoramento", "Resolução"]
                },
                {
                    "id": "db-manager",
                    "name": "DB Manager",
                    "description": "Gerenciamento de bancos de dados",
                    "type": "db_manager",
                    "file": "src/agents/db_manager.py",
                    "uses_llm": False,
                    "dependencies": ["neo4j", "psycopg2", "pymongo"],
                    "capabilities": ["Conexão com bancos", "Execução de queries", "Gerenciamento"]
                },
                {
                    "id": "git-integration",
                    "name": "Git Integration",
                    "description": "Integração com Git/GitHub",
                    "type": "git_integration",
                    "file": "src/agents/git_integration.py",
                    "uses_llm": False,
                    "dependencies": ["gitpython"],
                    "capabilities": ["Commits", "Branches", "PRs", "Operações Git"]
                },
                {
                    "id": "obsidian-integration",
                    "name": "Obsidian Integration",
                    "description": "Integração com Obsidian para gerenciamento de notas",
                    "type": "obsidian",
                    "file": "src/agents/mcp_obsidian_integration.py",
                    "uses_llm": False,
                    "dependencies": [],
                    "capabilities": ["Criação de notas", "Gerenciamento de vault", "Links entre notas"]
                },
                {
                    "id": "kestra-agent",
                    "name": "Kestra Agent",
                    "description": "Orquestração de workflows Kestra",
                    "type": "kestra",
                    "file": "src/agents/mcp_kestra_integration.py",
                    "uses_llm": False,
                    "dependencies": ["requests"],
                    "capabilities": ["Criação de workflows", "Execução", "Monitoramento"]
                },
                {
                    "id": "docker-integration",
                    "name": "Docker Integration",
                    "description": "Gerenciamento de containers Docker",
                    "type": "docker_integration",
                    "file": "src/agents/mcp_docker_integration.py",
                    "uses_llm": False,
                    "dependencies": ["docker"],
                    "capabilities": ["Listagem de containers", "Gerenciamento", "Health checks"]
                }
            ]
            
            for agent in agents_data:
                try:
                    # Verifica se o arquivo existe
                    file_path = project_root / agent["file"]
                    file_exists = file_path.exists()
                    
                    session.run("""
                        MERGE (a:Agent {id: $id})
                        SET a.name = $name,
                            a.description = $description,
                            a.type = $type,
                            a.file = $file,
                            a.file_exists = $file_exists,
                            a.uses_llm = $uses_llm,
                            a.llm_config = $llm_config,
                            a.dependencies = $dependencies,
                            a.capabilities = $capabilities,
                            a.created_at = datetime(),
                            a.updated_at = datetime()
                        WITH a
                        MATCH (p:Project {id: 'ia-test'})
                        MERGE (p)-[:HAS_AGENT]->(a)
                        RETURN a.name as name
                    """, {
                        **agent,
                        "file_exists": file_exists,
                        "llm_config": agent.get("llm_config", ""),
                        "dependencies": agent.get("dependencies", []),
                        "capabilities": agent.get("capabilities", [])
                    })
                    print(f"   OK - {agent['name']} ({agent['type']})")
                except Exception as e:
                    log_ignored("agents", agent, str(e))
                    print(f"   IGNORADO - {agent['name']}: {e}")
            
            print()
            
            # ============================================
            # 3. SERVIÇOS DOCKER
            # ============================================
            print("3. Criando nós dos Serviços Docker...")
            services_data = [
                {
                    "id": "neo4j-service",
                    "name": "Neo4j Database",
                    "description": "Banco de dados de grafos Neo4j",
                    "port_http": 7474,
                    "port_bolt": 7687,
                    "type": "database",
                    "image": "neo4j:5.26",
                    "profile": "core",
                    "healthcheck": True
                },
                {
                    "id": "api-service",
                    "name": "FastAPI",
                    "description": "API REST para o sistema",
                    "port": 8504,
                    "type": "api",
                    "image": "langchain/langchain:latest",
                    "profile": "core",
                    "healthcheck": True
                },
                {
                    "id": "frontend-service",
                    "name": "Frontend (Svelte)",
                    "description": "Interface frontend Svelte",
                    "port": 8505,
                    "type": "frontend",
                    "image": "node:alpine",
                    "profile": "core",
                    "healthcheck": False
                },
                {
                    "id": "dashboard-service",
                    "name": "Agent Dashboard",
                    "description": "Dashboard Streamlit para gerenciamento de agentes",
                    "port": 8507,
                    "type": "dashboard",
                    "image": "langchain/langchain:latest",
                    "profile": "core",
                    "healthcheck": True
                },
                {
                    "id": "kestra-service",
                    "name": "Kestra",
                    "description": "Orquestração de workflows",
                    "port": 8080,
                    "type": "workflow",
                    "image": "kestra/kestra:latest",
                    "profile": "tools",
                    "healthcheck": True
                },
                {
                    "id": "kestra-postgres",
                    "name": "Kestra PostgreSQL",
                    "description": "Banco de dados PostgreSQL para Kestra",
                    "port": 5432,
                    "type": "database",
                    "image": "postgres:16",
                    "profile": "tools",
                    "healthcheck": False
                },
                {
                    "id": "mcp-manager-service",
                    "name": "MCP Manager UI",
                    "description": "Interface Streamlit para gerenciamento MCP",
                    "port": 8506,
                    "type": "dashboard",
                    "image": "python:3.11",
                    "profile": "tools",
                    "healthcheck": True
                },
                {
                    "id": "bot-service",
                    "name": "Bot Streamlit",
                    "description": "Aplicação bot Streamlit",
                    "port": 8501,
                    "type": "streamlit",
                    "image": "langchain/langchain:latest",
                    "profile": "streamlit",
                    "healthcheck": False
                },
                {
                    "id": "loader-service",
                    "name": "Loader Streamlit",
                    "description": "Aplicação loader Streamlit",
                    "port": 8502,
                    "type": "streamlit",
                    "image": "langchain/langchain:latest",
                    "profile": "streamlit",
                    "healthcheck": False
                },
                {
                    "id": "pdf-bot-service",
                    "name": "PDF Bot Streamlit",
                    "description": "Aplicação PDF bot Streamlit",
                    "port": 8503,
                    "type": "streamlit",
                    "image": "langchain/langchain:latest",
                    "profile": "streamlit",
                    "healthcheck": False
                }
            ]
            
            for service in services_data:
                try:
                    session.run("""
                        MERGE (s:Service {id: $id})
                        SET s.name = $name,
                            s.description = $description,
                            s.port = $port,
                            s.port_http = $port_http,
                            s.port_bolt = $port_bolt,
                            s.type = $type,
                            s.image = $image,
                            s.profile = $profile,
                            s.healthcheck = $healthcheck,
                            s.created_at = datetime(),
                            s.updated_at = datetime()
                        WITH s
                        MATCH (p:Project {id: 'ia-test'})
                        MERGE (p)-[:HAS_SERVICE]->(s)
                        RETURN s.name as name
                    """, {
                        **service,
                        "port": service.get("port", service.get("port_http", 0)),
                        "port_http": service.get("port_http"),
                        "port_bolt": service.get("port_bolt")
                    })
                    print(f"   OK - {service['name']} (porta {service.get('port', service.get('port_http', 'N/A'))})")
                except Exception as e:
                    log_ignored("services", service, str(e))
                    print(f"   IGNORADO - {service['name']}: {e}")
            
            print()
            
            # ============================================
            # 4. MCPS (Model Context Protocol)
            # ============================================
            print("4. Criando nós dos MCPs...")
            mcp_file = project_root / "mcp_servers.json"
            if mcp_file.exists():
                try:
                    with open(mcp_file, 'r', encoding='utf-8') as f:
                        mcps_data = json.load(f)
                    
                    for mcp_id, mcp_info in mcps_data.items():
                        try:
                            session.run("""
                                MERGE (m:MCP {id: $id})
                                SET m.name = $name,
                                    m.description = $description,
                                    m.command = $command,
                                    m.args = $args,
                                    m.enabled = $enabled,
                                    m.created_at = datetime(),
                                    m.updated_at = datetime()
                                WITH m
                                MATCH (p:Project {id: 'ia-test'})
                                MERGE (p)-[:HAS_MCP]->(m)
                                RETURN m.name as name
                            """, {
                                "id": mcp_id,
                                "name": mcp_info.get("name", mcp_id),
                                "description": mcp_info.get("description", ""),
                                "command": mcp_info.get("command", ""),
                                "args": mcp_info.get("args", []),
                                "enabled": mcp_info.get("enabled", False)
                            })
                            print(f"   OK - {mcp_info.get('name', mcp_id)} ({'habilitado' if mcp_info.get('enabled') else 'desabilitado'})")
                        except Exception as e:
                            log_ignored("mcps", mcp_info, str(e))
                            print(f"   IGNORADO - {mcp_id}: {e}")
                except Exception as e:
                    log_ignored("files", {"file": str(mcp_file)}, f"Erro ao ler arquivo: {e}")
                    print(f"   ERRO ao ler mcp_servers.json: {e}")
            else:
                log_ignored("files", {"file": str(mcp_file)}, "Arquivo não encontrado")
                print(f"   AVISO - mcp_servers.json não encontrado")
            
            print()
            
            # ============================================
            # 5. CONFIGURAÇÕES E VARIÁVEIS DE AMBIENTE
            # ============================================
            print("5. Criando nós de Configurações...")
            configs = {
                "llm": {
                    "name": "LLM Configuration",
                    "value": os.getenv("LLM", "llama2"),
                    "type": "llm",
                    "description": "Modelo LLM principal"
                },
                "embedding_model": {
                    "name": "Embedding Model",
                    "value": os.getenv("EMBEDDING_MODEL", "sentence_transformer"),
                    "type": "embedding",
                    "description": "Modelo de embedding"
                },
                "neo4j_uri": {
                    "name": "Neo4j URI",
                    "value": os.getenv("NEO4J_URI", "neo4j://localhost:7687"),
                    "type": "database",
                    "description": "URI de conexão Neo4j"
                },
                "ollama_url": {
                    "name": "Ollama Base URL",
                    "value": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
                    "type": "llm_service",
                    "description": "URL base do Ollama"
                }
            }
            
            for config_id, config_data in configs.items():
                try:
                    session.run("""
                        MERGE (c:Config {id: $id})
                        SET c.name = $name,
                            c.value = $value,
                            c.type = $type,
                            c.description = $description,
                            c.created_at = datetime()
                        WITH c
                        MATCH (p:Project {id: 'ia-test'})
                        MERGE (p)-[:HAS_CONFIG]->(c)
                        RETURN c.name as name
                    """, {
                        "id": config_id,
                        **config_data
                    })
                    print(f"   OK - {config_data['name']}: {config_data['value']}")
                except Exception as e:
                    log_ignored("configs", config_data, str(e))
                    print(f"   IGNORADO - {config_id}: {e}")
            
            print()
            
            # ============================================
            # 6. RELACIONAMENTOS ENTRE COMPONENTES
            # ============================================
            print("6. Criando relacionamentos entre componentes...")
            relationships = [
                # Agentes -> Serviços
                ("neo4j-graphrag", "neo4j-service", "USES", "Conecta ao banco Neo4j"),
                ("orchestrator", "neo4j-service", "USES", "Usa Neo4j para armazenar dados"),
                ("api-service", "neo4j-service", "CONNECTS_TO", "API conecta ao Neo4j"),
                ("dashboard-service", "api-service", "CONNECTS_TO", "Dashboard usa API"),
                ("orchestrator", "kestra-service", "ORCHESTRATES", "Orquestra workflows Kestra"),
                ("kestra-service", "kestra-postgres", "USES", "Kestra usa PostgreSQL"),
                
                # Agentes -> MCPs
                ("mcp-manager", "neo4j", "MANAGES", "Gerencia servidor MCP Neo4j"),
                ("mcp-manager", "obsidian", "MANAGES", "Gerencia servidor MCP Obsidian"),
                ("mcp-manager", "git", "MANAGES", "Gerencia servidor MCP Git"),
                ("obsidian-integration", "obsidian", "USES", "Usa MCP Obsidian"),
                ("git-integration", "git", "USES", "Usa MCP Git"),
                ("neo4j-graphrag", "neo4j", "USES", "Usa MCP Neo4j"),
                
                # Agentes -> Agentes
                ("orchestrator", "neo4j-graphrag", "COORDINATES", "Coordena GraphRAG"),
                ("orchestrator", "mcp-manager", "COORDINATES", "Coordena MCP Manager"),
                ("orchestrator", "system-health", "COORDINATES", "Coordena System Health"),
                ("orchestrator", "db-manager", "COORDINATES", "Coordena DB Manager"),
                ("system-health", "db-manager", "MONITORS", "Monitora DB Manager"),
                ("system-health", "mcp-manager", "MONITORS", "Monitora MCP Manager"),
                
                # Projeto -> Configurações
                ("ia-test", "llm", "HAS_CONFIG", "Projeto tem configuração LLM"),
                ("ia-test", "embedding_model", "HAS_CONFIG", "Projeto tem configuração de embedding"),
                ("ia-test", "neo4j_uri", "HAS_CONFIG", "Projeto tem configuração Neo4j"),
                
                # Agentes -> Configurações
                ("orchestrator", "llm", "USES_CONFIG", "Orchestrator usa configuração LLM"),
                ("neo4j-graphrag", "llm", "USES_CONFIG", "GraphRAG usa configuração LLM"),
                ("neo4j-graphrag", "embedding_model", "USES_CONFIG", "GraphRAG usa configuração de embedding")
            ]
            
            created_rels = 0
            for source_id, target_id, rel_type, description in relationships:
                try:
                    result = session.run("""
                        MATCH (source {id: $source_id})
                        MATCH (target {id: $target_id})
                        MERGE (source)-[r:%s {description: $description}]->(target)
                        SET r.created_at = datetime()
                        RETURN r
                    """ % rel_type, {
                        "source_id": source_id,
                        "target_id": target_id,
                        "description": description
                    })
                    
                    if result.single():
                        created_rels += 1
                except Exception as e:
                    log_ignored("relationships", {
                        "source": source_id,
                        "target": target_id,
                        "type": rel_type
                    }, str(e))
                    print(f"   IGNORADO - {source_id} -> {target_id} ({rel_type}): {e}")
            
            print(f"   OK - {created_rels} relacionamentos criados")
            print()
            
            # ============================================
            # 7. ESTATÍSTICAS FINAIS
            # ============================================
            print("7. Estatísticas do Grafo:")
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
        
        # ============================================
        # 8. SALVAR LISTA DE IGNORADOS
        # ============================================
        ignored_file = project_root / "NEO4J_IGNORED_ITEMS.json"
        with open(ignored_file, 'w', encoding='utf-8') as f:
            json.dump(ignored_items, f, indent=2, ensure_ascii=False, default=str)
        
        total_ignored = sum(len(items) for items in ignored_items.values())
        
        print("=" * 80)
        print("SUCESSO! Neo4j populado com dados completos do projeto")
        print("=" * 80)
        print()
        print(f"Total de itens ignorados: {total_ignored}")
        if total_ignored > 0:
            print(f"Lista de ignorados salva em: {ignored_file}")
            print()
            print("Itens ignorados por categoria:")
            for category, items in ignored_items.items():
                if items:
                    print(f"  - {category}: {len(items)} itens")
        print()
        print("Acesse o Neo4j Browser em: http://localhost:7474")
        print("Execute a query: MATCH (n) RETURN n LIMIT 50")
        print()
        print("Queries úteis:")
        print("  - Ver todos os agentes: MATCH (a:Agent) RETURN a")
        print("  - Ver todos os serviços: MATCH (s:Service) RETURN s")
        print("  - Ver relacionamentos: MATCH (a)-[r]->(b) RETURN a, r, b LIMIT 25")
        
    except Exception as e:
        print(f"ERRO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    create_complete_graph()

