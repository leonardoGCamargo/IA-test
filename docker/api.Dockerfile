# Dockerfile para FastAPI Backend
FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY config/requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Instalar dependências adicionais para WebSockets
RUN pip install --no-cache-dir \
    python-socketio \
    python-multipart

# Copiar código fonte
COPY . .

# Expor porta
EXPOSE 8504

# Comando padrão (pode ser sobrescrito no docker-compose)
CMD ["uvicorn", "src.apps.api_v2:app", "--host", "0.0.0.0", "--port", "8504"]
