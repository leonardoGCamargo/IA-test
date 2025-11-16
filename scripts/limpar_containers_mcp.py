# -*- coding: utf-8 -*-
"""
Script para limpar containers MCP órfãos
Remove containers com nomes aleatórios que são órfãos do MCP
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

def listar_containers_orfos():
    """Lista containers órfãos (nomes aleatórios)."""
    cmd = ["docker", "ps", "--format", "json"]
    sucesso, output = executar_comando(cmd)
    
    if not sucesso:
        return []
    
    containers = []
    for line in output.split('\n'):
        if line.strip():
            try:
                container = json.loads(line)
                name = container.get('Names', '')
                
                # Containers importantes (não remover)
                importantes = ['ia-test', 'dokploy', 'n8n', 'postgres', 'redis', 'ollama', 'kestra', 'neo4j', 'traefik']
                if any(imp in name.lower() for imp in importantes):
                    continue
                
                # Containers com nomes aleatórios (padrão: palavra_palavra)
                if '_' in name and len(name.split('_')) == 2:
                    palavras = name.split('_')
                    if all(len(p) > 3 for p in palavras):
                        containers.append(container)
            except:
                pass
    
    return containers

def parar_e_remover(container_id, container_name):
    """Para e remove container."""
    print(f"  [PARANDO] {container_name}")
    cmd_stop = ["docker", "stop", container_id]
    sucesso, _ = executar_comando(cmd_stop)
    
    if sucesso:
        print(f"  [REMOVENDO] {container_name}")
        cmd_rm = ["docker", "rm", container_id]
        sucesso, _ = executar_comando(cmd_rm)
        return sucesso
    return False

def main():
    """Função principal."""
    print("=" * 70)
    print("LIMPEZA DE CONTAINERS MCP ORFAOS")
    print("=" * 70)
    print()
    
    orfos = listar_containers_orfos()
    print(f"Containers órfãos encontrados: {len(orfos)}")
    print()
    
    if not orfos:
        print("Nenhum container órfão encontrado.")
        return
    
    print("Containers que serão removidos:")
    for c in orfos[:30]:
        print(f"  - {c.get('Names', 'N/A')} ({c.get('Image', 'N/A')[:50]})")
    if len(orfos) > 30:
        print(f"  ... e mais {len(orfos) - 30} containers")
    print()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--executar":
        print(f"[ATENCAO] {len(orfos)} containers serao PARADOS e REMOVIDOS!")
        resposta = input("Confirma? Digite 'SIM': ")
        if resposta != 'SIM':
            print("Cancelado.")
            return
        
        print()
        removidos = 0
        for container in orfos:
            if parar_e_remover(container.get('ID', ''), container.get('Names', '')):
                removidos += 1
        
        print()
        print("=" * 70)
        print(f"✅ Removidos: {removidos}/{len(orfos)}")
        print("=" * 70)
    else:
        print("=" * 70)
        print("SIMULAÇÃO")
        print(f"Total que seria removido: {len(orfos)}")
        print()
        print("Para executar:")
        print("  python scripts/limpar_containers_mcp.py --executar")
        print("=" * 70)

if __name__ == "__main__":
    main()

