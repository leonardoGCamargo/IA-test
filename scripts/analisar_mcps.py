# -*- coding: utf-8 -*-
"""
Script para analisar MCPs configurados e identificar redundâncias
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Set
import re

project_root = Path(__file__).parent.parent

def encontrar_mcps_no_codigo():
    """Encontra quais MCPs são referenciados no código."""
    mcps_encontrados = set()
    
    # Busca em arquivos Python
    for py_file in project_root.rglob("*.py"):
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                conteudo = f.read()
                
                # Busca referências a MCPs
                # Padrões: "server-", "@modelcontextprotocol/", "mcp-server"
                padroes = [
                    r'@modelcontextprotocol/server-(\w+)',
                    r'@(\w+)/mcp-server-(\w+)',
                    r'mcp-server-(\w+)',
                    r'server-(\w+)',
                ]
                
                for padrao in padroes:
                    matches = re.findall(padrao, conteudo, re.IGNORECASE)
                    for match in matches:
                        if isinstance(match, tuple):
                            mcps_encontrados.update(match)
                        else:
                            mcps_encontrados.add(match)
        except Exception as e:
            pass
    
    return mcps_encontrados

def carregar_mcps_configurados():
    """Carrega MCPs do arquivo de configuração."""
    config_file = project_root / "mcp_servers.json"
    cursor_config = project_root / ".cursor" / "mcp.json"
    
    mcps = {}
    
    # Tenta carregar mcp_servers.json
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                mcps.update(data)
        except Exception as e:
            print(f"Erro ao ler mcp_servers.json: {e}")
    
    # Tenta carregar .cursor/mcp.json
    if cursor_config.exists():
        try:
            with open(cursor_config, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if "mcpServers" in data:
                    mcps.update(data["mcpServers"])
        except Exception as e:
            print(f"Erro ao ler .cursor/mcp.json: {e}")
    
    return mcps

def analisar_mcps_padrao():
    """Analisa quais MCPs são criados por padrão."""
    # Lê o código do mcp_manager.py
    mcp_manager_file = project_root / "src" / "agents" / "mcp_manager.py"
    
    mcps_padrao = []
    
    if mcp_manager_file.exists():
        with open(mcp_manager_file, 'r', encoding='utf-8') as f:
            conteudo = f.read()
            
            # Busca por padrões de servidores padrão
            # Procura por MCPServer( ou "name":
            padroes = [
                r'name=["\'](\w+)["\']',
                r'"name":\s*["\'](\w+)["\']',
            ]
            
            for padrao in padroes:
                matches = re.findall(padrao, conteudo)
                mcps_padrao.extend(matches)
    
    return list(set(mcps_padrao))

def verificar_uso_mcps():
    """Verifica quais MCPs estão sendo realmente usados."""
    print("=" * 70)
    print("ANALISANDO MCPS DO SISTEMA")
    print("=" * 70)
    print()
    
    # 1. MCPs configurados
    mcps_configurados = carregar_mcps_configurados()
    print(f"1. MCPs Configurados: {len(mcps_configurados)}")
    for nome, config in mcps_configurados.items():
        enabled = config.get("enabled", True)
        status = "HABILITADO" if enabled else "DESABILITADO"
        print(f"   - {nome}: {status}")
    print()
    
    # 2. MCPs no código
    mcps_no_codigo = encontrar_mcps_no_codigo()
    print(f"2. MCPs Referenciados no Código: {len(mcps_no_codigo)}")
    for mcp in sorted(mcps_no_codigo):
        if mcp:
            print(f"   - {mcp}")
    print()
    
    # 3. MCPs padrão
    mcps_padrao = analisar_mcps_padrao()
    print(f"3. MCPs Criados por Padrão: {len(mcps_padrao)}")
    for mcp in sorted(mcps_padrao):
        print(f"   - {mcp}")
    print()
    
    # 4. Análise de redundâncias
    print("4. ANALISE DE REDUNDANCIAS:")
    print()
    
    # MCPs configurados mas não usados
    mcps_nao_usados = set(mcps_configurados.keys()) - mcps_no_codigo
    if mcps_nao_usados:
        print(f"   MCPs Configurados mas NAO Usados ({len(mcps_nao_usados)}):")
        for mcp in sorted(mcps_nao_usados):
            print(f"     - {mcp} (pode ser removido)")
    else:
        print("   Nenhum MCP configurado mas não usado encontrado.")
    print()
    
    # MCPs duplicados
    print("5. RECOMENDACOES:")
    print()
    
    # MCPs essenciais (baseado no uso do projeto)
    mcps_essenciais = {
        "neo4j": "GraphRAG e conhecimento",
        "obsidian": "Gestão de notas",
        "git": "Integração Git",
    }
    
    print("   MCPs ESSENCIAIS (manter):")
    for mcp, motivo in mcps_essenciais.items():
        if mcp in mcps_configurados:
            print(f"     - {mcp}: {motivo}")
    print()
    
    print("   MCPs OPCIONAIS (pode remover se não usar):")
    mcps_opcionais = ["filesystem", "puppeteer", "brave-search", "github"]
    for mcp in mcps_opcionais:
        if mcp in mcps_configurados:
            enabled = mcps_configurados[mcp].get("enabled", True)
            if not enabled:
                print(f"     - {mcp}: DESABILITADO (pode remover)")
            else:
                print(f"     - {mcp}: HABILITADO (verificar se usa)")
    print()
    
    return {
        "configurados": mcps_configurados,
        "no_codigo": mcps_no_codigo,
        "padrao": mcps_padrao,
        "nao_usados": mcps_nao_usados,
    }

def criar_relatorio_limpeza(analise):
    """Cria relatório de limpeza."""
    relatorio = {
        "total_configurados": len(analise["configurados"]),
        "total_no_codigo": len(analise["no_codigo"]),
        "total_nao_usados": len(analise["nao_usados"]),
        "mcps_para_remover": list(analise["nao_usados"]),
        "mcps_essenciais": ["neo4j", "obsidian", "git"],
    }
    
    return relatorio

def main():
    """Função principal."""
    analise = verificar_uso_mcps()
    relatorio = criar_relatorio_limpeza(analise)
    
    print("=" * 70)
    print("RELATORIO DE LIMPEZA")
    print("=" * 70)
    print()
    print(f"Total MCPs configurados: {relatorio['total_configurados']}")
    print(f"Total MCPs não usados: {relatorio['total_nao_usados']}")
    print()
    
    if relatorio["mcps_para_remover"]:
        print("MCPs que PODEM ser removidos:")
        for mcp in relatorio["mcps_para_remover"]:
            print(f"  - {mcp}")
    else:
        print("Nenhum MCP identificado para remoção.")
    
    print()
    print("=" * 70)
    print("ANALISE CONCLUIDA")
    print("=" * 70)
    print()
    print("Proximo passo:")
    print("  python scripts/limpar_mcps.py")
    print()
    
    # Salva relatório
    relatorio_file = project_root / "Obsidian_guardar aqui" / "RELATORIO-LIMPEZA-MCPS.json"
    with open(relatorio_file, 'w', encoding='utf-8') as f:
        json.dump(relatorio, f, indent=2, ensure_ascii=False)
    
    print(f"Relatorio salvo em: {relatorio_file}")

if __name__ == "__main__":
    main()

