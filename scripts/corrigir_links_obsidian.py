# -*- coding: utf-8 -*-
"""
Script para corrigir links quebrados no Obsidian
"""

from pathlib import Path
import re

obsidian_path = Path(__file__).parent.parent / "Obsidian_guardar aqui"

def corrigir_links_agentes():
    """Corrige links para agentes."""
    
    mapeamento = {
        "Agentes/Db-Manager": "Agentes/DB-Manager",
        "Agentes/Mcp-Manager": "Agentes/MCP-Manager",
        "Agentes/Mcp-Neo4j-Integration": "Agentes/Neo4j-GraphRAG",
        "Agentes/Mcp-Obsidian-Integration": "Agentes/Obsidian-Integration",
        "Agentes/Mcp-Kestra-Integration": "Agentes/Kestra-Agent",
        "Agentes/Mcp-Docker-Integration": "Agentes/Docker-Integration",
        "Agentes/Agent-Dashboard-Ui": "Agentes/Agent-Dashboard-UI",
        "Agentes/Mcp-Manager-Ui": "Agentes/MCP-Manager-UI",
        "Agentes/Git-Integration": "Agentes/Git-Integration",
    }
    
    for arquivo in obsidian_path.rglob("*.md"):
        with open(arquivo, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        conteudo_original = conteudo
        
        for link_antigo, link_novo in mapeamento.items():
            # Corrige links
            conteudo = re.sub(
                rf'\[\[{re.escape(link_antigo)}\]\]',
                f'[[{link_novo}]]',
                conteudo
            )
            conteudo = re.sub(
                rf'\[\[{re.escape(link_antigo)}\|([^\]]+)\]\]',
                rf'[[{link_novo}|\1]]',
                conteudo
            )
        
        if conteudo != conteudo_original:
            with open(arquivo, 'w', encoding='utf-8') as f:
                f.write(conteudo)
            print(f"Corrigido: {arquivo.name}")

def criar_arquivos_faltantes():
    """Cria arquivos de agentes que estão faltando."""
    
    agentes_faltantes = {
        "Agentes/DB-Manager.md": "# DB Manager\n\nAgente gerenciador de bancos de dados.\n\nVeja: [[PROJETO-IA-TEST|Projeto Principal]]",
        "Agentes/Git-Integration.md": "# Git Integration\n\nAgente de integração com Git/GitHub.\n\nVeja: [[PROJETO-IA-TEST|Projeto Principal]]",
    }
    
    for arquivo_nome, conteudo in agentes_faltantes.items():
        arquivo = obsidian_path / arquivo_nome
        if not arquivo.exists():
            arquivo.parent.mkdir(parents=True, exist_ok=True)
            with open(arquivo, 'w', encoding='utf-8') as f:
                f.write(conteudo)
            print(f"Criado: {arquivo_nome}")

def main():
    """Função principal."""
    print("=" * 70)
    print("CORRIGINDO LINKS DO OBSIDIAN")
    print("=" * 70)
    print()
    
    print("1. Corrigindo links de agentes...")
    corrigir_links_agentes()
    print()
    
    print("2. Criando arquivos faltantes...")
    criar_arquivos_faltantes()
    print()
    
    print("=" * 70)
    print("LINKS CORRIGIDOS!")
    print("=" * 70)

if __name__ == "__main__":
    main()

