# -*- coding: utf-8 -*-
"""
Script agressivo para limpar containers desnecessários
Remove containers órfãos com nomes aleatórios
"""

import subprocess
import json
import sys
from typing import List

def executar_comando(cmd: List[str]) -> tuple:
    """Executa comando Docker e retorna (sucesso, output)."""
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

def listar_containers_rodando():
    """Lista containers rodando."""
    cmd = ["docker", "ps", "--format", "json"]
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

def identificar_containers_importantes():
    """Lista containers importantes que NÃO devem ser removidos."""
    importantes = [
        'ia-test',  # Containers do projeto IA-test
        'dokploy',  # Dokploy
        'n8n',      # N8N
        'postgres', # PostgreSQL
        'redis',    # Redis
        'ollama',   # Ollama
        'kestra',   # Kestra
        'neo4j',    # Neo4j
        'traefik',  # Traefik
        'database', # Database genérico
    ]
    return importantes

def identificar_containers_orfos(containers):
    """Identifica containers órfãos (nomes aleatórios)."""
    importantes = identificar_containers_importantes()
    orfos = []
    
    for container in containers:
        name = container.get('Names', '').lower()
        
        # Pula containers importantes
        if any(imp in name for imp in importantes):
            continue
        
        # Containers com nomes aleatórios (geralmente têm underscore e são palavras aleatórias)
        # Ex: cool_chaplygin, gracious_newton, etc.
        if '_' in name and len(name.split('_')) == 2:
            # Verifica se parece ser um nome aleatório (não é um nome de projeto)
            palavras = name.split('_')
            if all(len(p) > 3 for p in palavras):  # Ambas palavras têm mais de 3 letras
                orfos.append(container)
    
    return orfos

def parar_e_remover_container(container_id: str, container_name: str) -> bool:
    """Para e remove um container."""
    print(f"  [PARANDO] {container_name} ({container_id[:12]})")
    
    # Para o container
    cmd_stop = ["docker", "stop", container_id]
    sucesso, _ = executar_comando(cmd_stop)
    
    if not sucesso:
        print(f"    [ERRO] Falha ao parar container")
        return False
    
    # Remove o container
    cmd_rm = ["docker", "rm", container_id]
    sucesso, _ = executar_comando(cmd_rm)
    
    if sucesso:
        print(f"    [OK] Removido com sucesso")
        return True
    else:
        print(f"    [ERRO] Falha ao remover")
        return False

def main():
    """Função principal."""
    print("=" * 70)
    print("LIMPEZA AGRESSIVA DE CONTAINERS")
    print("=" * 70)
    print()
    
    # Lista containers rodando
    print("Analisando containers...")
    containers = listar_containers_rodando()
    print(f"Total de containers rodando: {len(containers)}")
    print()
    
    # Identifica containers importantes
    importantes = identificar_containers_importantes()
    containers_importantes = [
        c for c in containers
        if any(imp in c.get('Names', '').lower() for imp in importantes)
    ]
    print(f"Containers importantes (não serão removidos): {len(containers_importantes)}")
    for c in containers_importantes:
        print(f"  - {c.get('Names', 'N/A')}")
    print()
    
    # Identifica órfãos
    orfos = identificar_containers_orfos(containers)
    print(f"Containers órfãos identificados: {len(orfos)}")
    print()
    
    if not orfos:
        print("Nenhum container órfão encontrado.")
        return
    
    # Mostra containers que serão removidos
    print("Containers que serão removidos:")
    for c in orfos[:20]:
        print(f"  - {c.get('Names', 'N/A')} ({c.get('Image', 'N/A')})")
    if len(orfos) > 20:
        print(f"  ... e mais {len(orfos) - 20} containers")
    print()
    
    # Confirmação
    if len(sys.argv) > 1 and sys.argv[1] == "--executar":
        print("⚠️  MODO DE EXECUÇÃO REAL")
        print(f"⚠️  {len(orfos)} containers serão PARADOS e REMOVIDOS!")
        print()
        resposta = input("Tem certeza? Digite 'SIM' para confirmar: ")
        if resposta != 'SIM':
            print("Operação cancelada.")
            return
        print()
        
        # Remove containers
        removidos = 0
        for container in orfos:
            container_id = container.get('ID', '')
            container_name = container.get('Names', '')
            
            if container_id and parar_e_remover_container(container_id, container_name):
                removidos += 1
        
        print()
        print("=" * 70)
        print(f"LIMPEZA CONCLUÍDA!")
        print(f"Containers removidos: {removidos}/{len(orfos)}")
        print("=" * 70)
    else:
        print("=" * 70)
        print("SIMULAÇÃO CONCLUÍDA")
        print(f"Total de containers que seriam removidos: {len(orfos)}")
        print()
        print("Para executar de verdade, use:")
        print("  python scripts/limpar_containers_agressivo.py --executar")
        print("=" * 70)

if __name__ == "__main__":
    main()
