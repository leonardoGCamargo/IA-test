"""
Script para renomear o projeto com nome comercial.

Nome sugerido: "MCP Orchestrator" ou "OrchestrAI Platform"
"""

import sys
from pathlib import Path
import re

# Nome comercial sugerido
PROJECT_NAME = "MCP Orchestrator"
PROJECT_DESCRIPTION = "Plataforma profissional de orquestração de agentes MCP"
PROJECT_SHORT_NAME = "mcp-orchestrator"

root_dir = Path(__file__).parent.parent


def update_file_content(file_path: Path, old_name: str, new_name: str):
    """Atualiza conteúdo de um arquivo."""
    try:
        if not file_path.exists():
            return False
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        updated_content = content.replace(old_name, new_name)
        
        if content != updated_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            return True
        return False
    except Exception as e:
        print(f"⚠️  Erro ao atualizar {file_path}: {e}")
        return False


def main():
    """Renomeia o projeto."""
    print("\n" + "="*70)
    print("📝 RENOMEAÇÃO DO PROJETO")
    print("="*70)
    print(f"\nNome sugerido: {PROJECT_NAME}")
    print(f"Descrição: {PROJECT_DESCRIPTION}")
    print(f"Nome curto: {PROJECT_SHORT_NAME}")
    
    response = input("\nDeseja usar este nome? (s/n): ").strip().lower()
    
    if response != 's':
        project_name = input("Digite o nome do projeto: ").strip()
        project_short = input("Digite o nome curto (para URLs): ").strip()
        project_desc = input("Digite a descrição: ").strip()
    else:
        project_name = PROJECT_NAME
        project_short = PROJECT_SHORT_NAME
        project_desc = PROJECT_DESCRIPTION
    
    print(f"\n🔄 Renomeando para: {project_name}")
    
    # Arquivos para atualizar
    files_to_update = [
        ("README.md", "Sistema de Agentes MCP - Orchestrator", project_name),
        ("README.md", "Sistema modular de agentes", project_desc),
        ("README.md", "IA-test", project_short),
        ("readme.md", "Sistema de Agentes MCP - Orchestrator", project_name),
        ("docs/README.md", "Sistema de Agentes MCP", project_name),
        ("docs/ORGANIZACAO_PROJETO.md", "Sistema de Agentes MCP", project_name),
    ]
    
    updated = 0
    for file_path_str, old_text, new_text in files_to_update:
        file_path = root_dir / file_path_str
        if update_file_content(file_path, old_text, new_text):
            print(f"✅ Atualizado: {file_path_str}")
            updated += 1
        else:
            print(f"⏭️  Sem mudanças: {file_path_str}")
    
    print("\n" + "="*70)
    print(f"✅ {updated} arquivos atualizados")
    print("="*70)
    print("\n💡 Próximo passo: Execute 'python scripts/git_sync.py' para sincronizar!")


if __name__ == "__main__":
    main()

