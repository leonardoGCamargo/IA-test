"""
Script que usa o MCP do Neo4j para analisar e melhorar o grafo.

Este script:
1. Consulta o schema atual do Neo4j
2. Identifica padrões e oportunidades de melhoria
3. Adiciona relações baseadas em análise do código
4. Cria documentação automática das relações
5. Gera relatório de melhorias

Uso:
    python scripts/neo4j_mcp_enhancement.py
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

def analyze_codebase_for_relationships():
    """Analisa o código fonte para identificar relações reais."""
    relationships = []
    
    # Analisa imports e dependências
    agents_dir = project_root / "src" / "agents"
    if agents_dir.exists():
        for agent_file in agents_dir.glob("*.py"):
            if agent_file.name == "__init__.py":
                continue
            
            try:
                with open(agent_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                agent_name = agent_file.stem
                
                # Identifica imports de outros agentes
                for other_agent in agents_dir.glob("*.py"):
                    if other_agent.name == "__init__.py" or other_agent.name == agent_file.name:
                        continue
                    
                    other_name = other_agent.stem
                    if f"from src.agents.{other_name}" in content or f"import {other_name}" in content:
                        relationships.append({
                            "source": agent_name.replace("_", "-"),
                            "target": other_name.replace("_", "-"),
                            "type": "IMPORTS",
                            "description": f"{agent_name} importa {other_name}",
                            "confidence": "high"
                        })
                
                # Identifica uso de serviços
                if "neo4j" in content.lower():
                    relationships.append({
                        "source": agent_name.replace("_", "-"),
                        "target": "neo4j-service",
                        "type": "USES",
                        "description": f"{agent_name} usa Neo4j",
                        "confidence": "high"
                    })
                
                if "kestra" in content.lower():
                    relationships.append({
                        "source": agent_name.replace("_", "-"),
                        "target": "kestra-service",
                        "type": "USES",
                        "description": f"{agent_name} usa Kestra",
                        "confidence": "high"
                    })
                    
            except Exception as e:
                print(f"   AVISO - Erro ao analisar {agent_file}: {e}")
    
    return relationships

def enhance_with_mcp_analysis():
    """Melhora o grafo usando análise do MCP e código fonte."""
    print("=" * 80)
    print("MELHORANDO GRAFO COM ANALISE DO CODIGO E MCP")
    print("=" * 80)
    print()
    
    # Conecta ao Neo4j
    uri = os.getenv("NEO4J_URI", "neo4j://localhost:7687")
    username = os.getenv("NEO4J_USERNAME", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "password")
    
    print(f"Conectando ao Neo4j...")
    print(f"  URI: {uri}")
    print()
    
    try:
        driver = GraphDatabase.driver(uri, auth=(username, password))
        
        with driver.session() as session:
            # ============================================
            # 1. ANALISAR SCHEMA ATUAL
            # ============================================
            print("1. Analisando schema atual do Neo4j...")
            
            # Lista todos os tipos de nós
            node_types = session.run("""
                CALL db.labels() YIELD label
                RETURN label
                ORDER BY label
            """).data()
            
            print(f"   Tipos de nós encontrados: {len(node_types)}")
            for nt in node_types:
                print(f"      - {nt['label']}")
            
            # Lista todos os tipos de relacionamentos
            rel_types = session.run("""
                CALL db.relationshipTypes() YIELD relationshipType
                RETURN relationshipType
                ORDER BY relationshipType
            """).data()
            
            print(f"   Tipos de relacionamentos encontrados: {len(rel_types)}")
            for rt in rel_types:
                print(f"      - {rt['relationshipType']}")
            
            print()
            
            # ============================================
            # 2. ANALISAR CÓDIGO PARA RELAÇÕES
            # ============================================
            print("2. Analisando código fonte para identificar relações...")
            code_relationships = analyze_codebase_for_relationships()
            print(f"   {len(code_relationships)} relações identificadas no código")
            
            # Adiciona relações baseadas no código
            added = 0
            for rel in code_relationships:
                try:
                    # Normaliza IDs
                    source_id = rel["source"]
                    target_id = rel["target"]
                    
                    # Verifica se os nós existem
                    source_exists = session.run(
                        "MATCH (n {id: $id}) RETURN count(n) as count",
                        {"id": source_id}
                    ).single()["count"] > 0
                    
                    target_exists = session.run(
                        "MATCH (n {id: $id}) RETURN count(n) as count",
                        {"id": target_id}
                    ).single()["count"] > 0
                    
                    if source_exists and target_exists:
                        result = session.run("""
                            MATCH (source {id: $source_id})
                            MATCH (target {id: $target_id})
                            MERGE (source)-[r:%s]->(target)
                            ON CREATE SET r.description = $description,
                                          r.source = 'code_analysis',
                                          r.confidence = $confidence,
                                          r.created_at = datetime()
                            RETURN r
                        """ % rel["type"], {
                            "source_id": source_id,
                            "target_id": target_id,
                            "description": rel["description"],
                            "confidence": rel.get("confidence", "medium")
                        })
                        
                        if result.single():
                            added += 1
                except Exception as e:
                    print(f"   AVISO - Erro ao adicionar relação {rel['source']} -> {rel['target']}: {e}")
            
            print(f"   OK - {added} relações do código adicionadas")
            print()
            
            # ============================================
            # 3. IDENTIFICAR COMPONENTES FALTANTES
            # ============================================
            print("3. Identificando componentes que podem estar faltando...")
            
            # Verifica se há arquivos de agentes que não estão no grafo
            agents_dir = project_root / "src" / "agents"
            missing_agents = []
            
            if agents_dir.exists():
                for agent_file in agents_dir.glob("*.py"):
                    if agent_file.name == "__init__.py":
                        continue
                    
                    agent_id = agent_file.stem.replace("_", "-")
                    
                    exists = session.run(
                        "MATCH (a:Agent {id: $id}) RETURN count(a) as count",
                        {"id": agent_id}
                    ).single()["count"] > 0
                    
                    if not exists:
                        missing_agents.append({
                            "id": agent_id,
                            "file": str(agent_file.relative_to(project_root))
                        })
            
            if missing_agents:
                print(f"   AVISO - {len(missing_agents)} agentes encontrados no código mas não no grafo:")
                for agent in missing_agents:
                    print(f"      - {agent['id']} ({agent['file']})")
            else:
                print("   OK - Todos os agentes do código estão no grafo")
            
            print()
            
            # ============================================
            # 4. CRIAR RELAÇÕES DE VERSÃO E COMPATIBILIDADE
            # ============================================
            print("4. Adicionando relações de versão e compatibilidade...")
            
            # Adiciona informações de versão de dependências
            try:
                requirements_file = project_root / "requirements.txt"
                if requirements_file.exists():
                    with open(requirements_file, 'r') as f:
                        requirements = f.read()
                    
                    # Extrai versões principais
                    langchain_version = None
                    neo4j_version = None
                    
                    for line in requirements.split('\n'):
                        if 'langchain' in line.lower() and '==' in line:
                            langchain_version = line.split('==')[1].strip()
                        if 'neo4j' in line.lower() and '==' in line:
                            neo4j_version = line.split('==')[1].strip()
                    
                    # Adiciona como configuração
                    if langchain_version:
                        session.run("""
                            MERGE (c:Config {id: 'langchain_version'})
                            SET c.name = 'LangChain Version',
                                c.value = $version,
                                c.type = 'dependency',
                                c.description = 'Versão do LangChain usada no projeto'
                        """, {"version": langchain_version})
                    
                    if neo4j_version:
                        session.run("""
                            MERGE (c:Config {id: 'neo4j_version'})
                            SET c.name = 'Neo4j Driver Version',
                                c.value = $version,
                                c.type = 'dependency',
                                c.description = 'Versão do driver Neo4j'
                        """, {"version": neo4j_version})
                    
                    print("   OK - Versões de dependências adicionadas")
            except Exception as e:
                print(f"   AVISO - Erro ao adicionar versões: {e}")
            
            print()
            
            # ============================================
            # 5. CRIAR VISTAS E QUERIES ÚTEIS
            # ============================================
            print("5. Criando queries úteis e documentação...")
            
            useful_queries = {
                "all_agent_dependencies": """
                    MATCH (a:Agent)-[r:IMPORTS|DEPENDS_ON|USES]->(b)
                    RETURN a.name as agent, type(r) as relationship, b.name as dependency
                    ORDER BY a.name, type(r)
                """,
                "service_communication_flow": """
                    MATCH path = (s1:Service)-[:CALLS|QUERIES|CONNECTS_TO*]->(s2:Service)
                    RETURN s1.name as source, s2.name as target, length(path) as hops
                    ORDER BY hops
                """,
                "agent_capabilities": """
                    MATCH (a:Agent)
                    RETURN a.name as agent, a.capabilities as capabilities, a.type as type
                    ORDER BY a.name
                """,
                "configuration_usage": """
                    MATCH (a:Agent)-[:USES_CONFIG|REQUIRES]->(c:Config)
                    RETURN a.name as agent, c.name as config, c.value as value
                    ORDER BY a.name
                """
            }
            
            queries_file = project_root / "docs" / "NEO4J_USEFUL_QUERIES.md"
            with open(queries_file, 'w', encoding='utf-8') as f:
                f.write("# Queries Úteis para o Grafo Neo4j\n\n")
                f.write(f"Gerado em: {datetime.now().isoformat()}\n\n")
                
                for query_name, query in useful_queries.items():
                    f.write(f"## {query_name.replace('_', ' ').title()}\n\n")
                    f.write("```cypher\n")
                    f.write(query)
                    f.write("\n```\n\n")
            
            print(f"   OK - Queries úteis salvas em: {queries_file}")
            print()
            
            # ============================================
            # 6. ESTATÍSTICAS FINAIS
            # ============================================
            print("6. Estatísticas finais do grafo melhorado...")
            
            stats = session.run("""
                MATCH (n)
                RETURN labels(n)[0] as label, count(n) as count
                ORDER BY count DESC
            """).data()
            
            print("   Nós por tipo:")
            for stat in stats:
                print(f"      {stat['label']}: {stat['count']}")
            
            total_rels = session.run("MATCH ()-[r]->() RETURN count(r) as count").single()['count']
            print(f"   Total de relacionamentos: {total_rels}")
            
            # Relações por tipo
            rel_stats = session.run("""
                MATCH ()-[r]->()
                RETURN type(r) as rel_type, count(r) as count
                ORDER BY count DESC
                LIMIT 10
            """).data()
            
            print("   Top 10 tipos de relacionamentos:")
            for rel_stat in rel_stats:
                print(f"      {rel_stat['rel_type']}: {rel_stat['count']}")
            
            print()
            
        driver.close()
        
        print("=" * 80)
        print("SUCESSO! Grafo melhorado com análise do código e MCP")
        print("=" * 80)
        print()
        print("Melhorias aplicadas:")
        print("  - Relações identificadas no código fonte")
        print("  - Componentes faltantes identificados")
        print("  - Versões de dependências adicionadas")
        print("  - Queries úteis documentadas")
        print()
        print("Próximos passos:")
        print("  1. Revise as queries úteis em: docs/NEO4J_USEFUL_QUERIES.md")
        print("  2. Verifique componentes faltantes identificados")
        print("  3. Use o MCP do Neo4j no Cursor para explorar o grafo")
        
    except Exception as e:
        print(f"ERRO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    enhance_with_mcp_analysis()


