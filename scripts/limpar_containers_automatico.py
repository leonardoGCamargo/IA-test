# -*- coding: utf-8 -*-
"""
Script para limpar containers Docker desnecessários automaticamente
"""

import subprocess
import json
import sys
from pathlib import Path

def executar_comando(cmd):
    """Executa comando Docker e retorna resultado."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        return result.stdout.strip(), result.returncode
    except Exception as e:
        return str(e), 1

def listar_containers():
    """Lista todos os containers."""
    cmd = 'docker ps -a --format "{{json .}}"'
    output, code = executar_comando(cmd)
    
    if code != 0:
        print(f"Erro ao listar containers: {output}")
        return []
    
    containers = []
    for line in output.split('\n'):
        if line.strip():
            try:
                containers.append(json.loads(line))
            except:
                pass
    
    return containers

def analisar_containers():
    """Analisa containers."""
    containers = listar_containers()
    
    projeto_containers = []
    parados = []
    outros = []
    
    for container in containers:
        nome = container.get('Names', '')
        status = container.get('Status', '')
        
        if 'ia-test' in nome.lower() or 'kestra' in nome.lower() or 'neo4j' in nome.lower():
            projeto_containers.append(container)
        elif 'Exited' in status or 'Created' in status:
            parados.append(container)
        else:
            outros.append(container)
    
    return {
        'projeto': projeto_containers,
        'parados': parados,
        'outros': outros,
        'total': len(containers)
    }

def limpar_containers_parados():
    """Remove containers parados."""
    containers = listar_containers()
    parados = [c for c in containers if 'Exited' in c.get('Status', '') or 'Created' in c.get('Status', '')]
    
    if not parados:
        return 0, []
    
    removidos = []
    falhas = []
    
    for container in parados:
        nome = container.get('Names', '')
        if nome:
            cmd = f'docker rm {nome}'
            output, code = executar_comando(cmd)
            if code == 0:
                removidos.append(nome)
            else:
                falhas.append((nome, output))
    
    return len(removidos), falhas

def parar_containers_projeto_desnecessarios():
    """Para containers do projeto que não são essenciais."""
    containers = listar_containers()
    projeto_rodando = [
        c for c in containers 
        if ('ia-test' in c.get('Names', '').lower() or 'kestra' in c.get('Names', '').lower())
        and 'Up' in c.get('Status', '')
    ]
    
    # Containers essenciais que devem continuar rodando
    essenciais = ['neo4j', 'agent-dashboard', 'api']
    
    parados = []
    for container in projeto_rodando:
        nome = container.get('Names', '')
        # Se não for essencial, para
        if not any(ess in nome.lower() for ess in essenciais):
            cmd = f'docker stop {nome}'
            output, code = executar_comando(cmd)
            if code == 0:
                parados.append(nome)
    
    return len(parados)

def limpar_imagens_nao_usadas():
    """Limpa imagens não utilizadas."""
    cmd = 'docker image prune -a -f'
    output, code = executar_comando(cmd)
    return code == 0, output

def limpar_volumes_nao_usados():
    """Limpa volumes não utilizados."""
    cmd = 'docker volume prune -f'
    output, code = executar_comando(cmd)
    return code == 0, output

def main():
    """Função principal."""
    print("=" * 70)
    print("LIMPEZA AUTOMATICA DE CONTAINERS DOCKER")
    print("=" * 70)
    print()
    
    # Analisa
    resultado = analisar_containers()
    
    print(f"Total de containers: {resultado['total']}")
    print(f"  - Do projeto: {len(resultado['projeto'])}")
    print(f"  - Parados: {len(resultado['parados'])}")
    print(f"  - Outros: {len(resultado['outros'])}")
    print()
    
    # Limpa containers parados
    print("1. REMOVENDO CONTAINERS PARADOS...")
    removidos, falhas = limpar_containers_parados()
    print(f"   Removidos: {removidos}")
    if falhas:
        print(f"   Falhas: {len(falhas)}")
        for nome, erro in falhas[:3]:
            print(f"     - {nome}: {erro[:50]}")
    print()
    
    # Para containers desnecessários do projeto
    print("2. PARANDO CONTAINERS DESNECESSARIOS DO PROJETO...")
    parados = parar_containers_projeto_desnecessarios()
    print(f"   Parados: {parados}")
    print()
    
    # Limpa imagens
    print("3. LIMPANDO IMAGENS NAO UTILIZADAS...")
    sucesso, output = limpar_imagens_nao_usadas()
    if sucesso:
        print("   Imagens limpas!")
    else:
        print(f"   Erro: {output[:100]}")
    print()
    
    # Limpa volumes
    print("4. LIMPANDO VOLUMES NAO UTILIZADOS...")
    sucesso, output = limpar_volumes_nao_usados()
    if sucesso:
        print("   Volumes limpos!")
    else:
        print(f"   Erro: {output[:100]}")
    print()
    
    # Estatísticas finais
    resultado_final = analisar_containers()
    print("=" * 70)
    print("RESULTADO FINAL")
    print("=" * 70)
    print(f"Containers antes: {resultado['total']}")
    print(f"Containers depois: {resultado_final['total']}")
    print(f"Reducao: {resultado['total'] - resultado_final['total']} containers")
    print()
    print(f"Containers rodando: {len([c for c in resultado_final['outros'] + resultado_final['projeto'] if 'Up' in c.get('Status', '')])}")
    print()

if __name__ == "__main__":
    main()

