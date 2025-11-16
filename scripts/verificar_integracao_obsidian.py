"""
Script para verificar se a integração Obsidian está funcionando corretamente.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from src.agents.mcp_obsidian_integration import ObsidianManager

# Carrega .env
env_file = "e15fdb03f6467054904bd1a6eee67b8b6839bbbc4d2e4ec3419781663c81fd57.env"
if os.path.exists(env_file):
    load_dotenv(env_file)
else:
    load_dotenv()

print("\n" + "="*70)
print("🔍 VERIFICAÇÃO DA INTEGRAÇÃO OBSIDIAN")
print("="*70)

# Inicializa Obsidian Manager
obsidian = ObsidianManager()

# Verifica configuração do vault
vault_path = os.getenv("OBSIDIAN_VAULT_PATH")
if vault_path:
    obsidian.set_vault_path(vault_path)
    print(f"✅ Vault configurado via .env: {vault_path}")
elif obsidian.vault_path:
    print(f"✅ Vault detectado automaticamente: {obsidian.vault_path}")
else:
    print("⚠️ Vault não configurado")
    print("\nPara configurar, adicione no .env:")
    print("OBSIDIAN_VAULT_PATH=C:\\caminho\\para\\seu\\vault")

if obsidian.vault_path:
    vault = Path(obsidian.vault_path)
    
    print(f"\n📁 Vault: {vault}")
    
    # Verifica se é um vault válido
    if (vault / ".obsidian").exists():
        print("✅ É um vault Obsidian válido (.obsidian encontrado)")
    else:
        print("⚠️ Aviso: Pasta .obsidian não encontrada (pode ser normal)")
    
    # Verifica permissões
    try:
        test_file = vault / ".test_write"
        test_file.write_text("test")
        test_file.unlink()
        print("✅ Permissão de escrita: OK")
    except Exception as e:
        print(f"❌ Erro de permissão: {e}")
    
    # Testa criação de nota
    print("\n🧪 Testando criação de nota...")
    test_note = obsidian.create_note(
        "Teste-Integracao-MCP",
        """# Teste de Integração MCP

> **Criado em:** $(date)

Esta é uma nota de teste para verificar se a integração MCP → Obsidian está funcionando.

## Status

✅ Integração funcionando!
✅ Não requer plano pago do Obsidian
✅ Funciona diretamente com arquivos .md

## Como funciona

A integração MCP trabalha diretamente com os arquivos `.md` no vault do Obsidian, sem precisar de:
- Plano pago do Obsidian
- Obsidian Sync
- APIs oficiais do Obsidian

## Próximos Passos

1. Verificar se esta nota apareceu no Obsidian
2. Se apareceu, a integração está funcionando! 🎉
3. Pode deletar esta nota de teste

## Tags

#teste #mcp #integração
""",
        folder="Testes"
    )
    
    if test_note:
        print(f"✅ Nota de teste criada: {test_note.name}")
        print(f"   Localização: {test_note.parent}")
        print("\n💡 Abra o Obsidian e verifique se a nota apareceu!")
        print("   Se apareceu, a integração está funcionando perfeitamente!")
        
        # Conta notas existentes
        all_notes = obsidian.list_notes()
        print(f"\n📊 Total de notas no vault: {len(all_notes)}")
        
        # Verifica notas de documentação
        doc_notes = obsidian.list_notes("")
        doc_count = len([n for n in doc_notes if "MAPA" in n.name or "Guia" in n.name])
        if doc_count > 0:
            print(f"📚 Notas de documentação encontradas: {doc_count}")
        
        agent_notes = obsidian.list_notes("Agentes")
        if agent_notes:
            print(f"🤖 Notas de agentes encontradas: {len(agent_notes)}")
        
    else:
        print("❌ Erro ao criar nota de teste")
    
    print("\n" + "="*70)
    print("✅ VERIFICAÇÃO CONCLUÍDA")
    print("="*70)
    print("\n💡 Resumo:")
    print("   - Integração MCP funciona SEM plano pago do Obsidian")
    print("   - Trabalha diretamente com arquivos .md no vault")
    print("   - Não requer APIs ou assinaturas")
    print("   - Funciona 100% no plano gratuito do Obsidian!")

if __name__ == "__main__":
    pass

