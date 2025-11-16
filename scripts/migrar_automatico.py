# -*- coding: utf-8 -*-
"""
Script para migrar containers automaticamente (sem confirmação)
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
                if 'iaimplementation-n8n' in name.lower() and 'consolidado' not in name.lower():
                    containers.append(container)
                # Containers do Dokploy antigo (Swarm ou não consolidado)
                elif ('dokploy' in name.lower() and 'consolidado' not in name.lower() and 
                      not name.startswith('dokploy.1.')):
                    # Pula containers do Swarm que estão rodando
                    if container.get('State') != 'running':
                        containers.append(container)
            except:
                pass
    
    return containers

def parar_e_remover_containers(containers):
    """Para e remove containers."""
    removidos = 0
    for container in containers:
        container_id = container.get('ID', '')
        container_name = container.get('Names', '')
        state = container.get('State', '')
        
        if not container_id:
            continue
        
        print(f"[PROCESSANDO] {container_name} ({state})")
        
        # Para se estiver rodando
        if state == 'running':
            cmd_stop = ["docker", "stop", container_id]
            sucesso, _ = executar_comando(cmd_stop)
            if sucesso:
                print(f"  [OK] Parado")
            else:
                print(f"  [AVISO] Nao foi possivel parar (pode estar em Swarm)")
                continue
        
        # Remove
        cmd_rm = ["docker", "rm", "-f", container_id]
        sucesso, output = executar_comando(cmd_rm)
        if sucesso:
            removidos += 1
            print(f"  [OK] Removido")
        else:
            print(f"  [AVISO] {output}")
    
    return removidos

def main():
    """Função principal."""
    print("=" * 70)
    print("MIGRACAO AUTOMATICA - N8N + DOKPLOY")
    print("=" * 70)
    print()
    
    containers = listar_containers_antigos()
    
    if not containers:
        print("Nenhum container antigo encontrado para migrar.")
        print()
        print("Containers do Swarm (dokploy.1.*) serao mantidos")
        print("e substituidos quando iniciar a configuracao consolidada.")
        return
    
    print(f"Containers antigos encontrados: {len(containers)}")
    for c in containers:
        print(f"  - {c.get('Names', 'N/A')} ({c.get('Status', 'N/A')})")
    print()
    
    print("Parando e removendo containers antigos...")
    print()
    removidos = parar_e_remover_containers(containers)
    
    print()
    print("=" * 70)
    print(f"[OK] Processados: {removidos}/{len(containers)}")
    print()
    print("PROXIMOS PASSOS:")
    print("  1. Parar containers do Swarm (se necessario):")
    print("     docker service rm dokploy dokploy-postgres dokploy-redis")
    print()
    print("  2. Iniciar configuracao consolidada:")
    print("     docker compose -f config/docker-compose-consolidado.yml up -d")
    print("=" * 70)

if __name__ == "__main__":
    main()


