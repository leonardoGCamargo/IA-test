FROM python:3.11-slim

WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    docker.io \
    && rm -rf /var/lib/apt/lists/*

# Copia requirements e instala dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia código do agente
COPY mcp_docker_integration.py .
COPY mcp_neo4j_integration.py .
COPY mcp_obsidian_integration.py .
COPY chains.py .
COPY utils.py .

# Expõe porta para API (opcional, se adicionar interface web)
EXPOSE 8507

# Comando padrão: executa scan contínuo
CMD ["python", "mcp_docker_integration.py", "--scan"]

