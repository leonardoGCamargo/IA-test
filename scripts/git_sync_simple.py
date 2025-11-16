"""
Script simples para sincronizar repositório Git/GitHub.
Usa apenas comandos Git diretamente para evitar dependências.
"""

import subprocess
import sys
from pathlib import Path

def run_git_command(command):
    """Executa comando Git."""
    try:
        result = subprocess.run(
            ["git"] + command,
            capture_output=True,
            text=True,
            check=False
        )
        return result.stdout.strip(), result.stderr.strip(), result.returncode == 0
    except Exception as e:
        print(f"❌ Erro ao executar comando Git: {e}")
        return "", str(e), False


def main():
    """Sincroniza o repositório com GitHub."""
    print("\n" + "="*70)
    print("🔄 SINCRONIZAÇÃO GIT/GITHUB")
    print("="*70)
    
    # Verifica status
    print("\n📊 Verificando status do repositório...")
    stdout, stderr, success = run_git_command(["status", "--short"])
    
    if not success:
        print(f"❌ Erro: {stderr}")
        return
    
    if not stdout:
        print("✅ Nada para commitar - repositório limpo!")
        return
    
    print("📝 Mudanças detectadas:")
    print(stdout)
    
    # Adiciona todas as mudanças
    print("\n📦 Adicionando todas as mudanças...")
    _, stderr, success = run_git_command(["add", "-A"])
    
    if not success:
        print(f"❌ Erro ao adicionar arquivos: {stderr}")
        return
    
    print("✅ Arquivos adicionados ao staging")
    
    # Cria commit
    print("\n💾 Criando commit...")
    commit_message = """🔄 Reorganização completa do projeto e integração Git/GitHub

✨ Novidades:
- Estrutura profissional organizada em pastas
- Agente Git/GitHub integrado ao Orchestrator
- Documentação técnica completa para engenheiros
- Renomeação para "MCP Orchestrator"
- Agentes reorganizados em src/agents/
- Aplicações organizadas em src/apps/
- Dockerfiles organizados em docker/
- Documentação Obsidian em pasta dedicada

📁 Nova Estrutura:
- src/agents/ - Todos os agentes principais (incluindo Git Integration)
- src/apps/ - Aplicações existentes
- scripts/ - Scripts utilitários (git_sync, rename_project, etc)
- docs/ - Documentação técnica completa
- Obsidian_guardar aqui/ - Documentação Obsidian
- docker/ - Dockerfiles
- examples/ - Exemplos
- config/ - Configurações

🔧 Melhorias:
- Imports corrigidos para nova estrutura
- Docker Compose atualizado com novos caminhos
- README principal atualizado com nome comercial
- Documentação para engenheiros criada
- Git Agent totalmente integrado ao Orchestrator

🤖 Novo Agente:
- Git Integration Agent - Gerencia Git e GitHub automaticamente
"""
    
    _, stderr, success = run_git_command(["commit", "-m", commit_message.strip()])
    
    if not success:
        if "nothing to commit" in stderr.lower():
            print("✅ Nada para commitar")
        else:
            print(f"❌ Erro ao criar commit: {stderr}")
            return
    else:
        print("✅ Commit criado com sucesso")
    
    # Verifica branch atual
    stdout, _, _ = run_git_command(["branch", "--show-current"])
    branch = stdout.strip() if stdout else "main"
    print(f"\n🌿 Branch atual: {branch}")
    
    # Push para GitHub
    print(f"\n🚀 Fazendo push para GitHub (origin/{branch})...")
    _, stderr, success = run_git_command(["push", "origin", branch])
    
    if not success:
        print(f"❌ Erro ao fazer push: {stderr}")
        print("\n💡 Dica: Verifique suas credenciais do GitHub")
        return
    
    print("✅ Push realizado com sucesso!")
    
    # Verifica remotes
    print("\n🔗 Remotes configurados:")
    stdout, _, _ = run_git_command(["remote", "-v"])
    if stdout:
        print(stdout)
    
    print("\n" + "="*70)
    print("✅ SINCRONIZAÇÃO CONCLUÍDA COM SUCESSO!")
    print("="*70)
    
    # Extrai URL do GitHub
    if stdout:
        for line in stdout.split('\n'):
            if 'origin' in line and 'github.com' in line:
                url = line.split()[1]
                if url.startswith('http'):
                    repo_url = url.replace('.git', '')
                    print(f"\n📝 Verifique em: {repo_url}")


if __name__ == "__main__":
    main()

