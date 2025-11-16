# -*- coding: utf-8 -*-
"""
Script para analisar e limpar containers Docker desnecessários
"""

import subprocess
import json
from pathlib import Path
from typing import List, Dict, Any

def executar_comando(cmd: List[str]) -> str:
    """Executa comando Docker e retorna output."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Erro: {e}"

def listar_containers() -> List[Dict[str, Any]]:
    """Lista todos os containers."""
    output = executar_comando([
        "docker", "ps", "-a", "--format",
        "{{json .}}"
    ])
    
    containers = []
    for line in output.split('\n'):
        if line.strip():
            try:
                container = json.loads(line)
                containers.append(container)
            except:
                pass
    
    return containers

def analisar_containers():
    """Analisa containers e identifica quais são do projeto."""
    print("=" * 70)
    print("ANALISE DE CONTAINERS DOCKER")
    print("=" * 70)
    print()
    
    containers = listar_containers()
    
    print(f"Total de containers: {len(containers)}")
    print()
    
    # Categoriza containers
    projeto_containers = []
    outros_containers = []
    parados = []
    
    for container in containers:
        name = container.get('Names', '')
        status = container.get('Status', '')
        
        # Containers do projeto IA-test
        if 'ia-test' in name.lower() or 'kestra' in name.lower():
            projeto_containers.append(container)
        elif 'Exited' in status or 'Created' in status:
            parados.append(container)
        else:
            outros_containers.append(container)
    
    print("CATEGORIZACAO:")
    print(f"  - Containers do projeto IA-test: {len(projeto_containers)}")
    print(f"  - Containers parados: {len(parados)}")
    print(f"  - Outros containers: {len(outros_containers)}")
    print()
    
    # Lista containers do projeto
    if projeto_containers:
        print("CONTAINERS DO PROJETO IA-TEST:")
        for c in projeto_containers:
            print(f"  - {c.get('Names', 'N/A')}: {c.get('Status', 'N/A')}")
        print()
    
    # Lista containers parados
    if parados:
        print("CONTAINERS PARADOS (podem ser removidos):")
        for c in parados[:10]:  # Mostra primeiros 10
            print(f"  - {c.get('Names', 'N/A')}: {c.get('Status', 'N/A')}")
        if len(parados) > 10:
            print(f"  ... e mais {len(parados) - 10} containers parados")
        print()
    
    # Lista outros containers
    if outros_containers:
        print("OUTROS CONTAINERS RODANDO:")
        for c in outros_containers[:10]:  # Mostra primeiros 10
            print(f"  - {c.get('Names', 'N/A')}: {c.get('Status', 'N/A')}")
        if len(outros_containers) > 10:
            print(f"  ... e mais {len(outros_containers) - 10} containers")
        print()
    
    return {
        'total': len(containers),
        'projeto': len(projeto_containers),
        'parados': len(parados),
        'outros': len(outros_containers),
        'containers_parados': parados,
        'outros_containers': outros_containers
    }

def limpar_containers_parados():
    """Remove containers parados."""
    print("=" * 70)
    print("LIMPANDO CONTAINERS PARADOS")
    print("=" * 70)
    print()
    
    # Remove containers parados
    output = executar_comando([
        "docker", "container", "prune", "-f"
    ])
    
    print("Containers parados removidos!")
    print()

def limpar_imagens_nao_usadas():
    """Remove imagens não utilizadas."""
    print("=" * 70)
    print("LIMPANDO IMAGENS NAO USADAS")
    print("=" * 70)
    print()
    
    output = executar_comando([
        "docker", "image", "prune", "-a", "-f"
    ])
    
    print("Imagens não utilizadas removidas!")
    print()

def limpar_volumes_nao_usados():
    """Remove volumes não utilizados."""
    print("=" * 70)
    print("LIMPANDO VOLUMES NAO USADOS")
    print("=" * 70)
    print()
    
    output = executar_comando([
        "docker", "volume", "prune", "-f"
    ])
    
    print("Volumes não utilizados removidos!")
    print()

def limpar_networks_nao_usadas():
    """Remove networks não utilizadas."""
    print("=" * 70)
    print("LIMPANDO NETWORKS NAO USADAS")
    print("=" * 70)
    print()
    
    output = executar_comando([
        "docker", "network", "prune", "-f"
    ])
    
    print("Networks não utilizadas removidas!")
    print()

def parar_containers_projeto():
    """Para containers do projeto usando docker-compose."""
    print("=" * 70)
    print("PARANDO CONTAINERS DO PROJETO")
    print("=" * 70)
    print()
    
    project_root = Path(__file__).parent.parent
    docker_compose = project_root / "config" / "docker-compose.yml"
    
    if docker_compose.exists():
        print(f"Parando containers do docker-compose...")
        output = executar_comando([
            "docker", "compose", "-f", str(docker_compose), "down"
        ])
        print("Containers do projeto parados!")
    else:
        print("docker-compose.yml não encontrado")
    print()

def main():
    """Função principal."""
    # Analisa
    resultado = analisar_containers()
    
    print("=" * 70)
    print("RECOMENDACOES")
    print("=" * 70)
    print()
    
    if resultado['parados'] > 0:
        print(f"  - {resultado['parados']} containers parados podem ser removidos")
    
    if resultado['total'] > 20:
        print(f"  - Total de {resultado['total']} containers é muito alto")
        print("  - Considere limpar containers, imagens e volumes não utilizados")
    
    print()
    print("Para limpar automaticamente, execute:")
    print("  python scripts/limpar_containers.py --auto")
    print()

if __name__ == "__main__":
    main()
