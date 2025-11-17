# -*- coding: utf-8 -*-
"""
Script para adicionar suporte ao Google Gemini como LLM
"""

from pathlib import Path

project_root = Path(__file__).parent.parent
chains_file = project_root / "src" / "apps" / "chains.py"

def adicionar_suporte_gemini():
    """Adiciona suporte ao Gemini no load_llm()."""
    
    if not chains_file.exists():
        print("Arquivo chains.py nao encontrado!")
        return False
    
    conteudo = chains_file.read_text(encoding='utf-8')
    
    # Verifica se já tem suporte
    if "ChatGoogleGenerativeAI" in conteudo or "gemini" in conteudo.lower():
        print("Suporte ao Gemini ja existe!")
        return False
    
    # Adiciona import
    import_google = "from langchain_google_genai import ChatGoogleGenerativeAI\n"
    
    # Encontra linha dos imports
    linhas = conteudo.split('\n')
    nova_import_pos = None
    
    for i, linha in enumerate(linhas):
        if "from langchain_google_genai import GoogleGenerativeAIEmbeddings" in linha:
            nova_import_pos = i + 1
            break
    
    if nova_import_pos:
        linhas.insert(nova_import_pos, import_google)
    else:
        # Adiciona após outros imports do langchain
        for i, linha in enumerate(linhas):
            if "from langchain_aws import ChatBedrock" in linha:
                linhas.insert(i + 1, import_google)
                break
    
    # Adiciona suporte no load_llm
    # Procura pela seção do Ollama
    novo_codigo = """    elif llm_name in ["gemini", "gemini-pro", "gemini-1.5-pro", "gemini-1.5-flash"]:
        import os
        logger.info(f"LLM: Using Google Gemini: {llm_name}")
        google_api_key = os.getenv("GOOGLE_API_KEY")
        if not google_api_key:
            raise ValueError("GOOGLE_API_KEY não configurada. Configure no arquivo .env")
        return ChatGoogleGenerativeAI(
            model=llm_name.replace("gemini-", "gemini-1.5-") if "gemini-pro" in llm_name else llm_name,
            temperature=0,
            google_api_key=google_api_key,
            streaming=True
        )
    
    """
    
    # Encontra onde adicionar (antes do elif len(llm_name))
    conteudo_atualizado = '\n'.join(linhas)
    
    # Adiciona antes do elif len(llm_name)
    if "elif len(llm_name):" in conteudo_atualizado:
        conteudo_atualizado = conteudo_atualizado.replace(
            "    elif len(llm_name):",
            novo_codigo + "    elif len(llm_name):"
        )
    else:
        # Adiciona antes do fallback final
        conteudo_atualizado = conteudo_atualizado.replace(
            "    logger.info(\"LLM: Using GPT-3.5\")",
            novo_codigo + "    logger.info(\"LLM: Using GPT-3.5\")"
        )
    
    # Salva
    chains_file.write_text(conteudo_atualizado, encoding='utf-8')
    print("Suporte ao Gemini adicionado com sucesso!")
    print()
    print("Para usar Gemini, configure no .env:")
    print("  LLM=gemini-pro")
    print("  GOOGLE_API_KEY=your_google_api_key_here")
    
    return True

if __name__ == "__main__":
    print("=" * 70)
    print("ADICIONANDO SUPORTE AO GOOGLE GEMINI")
    print("=" * 70)
    print()
    adicionar_suporte_gemini()
    print()
    print("=" * 70)

