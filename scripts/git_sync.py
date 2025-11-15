"""
Script para sincronizar repositório Git/GitHub com todas as mudanças.

Este script:
1. Verifica o status do Git
2. Adiciona todas as mudanças
3. Cria commit
4. Faz push para GitHub
5. Opcionalmente renomeia o repositório
"""

import sys
import os
from pathlib import Path

# Adiciona o diretório raiz ao path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from src.agents.git_integration import get_git_agent
from src.agents.orchestrator import get_orchestrator, AgentType
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Sincroniza o repositório com GitHub."""
    print("\n" + "="*70)
    print("🔄 SINCRONIZAÇÃO GIT/GITHUB")
    print("="*70)
    
    # Inicializa Git Agent
    try:
        git_agent = get_git_agent()
        print("✅ Git Agent inicializado")
    except Exception as e:
        print(f"❌ Erro ao inicializar Git Agent: {e}")
        return
    
    # Verifica status
    print("\n📊 Verificando status do repositório...")
    status = git_agent.get_status()
    print(f"Branch: {status.branch}")
    print(f"Limpo: {'Sim' if status.is_clean else 'Não'}")
    print(f"Arquivos não rastreados: {len(status.untracked_files)}")
    print(f"Arquivos modificados: {len(status.modified_files)}")
    print(f"Arquivos deletados: {len(status.deleted_files)}")
    print(f"Arquivos em staging: {len(status.staged_files)}")
    print(f"Ahead: {status.ahead}, Behind: {status.behind}")
    
    if status.is_clean:
        print("\n✅ Nada para commitar!")
        return
    
    # Adiciona todas as mudanças
    print("\n📦 Adicionando todas as mudanças...")
    if git_agent.add_files(all_files=True):
        print("✅ Arquivos adicionados ao staging")
    else:
        print("❌ Erro ao adicionar arquivos")
        return
    
    # Cria commit
    print("\n💾 Criando commit...")
    commit_message = """
🔄 Reorganização completa do projeto

✨ Novidades:
- Estrutura profissional organizada em pastas
- Agente Git/GitHub integrado
- Documentação técnica completa
- Agentes reorganizados em src/agents/
- Aplicações organizadas em src/apps/
- Dockerfiles organizados em docker/
- Documentação Obsidian em pasta dedicada

📁 Nova Estrutura:
- src/agents/ - Todos os agentes principais
- src/apps/ - Aplicações existentes
- scripts/ - Scripts utilitários
- docs/ - Documentação técnica
- Obsidian_guardar aqui/ - Documentação Obsidian
- docker/ - Dockerfiles
- examples/ - Exemplos
- config/ - Configurações

🔧 Melhorias:
- Imports corrigidos para nova estrutura
- Docker Compose atualizado
- README principal atualizado
- Documentação para engenheiros criada
"""
    
    if git_agent.commit(commit_message.strip()):
        print("✅ Commit criado com sucesso")
    else:
        print("❌ Erro ao criar commit")
        return
    
    # Push para GitHub
    print("\n🚀 Fazendo push para GitHub...")
    if git_agent.push(remote="origin", force=False):
        print("✅ Push realizado com sucesso!")
    else:
        print("❌ Erro ao fazer push")
        return
    
    # Verifica remotes
    print("\n🔗 Remotes configurados:")
    remotes = git_agent.get_remotes()
    for name, url in remotes.items():
        print(f"  {name}: {url}")
    
    print("\n" + "="*70)
    print("✅ SINCRONIZAÇÃO CONCLUÍDA COM SUCESSO!")
    print("="*70)
    print(f"\n📝 Verifique em: {remotes.get('origin', 'N/A')}")


if __name__ == "__main__":
    main()

