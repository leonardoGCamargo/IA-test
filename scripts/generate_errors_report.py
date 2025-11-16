"""
Script para gerar relatório completo de erros e configurações faltantes.

Uso:
    python scripts/generate_errors_report.py
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime
import json

# Adiciona o diretório raiz ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Carrega .env
env_file = project_root / ".env"
if env_file.exists():
    load_dotenv(env_file)
else:
    load_dotenv()

def check_config(var_name: str, description: str, required_for: list = None) -> dict:
    """Verifica se uma configuração está presente."""
    value = os.getenv(var_name)
    
    is_configured = bool(value and value.strip() and 
                       not value.startswith("SUBSTITUA") and 
                       value != "password" and
                       value.strip() != "")
    
    # Mascarar valores sensíveis
    if is_configured and ("PASSWORD" in var_name or "KEY" in var_name or "SECRET" in var_name):
        masked_value = value[:10] + "..." if len(value) > 10 else "***"
    else:
        masked_value = value if value else None
    
    return {
        "name": var_name,
        "description": description,
        "required_for": required_for or [],
        "configured": is_configured,
        "value": masked_value if is_configured else None,
        "status": "✅ Configurado" if is_configured else "❌ Não configurado"
    }

def generate_report():
    """Gera relatório completo."""
    print("=" * 70)
    print("📋 Gerando Relatório de Erros e Configurações")
    print("=" * 70)
    print()
    
    # Categorias
    critical = [
        check_config("NEO4J_URI", "URI do Neo4j Aura DB", ["Neo4j", "GraphRAG"]),
        check_config("NEO4J_USERNAME", "Username do Neo4j", ["Neo4j"]),
        check_config("NEO4J_PASSWORD", "Senha do Neo4j", ["Neo4j"]),
    ]
    
    important_apis = [
        check_config("OPENAI_API_KEY", "Chave da API OpenAI", ["OpenAI LLM", "OpenAI Embeddings"]),
        check_config("GOOGLE_API_KEY", "Chave da API Google", ["Google Embeddings"]),
        check_config("AWS_ACCESS_KEY_ID", "AWS Access Key ID", ["AWS Bedrock"]),
        check_config("AWS_SECRET_ACCESS_KEY", "AWS Secret Access Key", ["AWS Bedrock"]),
        check_config("AWS_DEFAULT_REGION", "Região AWS", ["AWS Bedrock"]),
    ]
    
    important_databases = [
        check_config("SUPABASE_URL", "URL do Supabase", ["Supabase DB"]),
        check_config("SUPABASE_KEY", "Chave do Supabase", ["Supabase DB"]),
        check_config("SUPABASE_SERVICE_ROLE_KEY", "Service Role Key do Supabase", ["Supabase DB (opcional)"]),
        check_config("NEON_DATABASE_URL", "URL do Neon", ["Neon DB"]),
        check_config("NEON_PROJECT_ID", "Project ID do Neon", ["Neon DB (opcional)"]),
        check_config("MONGODB_URI", "URI do MongoDB", ["MongoDB"]),
        check_config("MONGODB_DATABASE", "Database do MongoDB", ["MongoDB"]),
    ]
    
    optional = [
        check_config("LANGCHAIN_TRACING_V2", "Habilitar LangChain Tracing", ["LangSmith"]),
        check_config("LANGCHAIN_API_KEY", "Chave da API LangChain", ["LangSmith"]),
        check_config("LANGCHAIN_PROJECT", "Projeto LangChain", ["LangSmith"]),
        check_config("OBSIDIAN_VAULT_PATH", "Caminho do Vault Obsidian", ["Obsidian Integration"]),
        check_config("OLLAMA_BASE_URL", "URL do Ollama", ["Ollama LLM"]),
    ]
    
    configs = [
        check_config("LLM", "Modelo LLM", ["Todos os agentes"]),
        check_config("EMBEDDING_MODEL", "Modelo de Embedding", ["RAG", "Vector Search"]),
    ]
    
    # Compilar relatório
    report = {
        "generated_at": datetime.now().isoformat(),
        "critical": critical,
        "important_apis": important_apis,
        "important_databases": important_databases,
        "optional": optional,
        "configs": configs,
        "summary": {
            "total": len(critical) + len(important_apis) + len(important_databases) + len(optional) + len(configs),
            "configured": sum(1 for c in critical + important_apis + important_databases + optional + configs if c["configured"]),
            "missing": sum(1 for c in critical + important_apis + important_databases + optional + configs if not c["configured"]),
        }
    }
    
    # Salvar JSON
    report_file = project_root / "Obsidian_guardar aqui" / "errors_report.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Relatório salvo em: {report_file}")
    print()
    print("📊 Resumo:")
    print(f"   Total: {report['summary']['total']}")
    print(f"   ✅ Configuradas: {report['summary']['configured']}")
    print(f"   ❌ Faltando: {report['summary']['missing']}")
    print(f"   📈 Percentual: {(report['summary']['configured']/report['summary']['total'])*100:.1f}%")
    
    return report

if __name__ == "__main__":
    generate_report()


