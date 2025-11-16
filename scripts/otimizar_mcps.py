# -*- coding: utf-8 -*-
"""
Script para otimizar configuração de MCPs
Mantém apenas os essenciais e remove redundâncias
"""

import json
from pathlib import Path
from typing import Dict

project_root = Path(__file__).parent.parent

# MCPs essenciais (manter sempre)
MCPS_ESSENCIAIS = {
    "neo4j": {
        "name": "neo4j",
        "command": "npx",
        "args": ["-y", "@neo4j/mcp-server-neo4j"],
        "enabled": True,
        "description": "Neo4j GraphRAG e conhecimento estruturado"
    },
    "obsidian": {
        "name": "obsidian",
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-obsidian"],
        "enabled": True,
        "description": "Gestão de notas Obsidian"
    },
    "git": {
        "name": "git",
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-git"],
        "enabled": True,
        "description": "Operações Git/GitHub"
    }
}

# MCPs opcionais (desabilitar por padrão)
MCPS_OPCIONAIS = {
    "filesystem": {
        "name": "filesystem",
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem"],
        "enabled": False,
        "description": "Acesso ao sistema de arquivos (opcional)"
    }
}

def criar_configuracao_otimizada():
    """Cria configuração otimizada de MCPs."""
    config = {}
    
    # Adiciona MCPs essenciais
    config.update(MCPS_ESSENCIAIS)
    
    # Adiciona MCPs opcionais (desabilitados)
    config.update(MCPS_OPCIONAIS)
    
    return config

def otimizar_mcp_servers_json():
    """Otimiza mcp_servers.json."""
    config_file = project_root / "mcp_servers.json"
    
    # Cria configuração otimizada
    config_otimizada = criar_configuracao_otimizada()
    
    # Se arquivo existe, preserva configurações customizadas
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config_existente = json.load(f)
            
            # Preserva MCPs essenciais existentes
            for nome, mcp_essencial in MCPS_ESSENCIAIS.items():
                if nome in config_existente:
                    # Mantém configuração existente mas garante que está habilitado
                    config_existente[nome]["enabled"] = True
                    config_otimizada[nome] = config_existente[nome]
        except Exception as e:
            print(f"Erro ao ler config existente: {e}")
    
    # Salva configuração otimizada
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config_otimizada, f, indent=2, ensure_ascii=False)
    
    return config_otimizada

def main():
    """Função principal."""
    print("=" * 70)
    print("OTIMIZANDO CONFIGURACAO DE MCPS")
    print("=" * 70)
    print()
    
    print("Criando configuração otimizada...")
    config = otimizar_mcp_servers_json()
    
    print(f"\nMCPs configurados: {len(config)}")
    print("\nMCPs ESSENCIAIS (habilitados):")
    for nome, mcp in config.items():
        if mcp.get("enabled", True) and nome in MCPS_ESSENCIAIS:
            print(f"  [OK] {nome}: {mcp.get('description', '')}")
    
    print("\nMCPs OPCIONAIS (desabilitados):")
    for nome, mcp in config.items():
        if not mcp.get("enabled", True):
            print(f"  [OPCIONAL] {nome}: {mcp.get('description', '')}")
    
    print()
    print("=" * 70)
    print("OTIMIZACAO CONCLUIDA!")
    print("=" * 70)
    print()
    print(f"Arquivo atualizado: mcp_servers.json")
    print(f"Total MCPs: {len(config)}")
    print(f"  - Essenciais: {len([m for n, m in config.items() if m.get('enabled') and n in MCPS_ESSENCIAIS])}")
    print(f"  - Opcionais: {len([m for n, m in config.items() if not m.get('enabled')])}")

if __name__ == "__main__":
    main()

