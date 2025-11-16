"""
Exemplo de uso do Docker Integration Agent.

Este script demonstra como usar o agente para:
1. Detectar servidores MCP em containers Docker
2. Sincronizar com Neo4j
3. Criar notas no Obsidian
4. Atualizar docker-compose.yml
"""

import os
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from src.agents.mcp_docker_integration import (
    DockerMCPDetector
)


def exemplo_basico():
    """Exemplo básico de uso do agente."""
    print("=== Exemplo Básico: Docker Integration Agent ===\n")
    
    # Inicializa o agente
    agent = DockerIntegrationAgent()
    
    # Verifica status
    status = agent.get_status()
    print("Status do Agente:")
    print(f"  Docker disponível: {status['docker_available']}")
    print(f"  Containers em execução: {status['containers_running']}")
    print(f"  Neo4j conectado: {status['neo4j_connected']}")
    print(f"  Obsidian configurado: {status['obsidian_configured']}")
    print()
    
    # Executa scan e sincronização
    print("Executando scan e sincronização...")
    results = agent.scan_and_sync(update_compose=True)
    
    print("\nResultados:")
    print(f"  Containers escaneados: {results['containers_scanned']}")
    print(f"  MCPs detectados: {results['mcps_detected']}")
    print(f"  Sincronizados com Neo4j: {results['neo4j_synced']}")
    print(f"  Notas criadas no Obsidian: {results['obsidian_synced']}")
    print(f"  Serviços atualizados no compose: {results['compose_updated']}")
    
    if results['errors']:
        print("\nErros encontrados:")
        for error in results['errors']:
            print(f"  - {error}")


def exemplo_deteccao_manual():
    """Exemplo de detecção manual de MCPs."""
    print("\n=== Exemplo: Detecção Manual de MCPs ===\n")
    
    detector = DockerMCPDetector()
    
    # Lista todos os containers
    print("Listando containers em execução...")
    containers = detector.list_running_containers()
    print(f"Total de containers: {len(containers)}")
    
    for container in containers[:5]:  # Mostra apenas os 5 primeiros
        print(f"  - {container.name} ({container.image})")
    
    # Detecta servidores MCP
    print("\nDetectando servidores MCP...")
    mcps = detector.detect_mcp_services()
    
    if mcps:
        print(f"\nEncontrados {len(mcps)} servidores MCP:")
        for mcp in mcps:
            print(f"\n  MCP: {mcp.name}")
            print(f"    Container: {mcp.container_name}")
            print(f"    Imagem: {mcp.image}")
            print(f"    Portas: {', '.join(mcp.ports) if mcp.ports else 'Nenhuma'}")
            print(f"    Comando: {mcp.command or 'N/A'}")
            print(f"    Detectado em: {mcp.detected_at}")
    else:
        print("Nenhum servidor MCP detectado.")


def exemplo_info_detalhada():
    """Exemplo de obtenção de informações detalhadas de um container."""
    print("\n=== Exemplo: Informações Detalhadas ===\n")
    
    detector = DockerMCPDetector()
    
    # Lista containers
    containers = detector.list_running_containers()
    
    if not containers:
        print("Nenhum container em execução.")
        return
    
    # Pega o primeiro container
    first_container = containers[0]
    print(f"Obtendo informações detalhadas de: {first_container.name}")
    
    info = detector.get_service_info(first_container.name)
    
    if info:
        print(f"\nInformações do Container:")
        print(f"  ID: {info.get('id', 'N/A')[:12]}...")
        print(f"  Nome: {info.get('name', 'N/A')}")
        print(f"  Status: {info.get('status', 'N/A')}")
        print(f"  Imagem: {info.get('image', 'N/A')}")
        print(f"  Redes: {', '.join(info.get('networks', []))}")
        
        ports = info.get('ports', [])
        if ports:
            print(f"  Portas:")
            for port in ports:
                host_port = port.get('host_port', 'N/A')
                container_port = port.get('container_port', 'N/A')
                print(f"    {host_port} -> {container_port}/{port.get('protocol', 'tcp')}")
        
        env_vars = info.get('env', [])
        if env_vars:
            print(f"  Variáveis de Ambiente ({len(env_vars)}):")
            for env in env_vars[:5]:  # Mostra apenas as 5 primeiras
                print(f"    {env}")
            if len(env_vars) > 5:
                print(f"    ... e mais {len(env_vars) - 5}")


def exemplo_compose_services():
    """Exemplo de listagem de serviços do docker-compose."""
    print("\n=== Exemplo: Serviços do Docker Compose ===\n")
    
    detector = DockerMCPDetector()
    
    services = detector.list_compose_services()
    
    if services:
        print(f"Serviços definidos no docker-compose.yml ({len(services)}):")
        for service in services:
            print(f"  - {service}")
    else:
        print("Nenhum serviço encontrado ou arquivo não existe.")


def exemplo_consulta_neo4j():
    """Exemplo de consulta ao Neo4j após sincronização."""
    print("\n=== Exemplo: Consulta ao Neo4j ===\n")
    
    agent = DockerIntegrationAgent()
    
    if not agent.neo4j_manager:
        print("Neo4j manager não disponível.")
        return
    
    try:
        # Obtém estatísticas do grafo
        stats = agent.neo4j_manager.get_graph_statistics()
        print("Estatísticas do Grafo Neo4j:")
        print(f"  MCPs: {stats.get('MCP_count', 0)}")
        print(f"  RAGs: {stats.get('RAG_count', 0)}")
        print(f"  Notas Obsidian: {stats.get('ObsidianNote_count', 0)}")
        print(f"  Tags: {stats.get('Tag_count', 0)}")
        print(f"  Relações: {stats.get('relation_count', 0)}")
        
        # Busca MCPs no grafo
        print("\nBuscando MCPs no grafo...")
        mcps = agent.neo4j_manager.query_graph(
            "MATCH (m:MCP) RETURN m.name as name, m.image as image, m.enabled as enabled LIMIT 10"
        )
        
        if mcps:
            print(f"Encontrados {len(mcps)} MCPs:")
            for mcp in mcps:
                mcp_data = mcp.get('m', {}) if isinstance(mcp.get('m'), dict) else {}
                name = mcp.get('name') or mcp_data.get('name', 'N/A')
                image = mcp.get('image') or mcp_data.get('image', 'N/A')
                enabled = mcp.get('enabled') or mcp_data.get('enabled', True)
                status = "✅" if enabled else "❌"
                print(f"  {status} {name} ({image})")
        else:
            print("Nenhum MCP encontrado no grafo.")
            
    except Exception as e:
        print(f"Erro ao consultar Neo4j: {e}")


def main():
    """Executa todos os exemplos."""
    print("=" * 60)
    print("EXEMPLOS DE USO: Docker Integration Agent")
    print("=" * 60)
    
    try:
        exemplo_basico()
        exemplo_deteccao_manual()
        exemplo_info_detalhada()
        exemplo_compose_services()
        exemplo_consulta_neo4j()
        
        print("\n" + "=" * 60)
        print("Exemplos concluídos!")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n\nInterrompido pelo usuário.")
    except Exception as e:
        print(f"\n\nErro durante execução: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

