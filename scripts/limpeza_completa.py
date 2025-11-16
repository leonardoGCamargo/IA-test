# -*- coding: utf-8 -*-
"""
Script para executar limpeza completa do sistema
"""

import os
import shutil
from pathlib import Path
import json

project_root = Path(__file__).parent.parent

def arquivar_kestra_master():
    """Arquiva kestra_langchain_master.py (redundante)."""
    arquivo = project_root / "src" / "agents" / "kestra_langchain_master.py"
    backup_dir = project_root / "backups" / "agents"
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    if arquivo.exists():
        destino = backup_dir / "kestra_langchain_master.py"
        shutil.move(str(arquivo), str(destino))
        print(f"  [OK] Arquivado: kestra_langchain_master.py -> backups/agents/")
        return True
    return False

def atualizar_run_dashboard():
    """Atualiza run_dashboard.py para usar dashboard principal."""
    arquivo = project_root / "scripts" / "run_dashboard.py"
    
    if arquivo.exists():
        conteudo = arquivo.read_text(encoding='utf-8')
        # Substitui agent_dashboard_ui.py por agent_dashboard.py
        novo_conteudo = conteudo.replace(
            "src/agents/agent_dashboard_ui.py",
            "src/apps/agent_dashboard.py"
        ).replace(
            "--server.port=8507",
            "--server.port=8508"
        )
        arquivo.write_text(novo_conteudo, encoding='utf-8')
        print(f"  [OK] Atualizado: run_dashboard.py")
        return True
    return False

def arquivar_agent_dashboard_ui():
    """Arquiva agent_dashboard_ui.py (redundante)."""
    arquivo = project_root / "src" / "agents" / "agent_dashboard_ui.py"
    backup_dir = project_root / "backups" / "agents"
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    if arquivo.exists():
        destino = backup_dir / "agent_dashboard_ui.py"
        shutil.move(str(arquivo), str(destino))
        print(f"  [OK] Arquivado: agent_dashboard_ui.py -> backups/agents/")
        return True
    return False

def consolidar_docs_dashboard():
    """Consolida documentação de dashboard."""
    docs_path = project_root / "docs"
    backup_dir = project_root / "backups" / "docs"
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    docs_dashboard = [
        "AGENT_DASHBOARD_README.md",
        "DASHBOARD_AGENTES.md",
        "DASHBOARD_MELHORIAS.md",
        "DASHBOARD_RESUMO.md",
        "DASHBOARD_SETUP.md"
    ]
    
    # Cria documento consolidado
    conteudo_consolidado = "# Dashboard de Agentes - Documentação Completa\n\n"
    conteudo_consolidado += "> **Documentação consolidada** - Última atualização: 2025-01-27\n\n"
    conteudo_consolidado += "---\n\n"
    
    for doc in docs_dashboard:
        doc_path = docs_path / doc
        if doc_path.exists():
            conteudo = doc_path.read_text(encoding='utf-8')
            conteudo_consolidado += f"## {doc}\n\n"
            conteudo_consolidado += conteudo
            conteudo_consolidado += "\n\n---\n\n"
            # Move para backup
            shutil.move(str(doc_path), str(backup_dir / doc))
    
    # Salva consolidado
    doc_consolidado = docs_path / "DASHBOARD_COMPLETO.md"
    doc_consolidado.write_text(conteudo_consolidado, encoding='utf-8')
    print(f"  [OK] Consolidado: {len(docs_dashboard)} docs -> DASHBOARD_COMPLETO.md")
    return len(docs_dashboard)

def consolidar_docs_organizacao():
    """Consolida documentação de organização."""
    docs_path = project_root / "docs"
    backup_dir = project_root / "backups" / "docs"
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    docs_org = [
        "ORGANIZACAO_COMPLETA.md",
        "ORGANIZACAO_FINAL.md",
        "ORGANIZACAO_FINALIZADA.md",
        "ORGANIZACAO_PROJETO.md",
        "RESUMO_ORGANIZACAO_FINAL.md"
    ]
    
    # Move para backup (já foram executadas)
    for doc in docs_org:
        doc_path = docs_path / doc
        if doc_path.exists():
            shutil.move(str(doc_path), str(backup_dir / doc))
    
    # Cria resumo final
    doc_resumo = docs_path / "ORGANIZACAO_RESUMO.md"
    doc_resumo.write_text(
        "# Organização do Projeto - Resumo\n\n"
        "> **Status:** Organização concluída em 2025-01-27\n\n"
        "A organização do projeto foi concluída. Detalhes históricos estão em `backups/docs/`.\n",
        encoding='utf-8'
    )
    print(f"  [OK] Consolidado: {len(docs_org)} docs -> ORGANIZACAO_RESUMO.md")
    return len(docs_org)

