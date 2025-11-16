"""
Script para sincronizar documentação com Obsidian.
Detecta automaticamente o vault ou permite configurar.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from src.agents.mcp_obsidian_integration import ObsidianManager

# Carrega o arquivo .env específico
env_file = "e15fdb03f6467054904bd1a6eee67b8b6839bbbc4d2e4ec3419781663c81fd57.env"
if os.path.exists(env_file):
    load_dotenv(env_file)
    print(f"✅ Arquivo .env carregado: {env_file}")
else:
    load_dotenv()
    print("⚠️ Usando .env padrão")

def detect_obsidian_vault() -> Path:
    """Detecta o vault do Obsidian em locais comuns."""
    home = Path.home()
    username = os.getenv("USERNAME", os.getenv("USER", ""))
    
    # Locais comuns do Obsidian no Windows
    common_locations = [
        home / "Documents" / "Obsidian",
        home / "Obsidian",
        home / "AppData" / "Roaming" / "Obsidian",
        Path(f"C:/Users/{username}/Documents/Obsidian"),
        Path(f"C:/Users/{username}/Obsidian"),
    ]
    
    # Primeiro, verifica se há OBSIDIAN_VAULT_PATH no .env
    vault_path = os.getenv("OBSIDIAN_VAULT_PATH")
    if vault_path:
        path = Path(vault_path)
        if path.exists():
            return path
    
    # Procura em locais comuns
    for location in common_locations:
        if location.exists():
            # Procura por vaults (diretórios com .obsidian)
            try:
                for item in location.iterdir():
                    if item.is_dir():
                        obsidian_config = item / ".obsidian"
                        if obsidian_config.exists():
                            return item
            except (PermissionError, OSError):
                continue
    
    return None

def read_md_file(filepath: str) -> str:
    """Lê conteúdo de arquivo markdown."""
    try:
        file_path = Path(filepath)
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        return ""
    except Exception as e:
        return ""

def main():
    print("\n" + "="*70)
    print("📝 SINCRONIZAÇÃO DE DOCUMENTAÇÃO COM OBSIDIAN")
    print("="*70)
    
    # Tenta obter caminho via argumento ou detectar
    vault_path = None
    
    if len(sys.argv) > 1:
        vault_path = Path(sys.argv[1])
        print(f"✅ Caminho fornecido via argumento: {vault_path}")
    else:
        vault_path = detect_obsidian_vault()
        if vault_path:
            print(f"✅ Vault detectado automaticamente: {vault_path}")
    
    # Se ainda não encontrou, tenta variável de ambiente
    if not vault_path:
        env_vault = os.getenv("OBSIDIAN_VAULT_PATH")
        if env_vault:
            vault_path = Path(env_vault)
            print(f"✅ Vault encontrado no .env: {vault_path}")
    
    # Se ainda não encontrou, pede ao usuário
    if not vault_path or not vault_path.exists():
        print("\n❌ Vault do Obsidian não encontrado automaticamente.")
        print("\nOpções:")
        print("1. Execute com o caminho como argumento:")
        print("   python sync_obsidian_docs.py \"C:\\Users\\Usuario\\Documents\\Obsidian\\MeuVault\"")
        print("\n2. Configure OBSIDIAN_VAULT_PATH no arquivo .env")
        print("\n3. Ou informe o caminho agora:")
        
        try:
            user_input = input("\nCaminho do vault (ou Enter para cancelar): ").strip().strip('"')
            if user_input:
                vault_path = Path(user_input)
            else:
                print("❌ Operação cancelada.")
                return
        except KeyboardInterrupt:
            print("\n❌ Operação cancelada.")
            return
    
    # Verifica se o vault existe
    if not vault_path.exists():
        print(f"❌ Caminho não existe: {vault_path}")
        return
    
    # Verifica se é um vault (tem .obsidian)
    if not (vault_path / ".obsidian").exists():
        print(f"⚠️ Aviso: {vault_path} não parece ser um vault Obsidian (.obsidian não encontrado)")
        print("Continuando mesmo assim...\n")
    
    # Inicializa Obsidian Manager
    obsidian = ObsidianManager()
    if obsidian.set_vault_path(str(vault_path)):
        print(f"✅ Vault configurado: {vault_path}\n")
    else:
        print(f"❌ Erro ao configurar vault: {vault_path}")
        return
    
    # Lista de arquivos para criar
    files_to_create = [
        # Arquivos principais (raiz)
        ("00-MAPA-DE-AGENTES.md", ""),
        ("01-Guia-Obsidian.md", ""),
        ("02-Guia-Cursor.md", ""),
        ("03-Manual-Sistema-Agentes.md", ""),
        ("04-Como-Criar-Agentes.md", ""),
        ("RESUMO-MAPA-AGENTES.md", ""),
        
        # Documentação dos agentes (pasta Agentes)
        ("Agentes/Orchestrator.md", "Agentes"),
        ("Agentes/Master-Agent.md", "Agentes"),
        ("Agentes/Helper-System.md", "Agentes"),
        ("Agentes/MCP-Manager.md", "Agentes"),
        ("Agentes/Docker-Integration.md", "Agentes"),
        ("Agentes/Neo4j-GraphRAG.md", "Agentes"),
        ("Agentes/Obsidian-Integration.md", "Agentes"),
        ("Agentes/Kestra-Agent.md", "Agentes"),
    ]
    
    print("📝 Criando/atualizando notas...\n")
    
    created_count = 0
    updated_count = 0
    skipped_count = 0
    failed_count = 0
    
    for filepath, folder in files_to_create:
        # Lê o conteúdo
        content = read_md_file(filepath)
        
        if not content:
            skipped_count += 1
            continue
        
        # Extrai título
        title = Path(filepath).stem
        
        try:
            # Determina caminho do arquivo no vault
            target_folder = vault_path / folder if folder else vault_path
            target_folder.mkdir(parents=True, exist_ok=True)
            target_file = target_folder / f"{title}.md"
            
            # Verifica se já existe
            file_exists = target_file.exists()
            
            # Escreve/atualiza arquivo
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            if file_exists:
                print(f"🔄 Atualizado: {folder}/{title}.md" if folder else f"🔄 Atualizado: {title}.md")
                updated_count += 1
            else:
                print(f"✅ Criado: {folder}/{title}.md" if folder else f"✅ Criado: {title}.md")
                created_count += 1
                
        except Exception as e:
            print(f"❌ Erro ao processar {title}: {e}")
            failed_count += 1
    
    print("\n" + "="*70)
    print(f"✅ {created_count} notas criadas")
    print(f"🔄 {updated_count} notas atualizadas")
    if skipped_count > 0:
        print(f"⚠️ {skipped_count} arquivos não encontrados (normal se não existirem)")
    if failed_count > 0:
        print(f"❌ {failed_count} erros")
    print("="*70)
    print(f"\n📁 Vault: {vault_path}")
    print("💡 Abra o Obsidian e navegue para ver as notas!")
    print("\n💡 Dica: Configure OBSIDIAN_VAULT_PATH no .env para não precisar informar sempre:")
    print(f"   OBSIDIAN_VAULT_PATH={vault_path}")

if __name__ == "__main__":
    main()
