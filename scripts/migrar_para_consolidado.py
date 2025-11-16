# -*- coding: utf-8 -*-
"""
Script para migrar containers do N8N e Dokploy para configuração consolidada
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

def listar_containers_antigos():
    """Lista containers antigos do N8N e Dokploy."""
    cmd = ["docker", "ps", "-a", "--format", "json"]
    sucesso, output = executar_comando(cmd)
    
    if not sucesso:
        return []
    
    containers = []
    for line in output.split('\n'):
        if line.strip():
            try:
                container = json.loads(line)
                name = container.get('Names', '')
                
                # Containers do N8N antigo
                if 'iaimplementation-n8n' in name.lower():
                    containers.append(container)
                # Containers do Dokploy antigo (Swarm)
                elif 'dokploy' in name.lower() and 'consolidado' not in name.lower():
                    containers.append(container)
            except:
                pass
    
    return containers

def parar_containers(containers):
    """Para containers."""
    for container in containers:
        container_id = container.get('ID', '')
        container_name = container.get('Names', '')
        
        if container_id:
            print(f"[PARANDO] {container_name}")
            cmd = ["docker", "stop", container_id]
            executar_comando(cmd)

def remover_containers(containers):
    """Remove containers."""
    for container in containers:
        container_id = container.get('ID', '')
        container_name = container.get('Names', '')
        
        if container_id:
            print(f"[REMOVENDO] {container_name}")
            cmd = ["docker", "rm", container_id]
            executar_comando(cmd)

def main():
    """Função principal."""
    print("=" * 70)
    print("MIGRACAO PARA CONFIGURACAO CONSOLIDADA")
    print("=" * 70)
    print()
    print("Este script vai:")
    print("  1. Parar containers antigos do N8N e Dokploy")
    print("  2. Remover containers antigos")
    print("  3. Você pode então iniciar a nova configuração consolidada")
    print()
    
    containers = listar_containers_antigos()
    
    if not containers:
        print("Nenhum container antigo encontrado.")
        return
    
    print(f"Containers antigos encontrados: {len(containers)}")
    for c in containers:
        print(f"  - {c.get('Names', 'N/A')} ({c.get('Status', 'N/A')})")
    print()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--executar":
        print("[ATENCAO] Containers serao PARADOS e REMOVIDOS!")
        resposta = input("Confirma? Digite 'SIM': ")
        if resposta != 'SIM':
            print("Cancelado.")
            return
        
        print()
        print("Parando containers...")
        parar_containers(containers)
        
        print()
        print("Removendo containers...")
        remover_containers(containers)
        
        print()
        print("=" * 70)
        print("[OK] Migracao concluida!")
        print()
        print("Agora inicie a nova configuracao consolidada:")
        print("  docker compose -f config/docker-compose-consolidado.yml up -d")
        print("=" * 70)
    else:
        print("=" * 70)
        print("SIMULACAO")
        print()
        print("Para executar:")
        print("  python scripts/migrar_para_consolidado.py --executar")
        print("=" * 70)

if __name__ == "__main__":
    main()

