# -*- coding: utf-8 -*-
"""
Script para limpar containers Docker desnecessários
"""

import subprocess
import json
from datetime import datetime, timedelta
from typing import List, Dict

def executar_comando(cmd: List[str]) -> str:
    """Executa comando Docker e retorna output."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar: {' '.join(cmd)}")
        print(f"Erro: {e.stderr}")
        return ""

def listar_containers() -> List[Dict]:
    """Lista todos os containers."""
    cmd = ["docker", "ps", "-a", "--format", "json"]
    output = executar_comando(cmd)
    
    containers = []
    for line in output.split('\n'):
        if line.strip():
            try:
                container = json.loads(line)
                containers.append(container)
            except:
                pass
    
    return containers

def listar_containers_parados() -> List[Dict]:
    """Lista containers parados."""
    containers = listar_containers()
    return [c for c in containers if c.get('State') == 'exited']

def listar_containers_antigos(dias: int = 7) -> List[Dict]:
    """Lista containers criados há mais de X dias."""
    containers = listar_containers()
    antigos = []
    
    for container in containers:
        created = container.get('CreatedAt', '')
        if created:
            try:
                # Formato: 2025-01-27 10:30:45 +0000 UTC
                created_date = datetime.strptime(created.split(' +')[0], '%Y-%m-%d %H:%M:%S')
                if (datetime.now() - created_date).days > dias:
                    antigos.append(container)
            except:
                pass
    
    return antigos

def remover_containers(containers: List[Dict], dry_run: bool = True) -> int:
    """Remove containers."""
    removidos = 0
    
    for container in containers:
        container_id = container.get('ID', '')
        container_name = container.get('Names', '')
        
        if not container_id:
            continue
        
        # Pula containers do sistema importantes
        if any(skip in container_name.lower() for skip in ['kestra', 'neo4j', 'database']):
            print(f"  [PULADO] {container_name} (importante)")
            continue
        
        if dry_run:
            print(f"  [SIMULACAO] Removeria: {container_name} ({container_id[:12]})")
        else:
            print(f"  [REMOVENDO] {container_name} ({container_id[:12]})")
            cmd = ["docker", "rm", container_id]
            result = executar_comando(cmd)
            if result or not result:  # docker rm não retorna output em sucesso
                removidos += 1
                print(f"    [OK] Removido")
            else:
                print(f"    [ERRO] Falha ao remover")
    
    return removidos

def limpar_containers_parados(dry_run: bool = True):
    """Limpa containers parados."""
    print("=" * 70)
    print("LIMPANDO CONTAINERS PARADOS")
    print("=" * 70)
    print()
    
    containers_parados = listar_containers_parados()
    print(f"Containers parados encontrados: {len(containers_parados)}")
    print()
    
    if containers_parados:
        print("Containers parados:")
        for c in containers_parados[:20]:  # Mostra primeiros 20
            print(f"  - {c.get('Names', 'N/A')} ({c.get('Image', 'N/A')})")
        if len(containers_parados) > 20:
            print(f"  ... e mais {len(containers_parados) - 20} containers")
        print()
        
        removidos = remover_containers(containers_parados, dry_run)
        print()
        print(f"Total {'simulado' if dry_run else 'removido'}: {removidos}")
    else:
        print("Nenhum container parado encontrado.")
    
    print()

def limpar_containers_antigos(dias: int = 7, dry_run: bool = True):
    """Limpa containers antigos."""
    print("=" * 70)
    print(f"LIMPANDO CONTAINERS ANTIGOS (mais de {dias} dias)")
    print("=" * 70)
    print()
    
    containers_antigos = listar_containers_antigos(dias)
    print(f"Containers antigos encontrados: {len(containers_antigos)}")
    print()
    
    if containers_antigos:
        print("Containers antigos:")
        for c in containers_antigos[:20]:
            print(f"  - {c.get('Names', 'N/A')} ({c.get('CreatedAt', 'N/A')})")
        if len(containers_antigos) > 20:
            print(f"  ... e mais {len(containers_antigos) - 20} containers")
        print()
        
        removidos = remover_containers(containers_antigos, dry_run)
        print()
        print(f"Total {'simulado' if dry_run else 'removido'}: {removidos}")
    else:
        print("Nenhum container antigo encontrado.")
    
    print()

def limpar_tudo_exceto_importantes(dry_run: bool = True):
    """Limpa tudo exceto containers importantes."""
    print("=" * 70)
    print("LIMPEZA COMPLETA (exceto importantes)")
    print("=" * 70)
    print()
    
    containers = listar_containers()
    
    # Containers importantes (não remover)
    importantes = ['kestra', 'neo4j', 'database', 'ia-test-neo4j', 'ia-test-kestra']
    
    containers_para_remover = []
    for container in containers:
        name = container.get('Names', '').lower()
        state = container.get('State', '')
        
        # Pula importantes
        if any(imp in name for imp in importantes):
            continue
        
        # Remove apenas parados
        if state == 'exited':
            containers_para_remover.append(container)
    
    print(f"Containers para remover: {len(containers_para_remover)}")
    print()
    
    if containers_para_remover:
        print("Containers que serão removidos:")
        for c in containers_para_remover[:30]:
            print(f"  - {c.get('Names', 'N/A')} ({c.get('State', 'N/A')})")
        if len(containers_para_remover) > 30:
            print(f"  ... e mais {len(containers_para_remover) - 30} containers")
        print()
        
        removidos = remover_containers(containers_para_remover, dry_run)
        print()
        print(f"Total {'simulado' if dry_run else 'removido'}: {removidos}")
    else:
        print("Nenhum container para remover.")
    
    print()

def estatisticas():
    """Mostra estatísticas dos containers."""
    containers = listar_containers()
    
    running = len([c for c in containers if c.get('State') == 'running'])
    exited = len([c for c in containers if c.get('State') == 'exited'])
    total = len(containers)
    
    print("=" * 70)
    print("ESTATISTICAS DE CONTAINERS")
    print("=" * 70)
    print()
    print(f"Total de containers: {total}")
    print(f"  - Rodando: {running}")
    print(f"  - Parados: {exited}")
    print()

def main():
    """Função principal."""
    import sys
    
    estatisticas()
    
    # Por padrão, faz simulação
    dry_run = True
    if len(sys.argv) > 1 and sys.argv[1] == "--executar":
        dry_run = False
        print("⚠️  MODO DE EXECUÇÃO REAL - Containers serão removidos!")
        print()
        resposta = input("Tem certeza? (sim/nao): ")
        if resposta.lower() != 'sim':
            print("Operação cancelada.")
            return
        print()
    
    # Limpa containers parados
    limpar_containers_parados(dry_run)
    
    # Limpa containers antigos
    limpar_containers_antigos(dias=7, dry_run=dry_run)
    
    # Estatísticas finais
    if not dry_run:
        print()
        estatisticas()
    
    print("=" * 70)
    if dry_run:
        print("SIMULAÇÃO CONCLUÍDA")
        print("Para executar de verdade, use: python scripts/limpar_containers.py --executar")
    else:
        print("LIMPEZA CONCLUÍDA!")
    print("=" * 70)

if __name__ == "__main__":
    main()
