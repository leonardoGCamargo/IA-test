# -*- coding: utf-8 -*-
"""
Script para sincronizar documentos do Obsidian para NotebookLM
Mantém a pasta NotebookLM atualizada
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

project_root = Path(__file__).parent.parent
obsidian_path = project_root / "Obsidian_guardar aqui"
notebooklm_path = project_root / "NotebookLM"

def sincronizar_documento(origem: Path, destino: Path):
    """Sincroniza um documento se foi modificado."""
    if not origem.exists():
        return False
    
    # Verifica se precisa atualizar
    if not destino.exists():
        # Novo arquivo
        destino.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(origem, destino)
        return True
    
    # Compara datas de modificação
    origem_mtime = origem.stat().st_mtime
    destino_mtime = destino.stat().st_mtime
    
    if origem_mtime > destino_mtime:
        # Arquivo foi modificado
        shutil.copy2(origem, destino)
        return True
    
    return False

def sincronizar_pasta():
    """Sincroniza todos os documentos."""
    
    if not notebooklm_path.exists():
        print("Pasta NotebookLM nao existe. Execute preparar_para_notebooklm.py primeiro.")
        return
    
    print("=" * 70)
    print("SINCRONIZANDO PARA NOTEBOOKLM")
    print("=" * 70)
    print()
    
    # Mapeamento (mesmo do script de preparação)
    mapeamento = {
        "01-Fundamentos": [
            "PROJETO-IA-TEST.md",
            "00-MAPA-DE-AGENTES.md",
            "ESTRUTURA-PROJETO.md",
            "00-ERROS-E-CONFIGURACOES-PENDENTES.md",
        ],
        "02-LangChain-LangGraph": [
            "LANGCHAIN-LANGGRAPH-GUIA.md",
            "LANGCHAIN-FUNDAMENTOS.md",
            "LANGGRAPH-CONCEITOS.md",
            "LANGGRAPH-WORKFLOWS.md",
            "LANGCHAIN-NEO4J.md",
            "LANGGRAPH-PADROES.md",
            "LANGGRAPH-AGENTES.md",
            "LANGCHAIN-EXEMPLOS.md",
            "PREPARACAO-LANGCHAIN.md",
            "RESUMO-LANGCHAIN-PREPARACAO.md",
        ],
        "03-Agentes": [
            "Agentes/Orchestrator.md",
            "Agentes/System-Health.md",
            "Agentes/DB-Manager.md",
            "Agentes/MCP-Manager.md",
            "Agentes/Neo4j-GraphRAG.md",
            "Agentes/Obsidian-Integration.md",
            "Agentes/Kestra-Agent.md",
            "Agentes/Docker-Integration.md",
            "Agentes/Git-Integration.md",
        ],
        "04-Configuracao": [
            "CONFIGURACOES-APLICADAS.md",
            "NEO4J-CONFIGURADO.md",
            "COMO-CONFIGURAR-NEO4J-URI.md",
            "ANALISE-BANCOS-DADOS.md",
        ],
        "05-Exemplos": [
            "VIDEOS_MCP_AGENTES.md",
            "OTIMIZACAO_AGENTES.md",
        ],
        "06-Referencias": [
            "README_ESTRUTURA.md",
            "RESUMO-MAPA-AGENTES.md",
        ]
    }
    
    atualizados = 0
    novos = 0
    
    for pasta_destino, arquivos in mapeamento.items():
        destino_pasta = notebooklm_path / pasta_destino
        
        for arquivo_nome in arquivos:
            origem = obsidian_path / arquivo_nome
            destino = destino_pasta / origem.name
            
            if sincronizar_documento(origem, destino):
                if destino.exists() and destino.stat().st_mtime == origem.stat().st_mtime:
                    novos += 1
                    print(f"Novo: {arquivo_nome}")
                else:
                    atualizados += 1
                    print(f"Atualizado: {arquivo_nome}")
    
    print()
    print(f"Total: {novos} novos, {atualizados} atualizados")
    print()
    print("Sincronizacao concluida!")
    print()
    print("Proximo passo:")
    print("  - Se a pasta esta no Google Drive, aguarde sincronizacao")
    print("  - O NotebookLM vai re-indexar automaticamente")

if __name__ == "__main__":
    sincronizar_pasta()

