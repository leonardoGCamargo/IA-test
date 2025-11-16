# -*- coding: utf-8 -*-
"""
Script para remover containers órfãos automaticamente
"""

import subprocess
import json

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
    """Lista containers órfãos."""
    cmd = ["docker", "ps", "-a", "--format", "json"]
    sucesso, output = executar_comando(cmd)
    
    if not sucesso:
        return []
    
    containers = []
    manter = ['ia-test', 'n8n', 'dokploy', 'postgres', 'redis', 'ollama', 'kestra', 'neo4j', 'traefik']
    
    for line in output.split('\n'):
        if line.strip():
            try:
                container = json.loads(line)
                name = container.get('Names', '').lower()
                
                # Mantém containers importantes
                if any(imp in name for imp in manter):
                    continue
                
                # Remove containers órfãos (nomes aleatórios)
                # Padrão: palavra_palavra (ex: cool_chaplygin, sad_beaver, zen_noyce)
                if '_' in name and len(name.split('_')) == 2:
                    palavras = name.split('_')
                    # Aceita se ambas palavras têm pelo menos 3 letras
                    if all(len(p) >= 3 for p in palavras):
                        containers.append(container)
            except:
                pass
    
    return containers

def main():
    """Função principal."""
    print("=" * 70)
    print("REMOVENDO CONTAINERS ORFAOS")
    print("=" * 70)
    print()
    
    orfos = listar_containers_orfos()
    print(f"Containers orfaos encontrados: {len(orfos)}")
    print()
    
    if not orfos:
        print("Nenhum container orfao encontrado.")
        return
    
    removidos = 0
    for container in orfos:
        container_id = container.get('ID', '')
        container_name = container.get('Names', '')
        
        print(f"[REMOVENDO] {container_name}")
        cmd = ["docker", "rm", "-f", container_id]
        sucesso, _ = executar_comando(cmd)
        
        if sucesso:
            removidos += 1
            print(f"  [OK] Removido")
        else:
            print(f"  [ERRO] Falha ao remover")
    
    print()
    print("=" * 70)
    print(f"[OK] Removidos: {removidos}/{len(orfos)}")
    print("=" * 70)

if __name__ == "__main__":
    main()