def consolidar_docs_mcp():
    """Consolida documentação MCP."""
    docs_path = project_root / "docs"
    backup_dir = project_root / "backups" / "docs"
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    docs_mcp = [
        "BROWSER_MCP_SETUP.md",
        "MCP_ARCHITECTURE.md",
        "MCP_BROWSER_CURSOR.md",
        "MCP_README.md"
    ]
    
    # Cria documento consolidado
    conteudo_consolidado = "# MCP (Model Context Protocol) - Documentação Completa\n\n"
    conteudo_consolidado += "> **Documentação consolidada** - Última atualização: 2025-01-27\n\n"
    conteudo_consolidado += "---\n\n"
    
    for doc in docs_mcp:
        doc_path = docs_path / doc
        if doc_path.exists():
            conteudo = doc_path.read_text(encoding='utf-8')
            conteudo_consolidado += f"## {doc}\n\n"
            conteudo_consolidado += conteudo
            conteudo_consolidado += "\n\n---\n\n"
            # Move para backup
            shutil.move(str(doc_path), str(backup_dir / doc))
    
    # Salva consolidado
    doc_consolidado = docs_path / "MCP_COMPLETO.md"
    doc_consolidado.write_text(conteudo_consolidado, encoding='utf-8')
    print(f"  [OK] Consolidado: {len(docs_mcp)} docs -> MCP_COMPLETO.md")
    return len(docs_mcp)

def consolidar_docker_compose():
    """Consolida docker-compose (mantém apenas a versão principal)."""
    config_path = project_root / "config"
    backup_dir = project_root / "backups" / "config"
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    # Mantém docker-compose.yml como principal
    # Move outras versões para backup
    versoes_backup = [
        "docker-compose.optimized.yml",
        "docker-compose.stacks.yml"
    ]
    
    for versao in versoes_backup:
        arquivo = config_path / versao
        if arquivo.exists():
            shutil.move(str(arquivo), str(backup_dir / versao))
            print(f"  [OK] Arquivado: {versao} -> backups/config/")
    
    return len(versoes_backup)

def atualizar_imports():
    """Atualiza imports após remoções."""
    # Remove referências a kestra_langchain_master em __init__.py se houver
    init_file = project_root / "src" / "agents" / "__init__.py"
    if init_file.exists():
        conteudo = init_file.read_text(encoding='utf-8')
        # Remove imports de kestra_langchain_master se existir
        linhas = conteudo.split('\n')
        novas_linhas = [l for l in linhas if 'kestra_langchain_master' not in l.lower()]
        init_file.write_text('\n'.join(novas_linhas), encoding='utf-8')
        print(f"  [OK] Atualizado: __init__.py (removidos imports obsoletos)")

def main():
    """Função principal."""
    print("=" * 70)
    print("LIMPEZA COMPLETA DO SISTEMA")
    print("=" * 70)
    print()
    
    resultados = {}
    
    # 1. Agentes
    print("1. LIMPANDO AGENTES:")
    resultados['agentes'] = {
        'kestra_master': arquivar_kestra_master(),
        'dashboard_ui': arquivar_agent_dashboard_ui(),
        'run_dashboard': atualizar_run_dashboard(),
    }
    print()
    
    # 2. Documentação
    print("2. CONSOLIDANDO DOCUMENTACAO:")
    resultados['docs'] = {
        'dashboard': consolidar_docs_dashboard(),
        'organizacao': consolidar_docs_organizacao(),
        'mcp': consolidar_docs_mcp(),
    }
    print()
    
    # 3. Docker Compose
    print("3. CONSOLIDANDO DOCKER COMPOSE:")
    resultados['docker'] = consolidar_docker_compose()
    print()
    
    # 4. Imports
    print("4. ATUALIZANDO IMPORTS:")
    atualizar_imports()
    print()
    
    # Resumo
    print("=" * 70)
    print("LIMPEZA CONCLUIDA!")
    print("=" * 70)
    print()
    print("Resumo:")
    print(f"  - Agentes arquivados: 2")
    print(f"  - Docs consolidados: {sum(resultados['docs'].values())}")
    print(f"  - Docker compose consolidado: {resultados['docker']} versoes -> 1")
    print()
    print("Arquivos movidos para backups/")
    print()
    
    # Salva relatório
    relatorio_file = project_root / "Obsidian_guardar aqui" / "LIMPEZA-EXECUTADA.json"
    with open(relatorio_file, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)
    
    print(f"Relatorio salvo em: {relatorio_file}")

if __name__ == "__main__":
    main()

