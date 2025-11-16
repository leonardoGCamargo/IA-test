# -*- coding: utf-8 -*-
"""
Script para limpar e otimizar containers Docker
Remove containers desnecessários e mantém apenas os do projeto
"""

import subprocess
import json
import sys

def executar_comando(cmd):
    """Executa comando Docker."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        return (True, result.stdout.strip())
    except subprocess.CalledProcessError as e:
        return (False, e.stderr.strip())

def listar_todos_containers():
    """Lista todos os containers (rodando e parados)."""
    cmd = ["docker", "ps", "-a", "--format", "json"]
    sucesso, output = executar_comando(cmd)
    
    if not sucesso:
        return []
    
    containers = []
    for line in output.split('\n'):
        if line.strip():
            try:
                container = json.loads(line)
                containers.append(container)
            except:
                pass
    
    return containers

def identificar_containers_manter():
    """Identifica containers que devem ser mantidos."""
    manter = [
        'ia-test',      # Containers do projeto IA-test
        'n8n',          # N8N (workflow automation)
        'dokploy',      # Dokploy (deployment)
        'postgres',     # PostgreSQL
        'redis',        # Redis
        'ollama',       # Ollama
        'kestra',       # Kestra
        'neo4j',        # Neo4j
        'traefik',      # Traefik
    ]
    return manter

def identificar_containers_remover(containers):
    """Identifica containers que devem ser removidos."""
    manter = identificar_containers_manter()
    remover = []
    
    for container in containers:
        name = container.get('Names', '').lower()
        
        # Mantém containers importantes
        if any(imp in name for imp in manter):
            continue
        
        # Remove containers órfãos (nomes aleatórios)
        if '_' in name and len(name.split('_')) == 2:
            palavras = name.split('_')
            if all(len(p) > 3 for p in palavras):
                remover.append(container)
    
    return remover

def remover_container(container_id, container_name):
    """Remove um container."""
    print(f"  [REMOVENDO] {container_name} ({container_id[:12]})")
    
    # Remove o container (funciona mesmo se estiver parado)
    cmd = ["docker", "rm", "-f", container_id]
    sucesso, output = executar_comando(cmd)
    
    if sucesso:
        print(f"    [OK] Removido")
        return True
    else:
        print(f"    [ERRO] {output}")
        return False

def listar_containers_projeto():
    """Lista containers do projeto IA-test."""
    cmd = ["docker", "ps", "-a", "--format", "{{.Names}}", "--filter", "name=ia-test"]
    sucesso, output = executar_comando(cmd)
    
    if sucesso:
        return [line.strip() for line in output.split('\n') if line.strip()]
    return []

def listar_containers_n8n():
    """Lista containers do N8N."""
    cmd = ["docker", "ps", "-a", "--format", "{{.Names}}", "--filter", "name=n8n"]
    sucesso, output = executar_comando(cmd)
    
    if sucesso:
        return [line.strip() for line in output.split('\n') if line.strip()]
    return []

def main():
    """Função principal."""
    print("=" * 70)
    print("LIMPEZA E OTIMIZACAO DE CONTAINERS")
    print("=" * 70)
    print()
    
    # Lista todos os containers
    print("Analisando containers...")
    containers = listar_todos_containers()
    print(f"Total de containers: {len(containers)}")
    print()
    
    # Containers do projeto
    containers_projeto = listar_containers_projeto()
    print(f"Containers do projeto IA-test: {len(containers_projeto)}")
    for c in containers_projeto:
        print(f"  - {c}")
    print()
    
    # Containers do N8N
    containers_n8n = listar_containers_n8n()
    print(f"Containers do N8N: {len(containers_n8n)}")
    for c in containers_n8n:
        print(f"  - {c}")
    print()
    
    # Containers para remover
    remover = identificar_containers_remover(containers)
    print(f"Containers para remover: {len(remover)}")
    print()
    
    if remover:
        print("Containers que serao removidos:")
        for c in remover[:30]:
            print(f"  - {c.get('Names', 'N/A')} ({c.get('Status', 'N/A')})")
        if len(remover) > 30:
            print(f"  ... e mais {len(remover) - 30} containers")
        print()
        
        if len(sys.argv) > 1 and sys.argv[1] == "--executar":
            print(f"[ATENCAO] {len(remover)} containers serao REMOVIDOS!")
            resposta = input("Confirma? Digite 'SIM': ")
            if resposta != 'SIM':
                print("Cancelado.")
                return
            
            print()
            removidos = 0
            for container in remover:
                container_id = container.get('ID', '')
                container_name = container.get('Names', '')
                
                if container_id and remover_container(container_id, container_name):
                    removidos += 1
            
            print()
            print("=" * 70)
            print(f"[OK] Removidos: {removidos}/{len(remover)}")
            print("=" * 70)
        else:
            print("=" * 70)
            print("SIMULACAO")
            print(f"Total que seria removido: {len(remover)}")
            print()
            print("Para executar:")
            print("  python scripts/limpar_e_otimizar_containers.py --executar")
            print("=" * 70)
    else:
        print("Nenhum container para remover.")
        print("=" * 70)

if __name__ == "__main__":
    main()

