"""
Script para analisar uso dos bancos de dados e reorganizar arquivos.
Usa os agentes criados para ajudar na análise.
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Any
import json

# Adiciona o diretório raiz ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
load_dotenv()

def analisar_uso_bancos():
    """Analisa como os bancos de dados estão sendo usados."""
    print("=" * 70)
    print("ANALISE DE USO DOS BANCOS DE DADOS")
    print("=" * 70)
    print()
    
    uso = {
        "Neo4j": {
            "configurado": bool(os.getenv("NEO4J_URI")),
            "uso_principal": [],
            "arquivos": [],
            "via_mcp": False,
            "via_codigo": False
        },
        "Neon": {
            "configurado": bool(os.getenv("NEON_PROJECT_ID")),
            "uso_principal": [],
            "arquivos": [],
            "via_mcp": True,  # Você mencionou que configurou via MCP
            "via_codigo": False
        },
        "Supabase": {
            "configurado": bool(os.getenv("SUPABASE_URL")),
            "uso_principal": [],
            "arquivos": [],
            "via_mcp": True,  # Você mencionou que "subiu o MCP"
            "via_codigo": False
        },
        "MongoDB": {
            "configurado": bool(os.getenv("MONGODB_URI")),
            "uso_principal": [],
            "arquivos": [],
            "via_mcp": False,
            "via_codigo": False
        }
    }
    
    # Analisa arquivos
    src_path = project_root / "src"
    
    # Neo4j
    neo4j_files = list(src_path.rglob("*neo4j*.py"))
    if neo4j_files:
        uso["Neo4j"]["via_codigo"] = True
        uso["Neo4j"]["arquivos"] = [str(f.relative_to(project_root)) for f in neo4j_files[:5]]
        uso["Neo4j"]["uso_principal"] = [
            "GraphRAG (mcp_neo4j_integration.py)",
            "Armazenamento de conhecimento",
            "Sincronização de MCPs e Obsidian"
        ]
    
    # Neon
    neon_files = list(src_path.rglob("*neon*.py"))
    if neon_files:
        uso["Neon"]["via_codigo"] = True
        uso["Neon"]["arquivos"] = [str(f.relative_to(project_root)) for f in neon_files[:5]]
    
    # Verifica db_manager
    db_manager_file = src_path / "agents" / "db_manager.py"
    if db_manager_file.exists():
        with open(db_manager_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if "NEON" in content:
                uso["Neon"]["via_codigo"] = True
                uso["Neon"]["uso_principal"].append("DatabaseManager (db_manager.py)")
            if "SUPABASE" in content:
                uso["Supabase"]["via_codigo"] = True
                uso["Supabase"]["uso_principal"].append("DatabaseManager (db_manager.py)")
            if "MONGODB" in content:
                uso["MongoDB"]["via_codigo"] = True
                uso["MongoDB"]["uso_principal"].append("DatabaseManager (db_manager.py)")
    
    # Imprime resultados
    for db, info in uso.items():
        print(f"\n📊 {db}:")
        print(f"   Configurado: {'✅' if info['configurado'] else '❌'}")
        print(f"   Via MCP: {'✅' if info['via_mcp'] else '❌'}")
        print(f"   Via Código: {'✅' if info['via_codigo'] else '❌'}")
        if info['uso_principal']:
            print(f"   Uso Principal:")
            for uso_item in info['uso_principal']:
                print(f"      - {uso_item}")
        if info['arquivos']:
            print(f"   Arquivos: {len(info['arquivos'])} encontrados")
    
    return uso

def verificar_arquivos_duplicados():
    """Verifica se há arquivos duplicados ou mal organizados."""
    print("\n" + "=" * 70)
    print("VERIFICACAO DE ARQUIVOS DUPLICADOS/MAL ORGANIZADOS")
    print("=" * 70)
    print()
    
    problemas = []
    
    # Verifica estrutura duplicada IA-test/IA-test/
    ia_test_duplicado = project_root / "IA-test"
    if ia_test_duplicado.exists() and ia_test_duplicado.is_dir():
        problemas.append({
            "tipo": "Estrutura duplicada",
            "caminho": "IA-test/",
            "descricao": "Pasta 'IA-test' dentro do projeto pode ser duplicação",
            "acao": "Verificar se é necessário ou pode ser removida"
        })
    
    # Verifica arquivos na raiz que deveriam estar em src/
    arquivos_raiz_suspeitos = [
        "api.py", "bot.py", "chains.py", "loader.py", "pdf_bot.py"
    ]
    
    for arquivo in arquivos_raiz_suspeitos:
        arquivo_path = project_root / arquivo
        if arquivo_path.exists():
            src_arquivo = project_root / "src" / "apps" / arquivo
            if src_arquivo.exists():
                problemas.append({
                    "tipo": "Arquivo duplicado",
                    "caminho": arquivo,
                    "descricao": f"Arquivo existe na raiz E em src/apps/",
                    "acao": "Verificar qual é o correto e remover duplicata"
                })
            else:
                problemas.append({
                    "tipo": "Arquivo na raiz",
                    "caminho": arquivo,
                    "descricao": f"Arquivo na raiz, deveria estar em src/apps/",
                    "acao": "Mover para src/apps/"
                })
    
    # Verifica Obsidian duplicado
    obsidian_duplicado = project_root / "Obsidian_guardar aqui" / "Obsidian_guardar aqui"
    if obsidian_duplicado.exists():
        problemas.append({
            "tipo": "Pasta Obsidian duplicada",
            "caminho": "Obsidian_guardar aqui/Obsidian_guardar aqui/",
            "descricao": "Pasta Obsidian dentro de Obsidian",
            "acao": "Remover pasta interna duplicada"
        })
    
    if problemas:
        print("⚠️ Problemas encontrados:\n")
        for i, problema in enumerate(problemas, 1):
            print(f"{i}. {problema['tipo']}: {problema['caminho']}")
            print(f"   {problema['descricao']}")
            print(f"   Ação sugerida: {problema['acao']}")
            print()
    else:
        print("✅ Nenhum problema encontrado!")
    
    return problemas

def gerar_relatorio(uso: Dict, problemas: List):
    """Gera relatório completo."""
    relatorio = {
        "data": str(Path(__file__).stat().st_mtime),
        "uso_bancos": uso,
        "problemas_arquivos": problemas,
        "recomendacoes": []
    }
    
    # Recomendações
    if uso["Neon"]["via_mcp"] and not uso["Neon"]["via_codigo"]:
        relatorio["recomendacoes"].append({
            "tipo": "Neon",
            "mensagem": "Neon está configurado apenas via MCP. Se não usar no código, está OK.",
            "prioridade": "baixa"
        })
    
    if uso["Supabase"]["via_mcp"] and not uso["Supabase"]["via_codigo"]:
        relatorio["recomendacoes"].append({
            "tipo": "Supabase",
            "mensagem": "Supabase está configurado apenas via MCP. Se não usar no código, está OK.",
            "prioridade": "baixa"
        })
    
    if problemas:
        relatorio["recomendacoes"].append({
            "tipo": "Organização",
            "mensagem": f"Encontrados {len(problemas)} problemas de organização. Revisar e corrigir.",
            "prioridade": "media"
        })
    
    # Salva relatório
    relatorio_path = project_root / "Obsidian_guardar aqui" / "relatorio_analise.json"
    with open(relatorio_path, 'w', encoding='utf-8') as f:
        json.dump(relatorio, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 70)
    print("RELATORIO GERADO")
    print("=" * 70)
    print(f"Salvo em: {relatorio_path}")
    print()
    
    if relatorio["recomendacoes"]:
        print("📋 Recomendações:")
        for rec in relatorio["recomendacoes"]:
            print(f"   [{rec['prioridade'].upper()}] {rec['tipo']}: {rec['mensagem']}")
    
    return relatorio

def main():
    """Função principal."""
    print("\n🔍 Iniciando análise...\n")
    
    # 1. Analisa uso dos bancos
    uso = analisar_uso_bancos()
    
    # 2. Verifica arquivos duplicados
    problemas = verificar_arquivos_duplicados()
    
    # 3. Gera relatório
    relatorio = gerar_relatorio(uso, problemas)
    
    print("\n" + "=" * 70)
    print("✅ ANÁLISE CONCLUÍDA")
    print("=" * 70)
    print("\nPróximos passos:")
    print("1. Revisar o relatório gerado")
    print("2. Corrigir problemas de organização se necessário")
    print("3. Confirmar uso dos bancos de dados")

if __name__ == "__main__":
    main()

