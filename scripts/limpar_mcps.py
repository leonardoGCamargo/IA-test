# -*- coding: utf-8 -*-
"""
Script para limpar MCPs desnecessários
"""

import json
from pathlib import Path
from typing import Dict, List

project_root = Path(__file__).parent.parent

def carregar_relatorio():
    """Carrega relatório de análise."""
    relatorio_file = project_root / "Obsidian_guardar aqui" / "RELATORIO-LIMPEZA-MCPS.json"
    
    if not relatorio_file.exists():
        print("Relatorio nao encontrado. Execute analisar_mcps.py primeiro.")
        return None
    
    with open(relatorio_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def limpar_mcp_servers_json(mcps_para_remover: List[str]):
    """Remove MCPs do mcp_servers.json."""
    config_file = project_root / "mcp_servers.json"
    
    if not config_file.exists():
        print("mcp_servers.json nao encontrado.")
        return False
    
    with open(config_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    removidos = 0
    for mcp in mcps_para_remover:
        if mcp in data:
            del data[mcp]
            removidos += 1
            print(f"  Removido: {mcp}")
    
    if removidos > 0:
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"\n  Total removidos: {removidos}")
        return True
    
    return False

def limpar_cursor_mcp_json(mcps_para_remover: List[str]):
    """Remove MCPs do .cursor/mcp.json."""
    cursor_config = project_root / ".cursor" / "mcp.json"
    
    if not cursor_config.exists():
        return False
    
    with open(cursor_config, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if "mcpServers" not in data:
        return False
    
    removidos = 0
    for mcp in mcps_para_remover:
        if mcp in data["mcpServers"]:
            del data["mcpServers"][mcp]
            removidos += 1
    
    if removidos > 0:
        with open(cursor_config, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    
    return False

def desabilitar_mcps_opcionais():
    """Desabilita MCPs opcionais em vez de remover."""
    config_file = project_root / "mcp_servers.json"
    
    if not config_file.exists():
        return False
    
    with open(config_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    mcps_opcionais = ["filesystem", "puppeteer", "brave-search"]
    desabilitados = 0
    
    for mcp in mcps_opcionais:
        if mcp in data:
            if data[mcp].get("enabled", True):
                data[mcp]["enabled"] = False
                desabilitados += 1
                print(f"  Desabilitado: {mcp}")
    
    if desabilitados > 0:
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"\n  Total desabilitados: {desabilitados}")
        return True
    
    return False

def main():
    """Função principal."""
    print("=" * 70)
    print("LIMPEZA DE MCPS")
    print("=" * 70)
    print()
    
    relatorio = carregar_relatorio()
    if not relatorio:
        return
    
    print("Opcoes:")
    print("1. Remover MCPs não usados")
    print("2. Desabilitar MCPs opcionais")
    print("3. Ambos")
    print()
    
    opcao = input("Escolha opcao (1/2/3): ").strip()
    
    if opcao == "1" or opcao == "3":
        print("\n1. Removendo MCPs não usados...")
        if relatorio["mcps_para_remover"]:
            limpar_mcp_servers_json(relatorio["mcps_para_remover"])
            limpar_cursor_mcp_json(relatorio["mcps_para_remover"])
        else:
            print("  Nenhum MCP para remover.")
    
    if opcao == "2" or opcao == "3":
        print("\n2. Desabilitando MCPs opcionais...")
        desabilitar_mcps_opcionais()
    
    print()
    print("=" * 70)
    print("LIMPEZA CONCLUIDA!")
    print("=" * 70)

if __name__ == "__main__":
    main()

