# -*- coding: utf-8 -*-
"""
Script para preparar documentos do Obsidian para NotebookLM
Organiza e exporta documentos de forma otimizada para o NotebookLM
"""

import os
import shutil
from pathlib import Path
from typing import List, Dict
import json

project_root = Path(__file__).parent.parent
obsidian_path = project_root / "Obsidian_guardar aqui"

def criar_estrutura_notebooklm():
    """Cria estrutura otimizada para NotebookLM."""
    
    # Pasta para NotebookLM (pode ser linkada ao Drive)
    notebooklm_path = project_root / "NotebookLM"
    notebooklm_path.mkdir(exist_ok=True)
    
    # Subpastas organizadas
    pastas = {
        "01-Fundamentos": "Documentos fundamentais e conceitos base",
        "02-LangChain-LangGraph": "Guias completos de LangChain e LangGraph",
        "03-Agentes": "Documentação dos agentes",
        "04-Configuracao": "Guias de configuração e setup",
        "05-Exemplos": "Exemplos práticos e casos de uso",
        "06-Referencias": "Referências e links externos"
    }
    
    for pasta, descricao in pastas.items():
        pasta_path = notebooklm_path / pasta
        pasta_path.mkdir(exist_ok=True)
        
        # Cria README na pasta
        readme = pasta_path / "README.md"
        if not readme.exists():
            with open(readme, 'w', encoding='utf-8') as f:
                f.write(f"# {pasta}\n\n{descricao}\n")
    
    return notebooklm_path

def organizar_documentos():
    """Organiza documentos do Obsidian para NotebookLM."""
    
    notebooklm_path = criar_estrutura_notebooklm()
    
    # Mapeamento de documentos para pastas
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
    
    copiados = 0
    
    for pasta_destino, arquivos in mapeamento.items():
        destino = notebooklm_path / pasta_destino
        
        for arquivo_nome in arquivos:
            origem = obsidian_path / arquivo_nome
            
            if origem.exists():
                # Copia arquivo
                destino_arquivo = destino / origem.name
                shutil.copy2(origem, destino_arquivo)
                copiados += 1
                print(f"Copiado: {arquivo_nome} -> {pasta_destino}/")
            else:
                print(f"Nao encontrado: {arquivo_nome}")
    
    return copiados

