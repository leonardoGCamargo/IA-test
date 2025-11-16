# -*- coding: utf-8 -*-
"""
Script para identificar todas as redundâncias do sistema
"""

import os
from pathlib import Path
from typing import Dict, List, Set
import json

project_root = Path(__file__).parent.parent

def identificar_agentes_redundantes():
    """Identifica agentes redundantes."""
    redundancias = []
    
    # Verifica kestra_langchain_master.py
    master_file = project_root / "src" / "agents" / "kestra_langchain_master.py"
    orchestrator_file = project_root / "src" / "agents" / "orchestrator.py"
    
    if master_file.exists() and orchestrator_file.exists():
        # Verifica se orchestrator tem as funcionalidades
        with open(orchestrator_file, 'r', encoding='utf-8') as f:
            orchestrator_content = f.read()
        
        if "execute_goal" in orchestrator_content and "planejamento inteligente" in orchestrator_content.lower():
            redundancias.append({
                "arquivo": "kestra_langchain_master.py",
                "motivo": "Funcionalidades já no orchestrator.py",
                "acao": "REMOVER"
            })
    
    # Verifica agent_dashboard_ui.py vs agent_dashboard.py
    dashboard_ui = project_root / "src" / "agents" / "agent_dashboard_ui.py"
    dashboard_app = project_root / "src" / "apps" / "agent_dashboard.py"
    
    if dashboard_ui.exists() and dashboard_app.exists():
        redundancias.append({
            "arquivo": "agent_dashboard_ui.py",
            "motivo": "Pode ser redundante com agent_dashboard.py",
            "acao": "VERIFICAR"
        })
    
    return redundancias

def identificar_docs_redundantes():
    """Identifica documentação redundante."""
    docs_path = project_root / "docs"
    
    grupos = {
        "dashboard": [],
        "organizacao": [],
        "mcp": [],
    }
    
    for doc_file in docs_path.glob("*.md"):
        nome = doc_file.stem.lower()
        
        if "dashboard" in nome:
            grupos["dashboard"].append(doc_file.name)
        elif "organizacao" in nome or "organiz" in nome:
            grupos["organizacao"].append(doc_file.name)
        elif "mcp" in nome:
            grupos["mcp"].append(doc_file.name)
    
    redundancias = []
    for grupo, arquivos in grupos.items():
        if len(arquivos) > 1:
            redundancias.append({
                "grupo": grupo,
                "arquivos": arquivos,
                "quantidade": len(arquivos),
                "acao": "CONSOLIDAR"
            })
    
    return redundancias

def identificar_docker_compose_redundantes():
    """Identifica docker-compose redundantes."""
    config_path = project_root / "config"
    
    docker_files = list(config_path.glob("docker-compose*.yml"))
    
    if len(docker_files) > 1:
        return {
            "quantidade": len(docker_files),
            "arquivos": [f.name for f in docker_files],
            "acao": "CONSOLIDAR em 1 versão"
        }
    
    return None

def main():
    """Função principal."""
    print("=" * 70)
    print("IDENTIFICANDO REDUNDANCIAS DO SISTEMA")
    print("=" * 70)
    print()
    
    # 1. Agentes redundantes
    print("1. AGENTES REDUNDANTES:")
    agentes = identificar_agentes_redundantes()
    if agentes:
        for agente in agentes:
            print(f"   - {agente['arquivo']}")
            print(f"     Motivo: {agente['motivo']}")
            print(f"     Acao: {agente['acao']}")
            print()
    else:
        print("   Nenhum agente redundante encontrado.")
    print()
    
    # 2. Documentação redundante
    print("2. DOCUMENTACAO REDUNDANTE:")
    docs = identificar_docs_redundantes()
    if docs:
        for doc in docs:
            print(f"   - {doc['grupo'].upper()}: {doc['quantidade']} arquivos")
            for arquivo in doc['arquivos']:
                print(f"     * {arquivo}")
            print(f"     Acao: {doc['acao']}")
            print()
    else:
        print("   Nenhuma documentação redundante encontrada.")
    print()
    
    # 3. Docker Compose redundantes
    print("3. DOCKER COMPOSE REDUNDANTES:")
    docker = identificar_docker_compose_redundantes()
    if docker:
        print(f"   Quantidade: {docker['quantidade']}")
        for arquivo in docker['arquivos']:
            print(f"     - {arquivo}")
        print(f"   Acao: {docker['acao']}")
    else:
        print("   Nenhum docker-compose redundante encontrado.")
    print()
    
    # Resumo
    print("=" * 70)
    print("RESUMO")
    print("=" * 70)
    print(f"Agentes redundantes: {len(agentes)}")
    print(f"Grupos de docs redundantes: {len(docs)}")
    print(f"Docker compose redundantes: {'Sim' if docker else 'Nao'}")
    print()
    
    # Salva relatório
    relatorio = {
        "agentes": agentes,
        "documentacao": docs,
        "docker_compose": docker,
    }
    
    relatorio_file = project_root / "Obsidian_guardar aqui" / "RELATORIO-REDUNDANCIAS.json"
    with open(relatorio_file, 'w', encoding='utf-8') as f:
        json.dump(relatorio, f, indent=2, ensure_ascii=False)
    
    print(f"Relatorio salvo em: {relatorio_file}")

if __name__ == "__main__":
    main()

