"""
Script para melhorar e enriquecer as relações no Neo4j usando o MCP.

Este script:
- Adiciona relações mais detalhadas entre componentes
- Cria índices para melhor performance
- Adiciona propriedades e metadados
- Identifica padrões e melhora a estrutura do grafo
- Gera relatório de melhorias

Uso:
    python scripts/enhance_neo4j_relationships.py
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

# Relatório de melhorias
improvements_report = {
    "timestamp": datetime.now().isoformat(),
    "indexes_created": [],
    "relationships_added": [],
    "properties_added": [],
    "patterns_identified": [],
    "suggestions": []
}

def enhance_graph():
    """Melhora o grafo Neo4j com relações mais detalhadas e índices."""
    print("=" * 80)
    print("MELHORANDO RELACOES E ESTRUTURA DO GRAFO NEO4J")
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
            # 1. CRIAR ÍNDICES PARA PERFORMANCE
            # ============================================
            print("1. Criando índices para melhor performance...")
            indexes = [
                # Índices em propriedades frequentemente usadas
                ("CREATE INDEX agent_type_idx IF NOT EXISTS FOR (a:Agent) ON (a.type)", "Agent.type"),
                ("CREATE INDEX agent_uses_llm_idx IF NOT EXISTS FOR (a:Agent) ON (a.uses_llm)", "Agent.uses_llm"),
                ("CREATE INDEX service_type_idx IF NOT EXISTS FOR (s:Service) ON (s.type)", "Service.type"),
                ("CREATE INDEX service_port_idx IF NOT EXISTS FOR (s:Service) ON (s.port)", "Service.port"),
                ("CREATE INDEX mcp_enabled_idx IF NOT EXISTS FOR (m:MCP) ON (m.enabled)", "MCP.enabled"),
                ("CREATE INDEX config_type_idx IF NOT EXISTS FOR (c:Config) ON (c.type)", "Config.type"),
            ]
            
            for index_query, index_name in indexes:
                try:
                    session.run(index_query)
                    improvements_report["indexes_created"].append(index_name)
                    print(f"   OK - Índice criado: {index_name}")
                except Exception as e:
                    print(f"   AVISO - {index_name}: {e}")
            
            print()
            
            # ============================================
            # 2. ADICIONAR RELAÇÕES MAIS DETALHADAS
            # ============================================
            print("2. Adicionando relações mais detalhadas...")
            
            # Relações de dependência entre agentes
            agent_dependencies = [
                ("orchestrator", "neo4j-graphrag", "DEPENDS_ON", "Orchestrator depende do GraphRAG para consultas"),
                ("orchestrator", "mcp-manager", "DEPENDS_ON", "Orchestrator depende do MCP Manager"),
                ("neo4j-graphrag", "db-manager", "USES", "GraphRAG usa DB Manager para conexões"),
                ("system-health", "docker-integration", "MONITORS", "System Health monitora Docker"),
                ("system-health", "kestra-agent", "MONITORS", "System Health monitora Kestra"),
            ]
            
            # Relações de comunicação entre serviços
            service_communication = [
                ("api-service", "neo4j-service", "QUERIES", "API faz queries no Neo4j"),
                ("dashboard-service", "api-service", "CALLS", "Dashboard chama API"),
                ("mcp-manager-service", "neo4j-service", "QUERIES", "MCP Manager consulta Neo4j"),
                ("kestra-service", "kestra-postgres", "STORES", "Kestra armazena dados no PostgreSQL"),
            ]
            
            # Relações de configuração
            config_usage = [
                ("orchestrator", "llm", "REQUIRES", "Orchestrator requer configuração LLM"),
                ("neo4j-graphrag", "embedding_model", "REQUIRES", "GraphRAG requer modelo de embedding"),
                ("api-service", "neo4j_uri", "REQUIRES", "API requer URI do Neo4j"),
            ]
            
            # Relações de fluxo de dados
            data_flow = [
                ("obsidian-integration", "neo4j-graphrag", "FEEDS", "Obsidian alimenta dados no GraphRAG"),
                ("mcp-manager", "neo4j-graphrag", "FEEDS", "MCP Manager alimenta dados no GraphRAG"),
                ("git-integration", "neo4j-graphrag", "FEEDS", "Git alimenta dados no GraphRAG"),
            ]
            
            all_relationships = agent_dependencies + service_communication + config_usage + data_flow
            
            created = 0
            for source_id, target_id, rel_type, description in all_relationships:
                try:
                    result = session.run("""
                        MATCH (source {id: $source_id})
                        MATCH (target {id: $target_id})
                        MERGE (source)-[r:%s]->(target)
                        ON CREATE SET r.description = $description,
                                      r.created_at = datetime(),
                                      r.weight = 1
                        ON MATCH SET r.updated_at = datetime(),
                                     r.weight = COALESCE(r.weight, 0) + 1
                        RETURN r
                    """ % rel_type, {
                        "source_id": source_id,
                        "target_id": target_id,
                        "description": description
                    })
                    
                    if result.single():
                        created += 1
                        improvements_report["relationships_added"].append({
                            "source": source_id,
                            "target": target_id,
                            "type": rel_type,
                            "description": description
                        })
                except Exception as e:
                    print(f"   IGNORADO - {source_id} -> {target_id} ({rel_type}): {e}")
            
            print(f"   OK - {created} relações detalhadas criadas")
            print()
            
            # ============================================
            # 3. ADICIONAR PROPRIEDADES E METADADOS
            # ============================================
            print("3. Adicionando propriedades e metadados...")
            
            # Adicionar propriedades de status aos serviços
            try:
                session.run("""
                    MATCH (s:Service)
                    WHERE s.status IS NULL
                    SET s.status = 'active',
                        s.last_health_check = datetime(),
                        s.health_status = 'unknown'
                """)
                improvements_report["properties_added"].append("Service.status, last_health_check, health_status")
                print("   OK - Propriedades de status adicionadas aos serviços")
            except Exception as e:
                print(f"   AVISO - Propriedades de status: {e}")
            
            # Adicionar propriedades de versão aos agentes
            try:
                session.run("""
                    MATCH (a:Agent)
                    WHERE a.version IS NULL
                    SET a.version = '1.0.0',
                        a.last_update = datetime(),
                        a.maintainer = 'IA-Test Team'
                """)
                improvements_report["properties_added"].append("Agent.version, last_update, maintainer")
                print("   OK - Propriedades de versão adicionadas aos agentes")
            except Exception as e:
                print(f"   AVISO - Propriedades de versão: {e}")
            
            # Adicionar propriedades de performance
            try:
                session.run("""
                    MATCH (a:Agent)
                    WHERE a.performance_metrics IS NULL
                    SET a.performance_metrics = {
                        avg_response_time: 0,
                        total_requests: 0,
                        success_rate: 100.0
                    }
                """)
                improvements_report["properties_added"].append("Agent.performance_metrics")
                print("   OK - Métricas de performance adicionadas")
            except Exception as e:
                print(f"   AVISO - Métricas de performance: {e}")
            
            print()
            
            # ============================================
            # 4. IDENTIFICAR PADRÕES E ESTRUTURAS
            # ============================================
            print("4. Identificando padrões e estruturas...")
            
            # Padrão: Agentes que usam LLM
            try:
                llm_agents = session.run("""
                    MATCH (a:Agent {uses_llm: true})
                    RETURN count(a) as count, collect(a.name) as agents
                """).single()
                
                if llm_agents:
                    improvements_report["patterns_identified"].append({
                        "pattern": "Agentes que usam LLM",
                        "count": llm_agents["count"],
                        "agents": llm_agents["agents"]
                    })
                    print(f"   OK - Padrão identificado: {llm_agents['count']} agentes usam LLM")
            except Exception as e:
                print(f"   AVISO - Padrão LLM: {e}")
            
            # Padrão: Serviços por profile
            try:
                profile_services = session.run("""
                    MATCH (s:Service)
                    RETURN s.profile as profile, count(s) as count
                    ORDER BY count DESC
                """).data()
                
                if profile_services:
                    improvements_report["patterns_identified"].append({
                        "pattern": "Serviços por profile Docker",
                        "distribution": profile_services
                    })
                    print(f"   OK - Padrão identificado: Distribuição de serviços por profile")
            except Exception as e:
                print(f"   AVISO - Padrão profile: {e}")
            
            # Padrão: Cadeias de dependência
            try:
                dependency_chains = session.run("""
                    MATCH path = (a:Agent)-[:DEPENDS_ON*]->(b:Agent)
                    WHERE length(path) > 0
                    RETURN count(path) as chains
                """).single()
                
                if dependency_chains and dependency_chains["chains"] > 0:
                    improvements_report["patterns_identified"].append({
                        "pattern": "Cadeias de dependência entre agentes",
                        "count": dependency_chains["chains"]
                    })
                    print(f"   OK - Padrão identificado: {dependency_chains['chains']} cadeias de dependência")
            except Exception as e:
                print(f"   AVISO - Padrão dependência: {e}")
            
            print()
            
            # ============================================
            # 5. CRIAR RELAÇÕES DE HIERARQUIA E GRUPOS
            # ============================================
            print("5. Criando relações de hierarquia e grupos...")
            
            # Criar grupos de agentes
            agent_groups = [
                ("core-agents", ["orchestrator", "system-health", "db-manager"], "Agentes core do sistema"),
                ("integration-agents", ["git-integration", "obsidian-integration", "docker-integration"], "Agentes de integração"),
                ("ai-agents", ["orchestrator", "neo4j-graphrag"], "Agentes que usam IA/LLM"),
            ]
            
            for group_id, agent_ids, description in agent_groups:
                try:
                    session.run("""
                        MERGE (g:AgentGroup {id: $group_id})
                        SET g.name = $group_id,
                            g.description = $description,
                            g.created_at = datetime()
                        WITH g
                        UNWIND $agent_ids AS agent_id
                        MATCH (a:Agent {id: agent_id})
                        MERGE (g)-[:CONTAINS]->(a)
                    """, {
                        "group_id": group_id,
                        "description": description,
                        "agent_ids": agent_ids
                    })
                    print(f"   OK - Grupo criado: {group_id} ({len(agent_ids)} agentes)")
                except Exception as e:
                    print(f"   IGNORADO - Grupo {group_id}: {e}")
            
            # Criar grupos de serviços
            service_groups = [
                ("core-services", ["neo4j-service", "api-service", "frontend-service", "dashboard-service"], "Serviços core"),
                ("streamlit-services", ["bot-service", "loader-service", "pdf-bot-service"], "Serviços Streamlit"),
                ("tool-services", ["kestra-service", "mcp-manager-service"], "Serviços de ferramentas"),
            ]
            
            for group_id, service_ids, description in service_groups:
                try:
                    session.run("""
                        MERGE (g:ServiceGroup {id: $group_id})
                        SET g.name = $group_id,
                            g.description = $description,
                            g.created_at = datetime()
                        WITH g
                        UNWIND $service_ids AS service_id
                        MATCH (s:Service {id: service_id})
                        MERGE (g)-[:CONTAINS]->(s)
                    """, {
                        "group_id": group_id,
                        "description": description,
                        "service_ids": service_ids
                    })
                    print(f"   OK - Grupo criado: {group_id} ({len(service_ids)} serviços)")
                except Exception as e:
                    print(f"   IGNORADO - Grupo {group_id}: {e}")
            
            print()
            
            # ============================================
            # 6. ADICIONAR RELAÇÕES DE FLUXO DE TRABALHO
            # ============================================
            print("6. Adicionando relações de fluxo de trabalho...")
            
            workflow_flows = [
                ("orchestrator", "neo4j-graphrag", "TRIGGERS", "Orchestrator dispara consultas GraphRAG"),
                ("user", "dashboard-service", "INTERACTS_WITH", "Usuário interage com dashboard"),
                ("dashboard-service", "orchestrator", "REQUESTS", "Dashboard solicita ações do Orchestrator"),
                ("kestra-service", "orchestrator", "NOTIFIES", "Kestra notifica Orchestrator de eventos"),
                ("system-health", "orchestrator", "ALERTS", "System Health alerta Orchestrator"),
            ]
            
            # Criar nó de usuário se não existir
            try:
                session.run("""
                    MERGE (u:User {id: 'user'})
                    SET u.name = 'System User',
                        u.type = 'human',
                        u.created_at = datetime()
                """)
            except:
                pass
            
            created_flows = 0
            for source_id, target_id, rel_type, description in workflow_flows:
                try:
                    result = session.run("""
                        MATCH (source {id: $source_id})
                        MATCH (target {id: $target_id})
                        MERGE (source)-[r:%s]->(target)
                        ON CREATE SET r.description = $description,
                                      r.created_at = datetime()
                        RETURN r
                    """ % rel_type, {
                        "source_id": source_id,
                        "target_id": target_id,
                        "description": description
                    })
                    
                    if result.single():
                        created_flows += 1
                except Exception as e:
                    print(f"   IGNORADO - {source_id} -> {target_id} ({rel_type}): {e}")
            
            print(f"   OK - {created_flows} fluxos de trabalho criados")
            print()
            
            # ============================================
            # 7. ESTATÍSTICAS FINAIS E ANÁLISE
            # ============================================
            print("7. Análise final do grafo...")
            
            # Estatísticas gerais
            stats = session.run("""
                MATCH (n)
                RETURN labels(n)[0] as label, count(n) as count
                ORDER BY count DESC
            """).data()
            
            print("   Estatísticas por tipo de nó:")
            for stat in stats:
                print(f"      {stat['label']}: {stat['count']} nós")
            
            # Contar relacionamentos por tipo
            rel_stats = session.run("""
                MATCH ()-[r]->()
                RETURN type(r) as rel_type, count(r) as count
                ORDER BY count DESC
            """).data()
            
            print("   Relacionamentos por tipo:")
            for rel_stat in rel_stats:
                print(f"      {rel_stat['rel_type']}: {rel_stat['count']}")
            
            total_rels = session.run("MATCH ()-[r]->() RETURN count(r) as count").single()['count']
            print(f"   Total de relacionamentos: {total_rels}")
            print()
            
            # Identificar componentes isolados
            isolated = session.run("""
                MATCH (n)
                WHERE NOT (n)--()
                RETURN labels(n)[0] as label, n.id as id, n.name as name
                LIMIT 10
            """).data()
            
            if isolated:
                improvements_report["suggestions"].append({
                    "type": "componentes_isolados",
                    "count": len(isolated),
                    "items": isolated,
                    "recommendation": "Adicionar relações para componentes isolados"
                })
                print(f"   AVISO - {len(isolated)} componentes isolados encontrados")
            
            # Identificar componentes com muitas relações (hubs)
            hubs = session.run("""
                MATCH (n)-[r]-()
                WITH n, count(r) as degree
                WHERE degree > 5
                RETURN labels(n)[0] as label, n.id as id, n.name as name, degree
                ORDER BY degree DESC
                LIMIT 5
            """).data()
            
            if hubs:
                improvements_report["patterns_identified"].append({
                    "pattern": "Componentes hub (muitas conexões)",
                    "hubs": hubs
                })
                print(f"   OK - {len(hubs)} componentes hub identificados")
            
        driver.close()
        
        # ============================================
        # 8. SALVAR RELATÓRIO DE MELHORIAS
        # ============================================
        report_file = project_root / "NEO4J_IMPROVEMENTS_REPORT.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(improvements_report, f, indent=2, ensure_ascii=False, default=str)
        
        print("=" * 80)
        print("SUCESSO! Grafo melhorado e enriquecido")
        print("=" * 80)
        print()
        print(f"Resumo de melhorias:")
        print(f"  - Índices criados: {len(improvements_report['indexes_created'])}")
        print(f"  - Relações adicionadas: {len(improvements_report['relationships_added'])}")
        print(f"  - Propriedades adicionadas: {len(improvements_report['properties_added'])}")
        print(f"  - Padrões identificados: {len(improvements_report['patterns_identified'])}")
        print(f"  - Sugestões: {len(improvements_report['suggestions'])}")
        print()
        print(f"Relatório completo salvo em: {report_file}")
        print()
        print("Acesse o Neo4j Browser em: http://localhost:7474")
        print("Queries úteis:")
        print("  - Ver grupos: MATCH (g:AgentGroup)-[:CONTAINS]->(a:Agent) RETURN g, a")
        print("  - Ver fluxos: MATCH (a)-[r:TRIGGERS|REQUESTS|ALERTS]->(b) RETURN a, r, b")
        print("  - Ver hubs: MATCH (n)-[r]-() WITH n, count(r) as degree WHERE degree > 5 RETURN n, degree")
        
    except Exception as e:
        print(f"ERRO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    enhance_graph()


