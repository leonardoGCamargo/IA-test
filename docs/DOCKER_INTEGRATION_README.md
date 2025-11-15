# Docker Integration Agent

Agente completo para identificar e gerenciar servidores MCP (Model Context Protocol) no Docker.

## Funcionalidades

- ✅ **Detecção Automática**: Identifica containers Docker que são servidores MCP
- ✅ **Integração Neo4j**: Sincroniza informações com grafo de conhecimento
- ✅ **Integração Obsidian**: Cria notas automáticas sobre servidores MCP
- ✅ **Atualização Automática**: Atualiza `docker-compose.yml` com novos serviços detectados
- ✅ **Monitoramento**: Status em tempo real de containers e serviços

## Instalação

```bash
pip install -r requirements.txt
```

## Configuração

1. Configure as variáveis de ambiente no arquivo `.env`:

```env
# Neo4j
NEO4J_URI=neo4j://database:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=password

# Obsidian (opcional)
OBSIDIAN_VAULT_PATH=/caminho/para/seu/vault
```

## Uso

### Como Script

```bash
# Escanear containers e sincronizar
python mcp_docker_integration.py --scan

# Ver status do agente
python mcp_docker_integration.py --status

# Escanear sem atualizar docker-compose.yml
python mcp_docker_integration.py --scan --no-compose-update
```

### Como Módulo Python

```python
from mcp_docker_integration import DockerIntegrationAgent

# Inicializa o agente
agent = DockerIntegrationAgent()

# Escaneia e sincroniza tudo
results = agent.scan_and_sync(update_compose=True)
print(f"Detectados {results['mcps_detected']} servidores MCP")
print(f"Sincronizados {results['neo4j_synced']} com Neo4j")
print(f"Criadas {results['obsidian_synced']} notas no Obsidian")

# Verifica status
status = agent.get_status()
print(f"Docker disponível: {status['docker_available']}")
print(f"Containers em execução: {status['containers_running']}")
```

### Detecção Manual de MCPs

```python
from mcp_docker_integration import DockerMCPDetector

detector = DockerMCPDetector()

# Lista todos os containers
containers = detector.list_running_containers()
print(f"Containers encontrados: {len(containers)}")

# Detecta servidores MCP
mcps = detector.detect_mcp_services()
for mcp in mcps:
    print(f"MCP: {mcp.name}")
    print(f"  Container: {mcp.container_name}")
    print(f"  Imagem: {mcp.image}")
    print(f"  Portas: {mcp.ports}")
```

## Como Funciona

### Detecção de MCPs

O agente identifica servidores MCP através de:

1. **Nome do container**: Busca por palavras-chave como `mcp`, `model-context`, `mcp-server`
2. **Imagem Docker**: Verifica se a imagem contém indicadores de MCP
3. **Labels**: Analisa labels do container para identificação

### Sincronização com Neo4j

- Cria nós do tipo `MCP` no grafo Neo4j
- Armazena embeddings para busca semântica
- Cria relações com notas do Obsidian e sistemas RAG

### Sincronização com Obsidian

- Cria notas em Markdown na pasta `MCP/`
- Inclui informações sobre portas, comandos e recursos
- Cria links bidirecionais entre notas relacionadas

### Atualização do docker-compose.yml

- Adiciona novos serviços MCP detectados
- Mantém configurações existentes
- Adiciona labels para identificação

## Estrutura de Dados

### MCPServerInfo

```python
@dataclass
class MCPServerInfo:
    name: str                    # Nome do servidor MCP
    container_name: str          # Nome do container Docker
    image: str                   # Imagem Docker
    ports: List[str]             # Portas expostas
    command: Optional[str]       # Comando de execução
    args: Optional[List[str]]    # Argumentos do comando
    description: Optional[str]   # Descrição
    enabled: bool                # Status (habilitado/desabilitado)
    resources: Optional[List[Dict]]  # Recursos disponíveis
    tools: Optional[List[Dict]]       # Ferramentas disponíveis
    detected_at: Optional[str]        # Data/hora de detecção
```

## Integração com Docker Compose

O agente pode ser adicionado ao `docker-compose.yml` como um serviço:

```yaml
mcp-docker-agent:
  build:
    context: .
    dockerfile: mcp_docker_integration.Dockerfile
  volumes:
    - /var/run/docker.sock:/var/run/docker.sock
    - ./docker-compose.yml:/app/docker-compose.yml
  environment:
    - NEO4J_URI=${NEO4J_URI}
    - NEO4J_USERNAME=${NEO4J_USERNAME}
    - NEO4J_PASSWORD=${NEO4J_PASSWORD}
    - OBSIDIAN_VAULT_PATH=${OBSIDIAN_VAULT_PATH}
  networks:
    - net
  depends_on:
    - database
```

## Troubleshooting

### Docker não encontrado

Certifique-se de que o Docker está instalado e acessível:

```bash
docker version
```

### Neo4j não conecta

Verifique as credenciais no `.env` e se o container do Neo4j está rodando:

```bash
docker ps | grep neo4j
```

### Obsidian não cria notas

Configure o caminho do vault:

```env
OBSIDIAN_VAULT_PATH=/caminho/completo/para/vault
```

## Logs

O agente usa logging padrão do Python. Configure o nível:

```python
import logging
logging.basicConfig(level=logging.DEBUG)  # Para logs detalhados
```

## Contribuindo

Este agente faz parte do sistema de gerenciamento MCP. Para melhorias:

1. Adicione novos padrões de detecção em `detect_mcp_services()`
2. Estenda a integração Neo4j em `Neo4jGraphRAGManager`
3. Melhore templates Obsidian em `ObsidianManager`

## Licença

Mesma licença do projeto principal.

