"""
Script para sincronizar todos os dados do projeto para Neo4j Aura.

Uso:
    python scripts/sync_to_neo4j.py
"""

import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.agents.orchestrator import get_orchestrator

def sync_all():
    """Sincroniza tudo para Neo4j."""
    print("=" * 70)
    print("🔄 Sincronização para Neo4j Aura")
    print("=" * 70)
    print()
    
    try:
        orchestrator = get_orchestrator()
        
        # 1. Sincronizar MCPs
        print("📡 Sincronizando MCPs para Neo4j...")
        try:
            mcp_result = orchestrator.sync_mcp_to_neo4j()
            print(f"   ✅ {mcp_result.get('synced_count', 0)}/{mcp_result.get('total', 0)} MCPs sincronizados")
            if mcp_result.get('errors'):
                print(f"   ⚠️  {len(mcp_result['errors'])} erros encontrados")
        except Exception as e:
            print(f"   ❌ Erro ao sincronizar MCPs: {e}")
        
        print()
        
        # 2. Sincronizar Obsidian
        print("📝 Sincronizando Obsidian para Neo4j...")
        try:
            obsidian_result = orchestrator.sync_mcp_to_obsidian()
            print(f"   ✅ {obsidian_result.get('created_count', 0)} notas criadas")
            if obsidian_result.get('errors'):
                print(f"   ⚠️  {len(obsidian_result['errors'])} erros encontrados")
        except Exception as e:
            print(f"   ❌ Erro ao sincronizar Obsidian: {e}")
        
        print()
        print("=" * 70)
        print("✅ Sincronização completa!")
        print("=" * 70)
        print()
        print("💡 Dica: Conecte no Neo4j Desktop para visualizar os dados")
        print("   Veja: docs/NEO4J_AURA_SETUP.md")
        
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    sync_all()


