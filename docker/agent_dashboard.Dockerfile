FROM langchain/langchain

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

COPY config/requirements.txt .

RUN pip install --upgrade -r requirements.txt

# Copia o código fonte
COPY src/ ./src/
COPY config/ ./config/

# Expõe a porta do Streamlit
EXPOSE 8507

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8507/_stcore/health || exit 1

# Comando para executar a interface
ENTRYPOINT ["streamlit", "run", "src/apps/agent_dashboard.py", "--server.port=8507", "--server.address=0.0.0.0"]