def criar_indice_principal():
    """Cria índice principal para NotebookLM."""
    
    notebooklm_path = project_root / "NotebookLM"
    indice_path = notebooklm_path / "INDICE-PRINCIPAL.md"
    
    conteudo = """# 📚 Índice Principal - Projeto IA-TEST

> **Documentação Completa para NotebookLM**  
> Última atualização: 2025-01-27

---

## 📋 Estrutura de Documentos

### 01-Fundamentos
Documentos fundamentais do projeto:
- PROJETO-IA-TEST.md - Visão geral completa
- 00-MAPA-DE-AGENTES.md - Mapa de todos os agentes
- ESTRUTURA-PROJETO.md - Estrutura do projeto
- 00-ERROS-E-CONFIGURACOES-PENDENTES.md - Troubleshooting

### 02-LangChain-LangGraph
Guias completos de LangChain e LangGraph:
- LANGCHAIN-LANGGRAPH-GUIA.md - Guia principal
- LANGCHAIN-FUNDAMENTOS.md - Fundamentos do LangChain
- LANGGRAPH-CONCEITOS.md - Conceitos do LangGraph
- LANGGRAPH-WORKFLOWS.md - Criando workflows
- LANGCHAIN-NEO4J.md - Integração com Neo4j
- LANGGRAPH-PADROES.md - Padrões e melhores práticas
- LANGGRAPH-AGENTES.md - Criando agentes
- LANGCHAIN-EXEMPLOS.md - Exemplos práticos

### 03-Agentes
Documentação de cada agente:
- Orchestrator.md - Coordenador central
- System-Health.md - Diagnóstico e monitoramento
- DB-Manager.md - Gerenciamento de bancos
- MCP-Manager.md - Gerenciamento MCP
- Neo4j-GraphRAG.md - GraphRAG com Neo4j
- Obsidian-Integration.md - Integração Obsidian
- Kestra-Agent.md - Orquestração Kestra
- Docker-Integration.md - Integração Docker
- Git-Integration.md - Integração Git

### 04-Configuracao
Guias de configuração:
- CONFIGURACOES-APLICADAS.md - Configurações atuais
- NEO4J-CONFIGURADO.md - Setup Neo4j
- COMO-CONFIGURAR-NEO4J-URI.md - Guia de configuração
- ANALISE-BANCOS-DADOS.md - Análise de bancos

### 05-Exemplos
Exemplos e casos de uso:
- VIDEOS_MCP_AGENTES.md - Vídeos analisados
- OTIMIZACAO_AGENTES.md - Otimizações realizadas

### 06-Referencias
Referências e links:
- README_ESTRUTURA.md - Estrutura do projeto
- RESUMO-MAPA-AGENTES.md - Resumo dos agentes

---

## 🎯 Como Usar no NotebookLM

1. **Conecte esta pasta ao NotebookLM**
   - No NotebookLM, adicione esta pasta do Google Drive
   - O NotebookLM vai indexar todos os documentos

2. **Faça perguntas sobre:**
   - LangChain e LangGraph
   - Agentes do projeto
   - Configurações
   - Exemplos práticos

3. **Explore por tópicos:**
   - "Como funciona o Orchestrator?"
   - "Como criar um workflow com LangGraph?"
   - "Como integrar Neo4j com LangChain?"
   - "Quais são os padrões de LangGraph?"

---

## 🔗 Links Importantes

- **Projeto Principal:** PROJETO-IA-TEST.md
- **Guia LangChain:** 02-LangChain-LangGraph/LANGCHAIN-LANGGRAPH-GUIA.md
- **Mapa de Agentes:** 01-Fundamentos/00-MAPA-DE-AGENTES.md

---

**Preparado para NotebookLM** ✅
"""
    
    with open(indice_path, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    
    print(f"Criado: INDICE-PRINCIPAL.md")

def criar_readme_notebooklm():
    """Cria README explicando a estrutura."""
    
    notebooklm_path = project_root / "NotebookLM"
    readme_path = notebooklm_path / "README.md"
    
    conteudo = """# 📚 Documentação para NotebookLM

Esta pasta contém toda a documentação do projeto organizada para uso no **Google NotebookLM**.

## 📁 Estrutura

- **01-Fundamentos/** - Documentos base do projeto
- **02-LangChain-LangGraph/** - Guias completos de LangChain
- **03-Agentes/** - Documentação de cada agente
- **04-Configuracao/** - Guias de configuração
- **05-Exemplos/** - Exemplos práticos
- **06-Referencias/** - Referências e links

## 🚀 Como Usar

1. **Sincronize esta pasta no Google Drive**
   - Certifique-se de que está sincronizada

2. **No NotebookLM:**
   - Adicione esta pasta como fonte
   - O NotebookLM vai indexar todos os documentos

3. **Faça perguntas:**
   - Sobre LangChain e LangGraph
   - Sobre os agentes do projeto
   - Sobre configurações
   - Sobre exemplos práticos

## 📖 Índice

Veja **INDICE-PRINCIPAL.md** para lista completa de documentos.

---

**Última atualização:** 2025-01-27
"""
    
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    
    print(f"Criado: README.md")

def main():
    """Função principal."""
    print("=" * 70)
    print("PREPARANDO DOCUMENTOS PARA NOTEBOOKLM")
    print("=" * 70)
    print()
    
    print("1. Criando estrutura de pastas...")
    notebooklm_path = criar_estrutura_notebooklm()
    print(f"   Pasta criada: {notebooklm_path}")
    print()
    
    print("2. Organizando documentos...")
    copiados = organizar_documentos()
    print(f"   Total copiados: {copiados}")
    print()
    
    print("3. Criando índices...")
    criar_indice_principal()
    criar_readme_notebooklm()
    print()
    
    print("=" * 70)
    print("PREPARACAO CONCLUIDA!")
    print("=" * 70)
    print()
    print("Proximos passos:")
    print("1. Sincronize a pasta 'NotebookLM' no Google Drive")
    print("2. No NotebookLM, adicione esta pasta como fonte")
    print("3. Comece a fazer perguntas sobre o projeto!")
    print()
    print(f"Pasta criada em: {notebooklm_path}")

if __name__ == "__main__":
    main()

