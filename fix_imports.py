"""
Script para corrigir imports após reorganização dos arquivos.
"""

import re
from pathlib import Path

def fix_imports_in_file(filepath: Path):
    """Corrige imports em um arquivo."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Mapeamento de imports antigos para novos
        import_mappings = {
            # Agents
            r'^from mcp_manager import': 'from src.agents.mcp_manager import',
            r'^from mcp_docker_integration import': 'from src.agents.mcp_docker_integration import',
            r'^from mcp_neo4j_integration import': 'from src.agents.mcp_neo4j_integration import',
            r'^from mcp_obsidian_integration import': 'from src.agents.mcp_obsidian_integration import',
            r'^from mcp_kestra_integration import': 'from src.agents.mcp_kestra_integration import',
            r'^from kestra_langchain_master import': 'from src.agents.kestra_langchain_master import',
            r'^from agent_helper_system import': 'from src.agents.agent_helper_system import',
            r'^from orchestrator import': 'from src.agents.orchestrator import',
            
            # Apps
            r'^from chains import': 'from src.apps.chains import',
            r'^from utils import': 'from src.apps.utils import',
            
            # Relative imports dentro de src/
            r'^from \.mcp_manager import': 'from .mcp_manager import',
            r'^from \.mcp_docker_integration import': 'from .mcp_docker_integration import',
            r'^from \.mcp_neo4j_integration import': 'from .mcp_neo4j_integration import',
            r'^from \.mcp_obsidian_integration import': 'from .mcp_obsidian_integration import',
            r'^from \.mcp_kestra_integration import': 'from .mcp_kestra_integration import',
            r'^from \.kestra_langchain_master import': 'from .kestra_langchain_master import',
            r'^from \.agent_helper_system import': 'from .agent_helper_system import',
            r'^from \.orchestrator import': 'from .orchestrator import',
        }
        
        # Aplica substituições
        for pattern, replacement in import_mappings.items():
            content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
        
        # Se mudou, salva
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Corrigido: {filepath}")
            return True
        else:
            print(f"⏭️  Sem mudanças: {filepath}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao corrigir {filepath}: {e}")
        return False

def main():
    """Corrige imports em todos os arquivos Python."""
    print("\n" + "="*70)
    print("🔧 CORRIGINDO IMPORTS APÓS REORGANIZAÇÃO")
    print("="*70)
    
    # Arquivos para corrigir
    files_to_fix = [
        # Agents
        "src/agents/orchestrator.py",
        "src/agents/kestra_langchain_master.py",
        "src/agents/agent_helper_system.py",
        "src/agents/mcp_manager.py",
        "src/agents/mcp_manager_ui.py",
        "src/agents/mcp_docker_integration.py",
        "src/agents/mcp_neo4j_integration.py",
        "src/agents/mcp_obsidian_integration.py",
        "src/agents/mcp_kestra_integration.py",
        
        # Apps (podem importar de agents)
        "src/apps/bot.py",
        "src/apps/loader.py",
        "src/apps/pdf_bot.py",
        "src/apps/api.py",
        "src/apps/chains.py",
        "src/apps/utils.py",
        
        # Scripts
        "scripts/master_demo.py",
        "scripts/sync_obsidian_docs.py",
        "scripts/verificar_integracao_obsidian.py",
    ]
    
    fixed = 0
    skipped = 0
    
    for filepath_str in files_to_fix:
        filepath = Path(filepath_str)
        if filepath.exists():
            if fix_imports_in_file(filepath):
                fixed += 1
            else:
                skipped += 1
        else:
            print(f"⚠️  Arquivo não encontrado: {filepath}")
            skipped += 1
    
    print("\n" + "="*70)
    print(f"✅ {fixed} arquivos corrigidos")
    print(f"⏭️  {skipped} arquivos sem mudanças ou não encontrados")
    print("="*70)
    print("\n💡 Verifique se os imports estão corretos e teste o sistema!")

if __name__ == "__main__":
    main()

