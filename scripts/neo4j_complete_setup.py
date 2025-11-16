"""
Script Master - Executa população completa e melhorias do Neo4j.

Este script executa em sequência:
1. População inicial do Neo4j
2. Melhorias de relações e índices
3. Análise do código e MCP
4. Geração de relatório final

Uso:
    python scripts/neo4j_complete_setup.py
"""

import sys
import subprocess
from pathlib import Path
from datetime import datetime

project_root = Path(__file__).parent.parent

def run_script(script_name, description):
    """Executa um script Python e retorna o resultado."""
    print("\n" + "=" * 80)
    print(f"{description}")
    print("=" * 80)
    print()
    
    script_path = project_root / "scripts" / script_name
    
    if not script_path.exists():
        print(f"ERRO: Script {script_name} não encontrado!")
        return False
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=str(project_root),
            capture_output=False,
            text=True
        )
        return result.returncode == 0
    except Exception as e:
        print(f"ERRO ao executar {script_name}: {e}")
        return False

def main():
    """Executa o setup completo do Neo4j."""
    print("=" * 80)
    print("SETUP COMPLETO DO NEO4J - IA-Test Project")
    print("=" * 80)
    print()
    print("Este script irá:")
    print("  1. Popular o Neo4j com dados do projeto")
    print("  2. Melhorar relações e criar índices")
    print("  3. Analisar código e adicionar relações baseadas no código")
    print("  4. Gerar relatório final")
    print()
    print("Iniciando em 2 segundos...")
    import time
    time.sleep(2)
    print()
    
    # 1. População inicial
    if not run_script("populate_neo4j_complete.py", "1. POPULANDO NEO4J COM DADOS DO PROJETO"):
        print("\nAVISO: População inicial falhou, mas continuando...")
    
    # 2. Melhorias de relações
    if not run_script("enhance_neo4j_relationships.py", "2. MELHORANDO RELAÇÕES E CRIANDO ÍNDICES"):
        print("\nAVISO: Melhorias de relações falharam, mas continuando...")
    
    # 3. Análise do código e MCP
    if not run_script("neo4j_mcp_enhancement.py", "3. ANALISANDO CÓDIGO E APLICANDO MELHORIAS DO MCP"):
        print("\nAVISO: Análise do código falhou, mas continuando...")
    
    # Relatório final
    print("\n" + "=" * 80)
    print("SETUP COMPLETO!")
    print("=" * 80)
    print()
    print("Arquivos gerados:")
    print("  - NEO4J_IGNORED_ITEMS.json (itens que não puderam ser conectados)")
    print("  - NEO4J_IMPROVEMENTS_REPORT.json (relatório de melhorias)")
    print("  - docs/NEO4J_USEFUL_QUERIES.md (queries úteis)")
    print()
    print("Próximos passos:")
    print("  1. Acesse o Neo4j Browser: http://localhost:7474")
    print("  2. Use o MCP do Neo4j no Cursor para explorar o grafo")
    print("  3. Revise os relatórios gerados")
    print()
    print("Queries úteis para começar:")
    print("  MATCH (n) RETURN n LIMIT 50")
    print("  MATCH (a:Agent)-[r]->(b) RETURN a, r, b LIMIT 25")
    print("  MATCH (g:AgentGroup)-[:CONTAINS]->(a:Agent) RETURN g, a")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelado pelo usuário.")
        sys.exit(1)

