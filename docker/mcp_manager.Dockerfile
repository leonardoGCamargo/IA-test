FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar arquivos do gerenciador MCP
COPY mcp_manager.py .
COPY mcp_manager_ui.py .
COPY mcp_docker_integration.py .
COPY mcp_obsidian_integration.py .
COPY mcp_neo4j_integration.py .
COPY chains.py .
COPY utils.py .

# Expor porta do Streamlit
EXPOSE 8506

# Comando para executar a interface
CMD ["streamlit", "run", "mcp_manager_ui.py", "--server.port=8506", "--server.address=0.0.0.0"]


