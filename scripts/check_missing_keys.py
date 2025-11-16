"""
Script para verificar quais chaves e configurações estão faltando.

Uso:
    python scripts/check_missing_keys.py
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Dict, List, Tuple

# Carrega .env
project_root = Path(__file__).parent.parent
env_file = project_root / ".env"
if env_file.exists():
    load_dotenv(env_file)
else:
    load_dotenv()

def check_variable(var_name: str, description: str, required_for: List[str] = None) -> Tuple[bool, str]:
    """Verifica se uma variável está configurada."""
    value = os.getenv(var_name)
    
    if not value or value.strip() == "" or value.startswith("SUBSTITUA") or value == "password":
        return False, "❌ Não configurado"
    
    # Mascarar senhas e chaves
    if "PASSWORD" in var_name or "KEY" in var_name or "SECRET" in var_name:
        masked = value[:10] + "..." if len(value) > 10 else "***"
        return True, f"✅ Configurado: {masked}"
    
    return True, f"✅ Configurado: {value[:50]}"

def main():
    """Verifica todas as configurações."""
    print("=" * 70)
    print("🔍 Verificação de Chaves e Configurações")
    print("=" * 70)
    print()
    
    # Categorias
    categories = {
        "🔴 CRÍTICO": [
            ("NEO4J_URI", "URI do Neo4j Aura DB", ["Neo4j", "GraphRAG"]),
            ("NEO4J_USERNAME", "Username do Neo4j", ["Neo4j"]),
            ("NEO4J_PASSWORD", "Senha do Neo4j", ["Neo4j"]),
        ],
        "🟡 IMPORTANTE - APIs": [
            ("OPENAI_API_KEY", "Chave da API OpenAI", ["OpenAI LLM", "OpenAI Embeddings"]),
            ("GOOGLE_API_KEY", "Chave da API Google", ["Google Embeddings"]),
            ("AWS_ACCESS_KEY_ID", "AWS Access Key ID", ["AWS Bedrock"]),
            ("AWS_SECRET_ACCESS_KEY", "AWS Secret Access Key", ["AWS Bedrock"]),
            ("AWS_DEFAULT_REGION", "Região AWS", ["AWS Bedrock"]),
        ],
        "🟡 IMPORTANTE - Bancos de Dados": [
            ("SUPABASE_URL", "URL do Supabase", ["Supabase DB"]),
            ("SUPABASE_KEY", "Chave do Supabase", ["Supabase DB"]),
            ("SUPABASE_SERVICE_ROLE_KEY", "Service Role Key do Supabase", ["Supabase DB (opcional)"]),
            ("NEON_DATABASE_URL", "URL do Neon", ["Neon DB"]),
            ("NEON_PROJECT_ID", "Project ID do Neon", ["Neon DB (opcional)"]),
            ("MONGODB_URI", "URI do MongoDB", ["MongoDB"]),
            ("MONGODB_DATABASE", "Database do MongoDB", ["MongoDB"]),
        ],
        "🟢 OPCIONAL": [
            ("LANGCHAIN_TRACING_V2", "Habilitar LangChain Tracing", ["LangSmith"]),
            ("LANGCHAIN_API_KEY", "Chave da API LangChain", ["LangSmith"]),
            ("LANGCHAIN_PROJECT", "Projeto LangChain", ["LangSmith"]),
            ("OBSIDIAN_VAULT_PATH", "Caminho do Vault Obsidian", ["Obsidian Integration"]),
            ("OLLAMA_BASE_URL", "URL do Ollama", ["Ollama LLM"]),
        ],
        "⚙️ CONFIGURAÇÕES": [
            ("LLM", "Modelo LLM", ["Todos os agentes"]),
            ("EMBEDDING_MODEL", "Modelo de Embedding", ["RAG", "Vector Search"]),
        ]
    }
    
    total = 0
    configured = 0
    missing = 0
    
    for category, vars_list in categories.items():
        print(f"\n{category}")
        print("-" * 70)
        
        for var_name, description, required_for in vars_list:
            total += 1
            is_configured, status = check_variable(var_name, description, required_for)
            
            if is_configured:
                configured += 1
            else:
                missing += 1
            
            print(f"  {var_name:30} {status}")
            if not is_configured and required_for:
                print(f"    {'':30} Necessário para: {', '.join(required_for)}")
    
    # Resumo
    print()
    print("=" * 70)
    print("📊 RESUMO")
    print("=" * 70)
    print(f"  Total de configurações: {total}")
    print(f"  ✅ Configuradas: {configured}")
    print(f"  ❌ Faltando: {missing}")
    print(f"  📈 Percentual: {(configured/total)*100:.1f}%")
    print()
    
    # Recomendações
    if missing > 0:
        print("💡 RECOMENDAÇÕES:")
        print()
        
        # Verifica críticos
        neo4j_uri = os.getenv("NEO4J_URI", "")
        if not neo4j_uri or neo4j_uri.startswith("SUBSTITUA"):
            print("  🔴 URGENTE: Configure NEO4J_URI no arquivo .env")
            print("     Veja: docs/NEO4J_AURA_SETUP.md")
            print()
        
        # Verifica LLM/Embedding
        llm = os.getenv("LLM", "llama2")
        embedding = os.getenv("EMBEDDING_MODEL", "sentence_transformer")
        
        if "gpt" in llm.lower() and not os.getenv("OPENAI_API_KEY"):
            print("  🟡 Configure OPENAI_API_KEY para usar OpenAI")
            print("     Obtenha em: https://platform.openai.com/api-keys")
            print()
        
        if "google" in embedding.lower() and not os.getenv("GOOGLE_API_KEY"):
            print("  🟡 Configure GOOGLE_API_KEY para usar Google embeddings")
            print("     Obtenha em: https://makersuite.google.com/app/apikey")
            print()
        
        print("  📚 Veja lista completa em: docs/CHAVES_E_CONFIGURACOES_FALTANTES.md")
    
    print()
    print("=" * 70)

if __name__ == "__main__":
    main()


