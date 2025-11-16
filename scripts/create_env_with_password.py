"""
Script para criar arquivo .env com a senha do Neo4j Aura DB.

Uso:
    python scripts/create_env_with_password.py
"""

import os
from pathlib import Path

def create_env_file():
    """Cria arquivo .env com a senha do Neo4j Aura DB."""
    project_root = Path(__file__).parent.parent
    env_file = project_root / ".env"
    
    # Senha fornecida pelo usuário
    neo4j_password = "zoit_O9j_sV80eNIuvU3OKXVYWAmCmaoAdBzOhBdWgM"
    
    # Conteúdo do .env
    env_content = f"""#*****************************************************************
# LLM and Embedding Model
#*****************************************************************
LLM=llama2 #or any Ollama model tag, gpt-4 (o or turbo), gpt-3.5, or any bedrock model
EMBEDDING_MODEL=sentence_transformer #or google-genai-embedding-001 openai, ollama, or aws

#*****************************************************************
# Neo4j Aura DB
#*****************************************************************
# IMPORTANTE: Substitua a URI abaixo pela URI real do seu Aura DB
# Você pode encontrar a URI no console do Neo4j Aura: https://console.neo4j.io/
# Formato: neo4j+s://xxxxx.databases.neo4j.io (ou neo4j+ssc:// para self-signed)
NEO4J_URI=neo4j+s://SUBSTITUA_PELA_URI_DO_AURA_DB.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD={neo4j_password}

#*****************************************************************
# Langchain
#*****************************************************************
# Optional for enabling Langchain Smith API

#LANGCHAIN_TRACING_V2=true # false
#LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
#LANGCHAIN_PROJECT=#your-project-name
#LANGCHAIN_API_KEY=#your-api-key ls_...

#*****************************************************************
# Ollama
#*****************************************************************
#OLLAMA_BASE_URL=http://host.docker.internal:11434

#*****************************************************************
# OpenAI
#*****************************************************************
# Only required when using OpenAI LLM or embedding model

#OPENAI_API_KEY=sk-...

#*****************************************************************
# AWS
#*****************************************************************
# Only required when using AWS Bedrock LLM or embedding model

#AWS_ACCESS_KEY_ID=
#AWS_SECRET_ACCESS_KEY=
#AWS_DEFAULT_REGION=us-east-1

#*****************************************************************
# GOOGLE
#*****************************************************************
# Only required when using GoogleGenai LLM or embedding model
GOOGLE_API_KEY=

#*****************************************************************
# MCP (Model Context Protocol)
#*****************************************************************
# Configuração opcional para servidores MCP
# O arquivo mcp_servers.json será criado automaticamente
# MCP_CONFIG_FILE=mcp_servers.json

#*****************************************************************
# OBSIDIAN
#*****************************************************************
# Caminho para o vault do Obsidian (opcional)
# OBSIDIAN_VAULT_PATH=C:/Users/SeuUsuario/Documents/Obsidian/MeuVault

#*****************************************************************
# SUPABASE
#*****************************************************************
# Configuração do Supabase (PostgreSQL com recursos adicionais)
# SUPABASE_URL=https://seu-projeto.supabase.co
# SUPABASE_KEY=seu-anon-key
# SUPABASE_SERVICE_ROLE_KEY=seu-service-role-key

#*****************************************************************
# NEON
#*****************************************************************
# Configuração do Neon (PostgreSQL serverless)
# NEON_DATABASE_URL=postgresql://usuario:senha@host/database
# NEON_PROJECT_ID=seu-project-id

#*****************************************************************
# MONGODB
#*****************************************************************
# Configuração do MongoDB
# MONGODB_URI=mongodb://usuario:senha@host:porta/database
# MONGODB_DATABASE=default
# MONGODB_ATLAS=false  # true se usar MongoDB Atlas
"""
    
    # Verifica se já existe
    if env_file.exists():
        print(f"⚠️  Arquivo .env já existe em: {env_file}")
        response = input("Deseja sobrescrever? (s/n): ").strip().lower()
        if response != 's':
            print("❌ Cancelado.")
            return False
    
    # Cria o arquivo
    try:
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        print(f"✅ Arquivo .env criado com sucesso em: {env_file}")
        print()
        print("📝 Configuração:")
        print(f"   NEO4J_PASSWORD: {neo4j_password[:20]}... (configurado)")
        print(f"   NEO4J_USERNAME: neo4j (padrão)")
        print(f"   NEO4J_URI: PRECISA SER CONFIGURADA")
        print()
        print("🔗 Próximo passo:")
        print("   1. Acesse: https://console.neo4j.io/")
        print("   2. Copie a Connection URI do seu Aura DB")
        print("   3. Edite o arquivo .env e substitua a linha NEO4J_URI")
        print()
        print("💡 Exemplo de URI:")
        print("   NEO4J_URI=neo4j+s://xxxxx.databases.neo4j.io")
        print()
        print("🧪 Após configurar a URI, teste com:")
        print("   python scripts/test_neo4j_connection.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar arquivo .env: {e}")
        return False

if __name__ == "__main__":
    create_env_file()

