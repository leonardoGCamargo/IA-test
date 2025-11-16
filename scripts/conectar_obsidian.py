# -*- coding: utf-8 -*-
"""
Script para conectar nós do Obsidian que estão desconectados
"""

from pathlib import Path
import re

obsidian_path = Path(__file__).parent.parent / "Obsidian_guardar aqui"

def encontrar_links_quebrados():
    """Encontra links quebrados no Obsidian."""
    links_quebrados = {}
    
    for arquivo in obsidian_path.rglob("*.md"):
        with open(arquivo, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        # Encontra todos os links [[...]]
        links = re.findall(r'\[\[([^\]]+)\]\]', conteudo)
        
        for link in links:
            # Remove alias se houver
            link_clean = link.split('|')[0].strip()
            
            # Verifica se arquivo existe
            possiveis_caminhos = [
                obsidian_path / f"{link_clean}.md",
                obsidian_path / f"{link_clean}",
                obsidian_path / "Agentes" / f"{link_clean}.md",
            ]
            
            existe = any(p.exists() for p in possiveis_caminhos)
            
            if not existe:
                if arquivo.name not in links_quebrados:
                    links_quebrados[arquivo.name] = []
                links_quebrados[arquivo.name].append(link_clean)
    
    return links_quebrados

def corrigir_links_comuns():
    """Corrige links comuns que podem estar quebrados."""
    
    mapeamento = {
        "Db-Manager": "DB-Manager",
        "Mcp-Manager": "MCP-Manager",
        "Mcp-Neo4j-Integration": "Neo4j-GraphRAG",
        "Mcp-Obsidian-Integration": "Obsidian-Integration",
        "Mcp-Kestra-Integration": "Kestra-Agent",
        "Mcp-Docker-Integration": "Docker-Integration",
        "Agent-Dashboard-Ui": "Agent-Dashboard-UI",
        "Mcp-Manager-Ui": "MCP-Manager-UI",
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

def adicionar_links_faltantes():
    """Adiciona links importantes que estão faltando."""
    
    arquivos_principais = {
        "PROJETO-IA-TEST.md": [
            "LANGCHAIN-LANGGRAPH-GUIA",
            "PREPARACAO-LANGCHAIN",
            "RESUMO-LANGCHAIN-PREPARACAO",
        ],
        "00-MAPA-DE-AGENTES.md": [
            "LANGCHAIN-LANGGRAPH-GUIA",
            "LANGCHAIN-FUNDAMENTOS",
        ],
        "PREPARACAO-LANGCHAIN.md": [
            "LANGCHAIN-LANGGRAPH-GUIA",
            "LANGCHAIN-FUNDAMENTOS",
            "LANGGRAPH-CONCEITOS",
            "LANGGRAPH-WORKFLOWS",
        ],
    }
    
    for arquivo_nome, links in arquivos_principais.items():
        arquivo = obsidian_path / arquivo_nome
        if arquivo.exists():
            with open(arquivo, 'r', encoding='utf-8') as f:
                conteudo = f.read()
            
            # Adiciona links se não existirem
            for link in links:
                if f"[[{link}]]" not in conteudo:
                    # Adiciona na seção de links ou no final
                    if "## 🔗 Links" in conteudo:
                        conteudo = conteudo.replace(
                            "## 🔗 Links",
                            f"## 🔗 Links\n\n- [[{link}]]"
                        )
                    elif "## 📚" in conteudo:
                        conteudo = conteudo.replace(
                            "## 📚",
                            f"## 🔗 Links Relacionados\n\n- [[{link}]]\n\n## 📚"
                        )
                    else:
                        conteudo += f"\n\n## 🔗 Links\n\n- [[{link}]]"
            
            with open(arquivo, 'w', encoding='utf-8') as f:
                f.write(conteudo)
            
            print(f"Atualizado: {arquivo_nome}")

def main():
    """Função principal."""
    print("=" * 70)
    print("CONECTANDO NOS DO OBSIDIAN")
    print("=" * 70)
    print()
    
    print("1. Corrigindo links comuns...")
    corrigir_links_comuns()
    print()
    
    print("2. Adicionando links faltantes...")
    adicionar_links_faltantes()
    print()
    
    print("3. Verificando links quebrados...")
    links_quebrados = encontrar_links_quebrados()
    
    if links_quebrados:
        print("Links quebrados encontrados:")
        for arquivo, links in links_quebrados.items():
            print(f"  {arquivo}: {', '.join(links)}")
    else:
        print("✅ Nenhum link quebrado encontrado!")
    
    print()
    print("=" * 70)
    print("CONEXOES ATUALIZADAS!")
    print("=" * 70)

if __name__ == "__main__":
    main()

