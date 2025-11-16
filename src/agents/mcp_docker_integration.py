"""
Docker Integration Agent - Identifica e gerencia servidores MCP no Docker.

Este módulo fornece funcionalidades para:
- Detectar containers Docker em execução
- Identificar servidores MCP automaticamente
- Enviar informações para Neo4j e Obsidian
- Atualizar docker-compose.yml automaticamente
"""

import os
import json
import re
import subprocess
import yaml
from typing import List, Dict, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
import logging
from dotenv import load_dotenv

# Importa integrações existentes
try:
    from src.agents.mcp_neo4j_integration import Neo4jGraphRAGManager, get_neo4j_manager
    from src.agents.mcp_obsidian_integration import ObsidianManager
except ImportError:
    # Fallback se os módulos não estiverem disponíveis
    Neo4jGraphRAGManager = None
    ObsidianManager = None

load_dotenv()

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class DockerService:
    """Representa um serviço Docker em execução."""
    name: str
    status: str
    ports: List[str]
    image: Optional[str] = None
    container_id: Optional[str] = None
    environment: Optional[Dict[str, str]] = None
    networks: Optional[List[str]] = None
    volumes: Optional[List[str]] = None
    labels: Optional[Dict[str, str]] = None


@dataclass
class MCPServerInfo:
    """Informações sobre um servidor MCP detectado."""
    name: str
    container_name: str
    image: str
    ports: List[str]
    command: Optional[str] = None
    args: Optional[List[str]] = None
    description: Optional[str] = None
    enabled: bool = True
    resources: Optional[List[Dict]] = None
    tools: Optional[List[Dict]] = None
    detected_at: Optional[str] = None


class DockerMCPDetector:
    """Detecta servidores MCP em execução no Docker."""
    
    def __init__(self, docker_compose_file: str = "docker-compose.yml"):
        """
        Inicializa o detector.
        
        Args:
            docker_compose_file: Caminho para o arquivo docker-compose.yml
        """
        self.docker_compose_file = Path(docker_compose_file)
        if not self.docker_compose_file.exists():
            logger.warning(f"Arquivo docker-compose.yml não encontrado: {docker_compose_file}")
    
    def list_running_containers(self) -> List[DockerService]:
        """
        Lista todos os containers Docker em execução.
        
        Returns:
            Lista de serviços Docker
        """
        try:
            result = subprocess.run(
                ["docker", "ps", "--format", "json"],
                capture_output=True,
                text=True,
                check=True,
                timeout=30
            )
            
            containers = []
            for line in result.stdout.strip().split('\n'):
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    containers.append(DockerService(
                        name=data.get("Names", "").lstrip('/'),
                        status=data.get("Status", ""),
                        ports=self._parse_ports(data.get("Ports", "")),
                        image=data.get("Image", ""),
                        container_id=data.get("ID", "")
                    ))
                except json.JSONDecodeError as e:
                    logger.debug(f"Erro ao parsear JSON do container: {e}")
                    continue
            
            logger.info(f"Encontrados {len(containers)} containers em execução")
            return containers
        except subprocess.CalledProcessError as e:
            logger.error(f"Erro ao listar containers: {e}")
            return []
        except subprocess.TimeoutExpired:
            logger.error("Timeout ao listar containers Docker")
            return []
        except FileNotFoundError:
            logger.error("Docker não encontrado. Certifique-se de que o Docker está instalado.")
            return []
    
    def _parse_ports(self, ports_str: str) -> List[str]:
        """Parseia a string de portas do Docker."""
        if not ports_str:
            return []
        # Formato: "0.0.0.0:8501->8501/tcp, 0.0.0.0:8502->8502/tcp"
        ports = []
        for port_mapping in ports_str.split(','):
            port_mapping = port_mapping.strip()
            if '->' in port_mapping:
                external = port_mapping.split('->')[0].strip()
                # Remove IP se presente
                if ':' in external:
                    external = external.split(':')[1]
                ports.append(external)
            elif port_mapping:
                # Porta sem mapeamento externo
                ports.append(port_mapping.split('/')[0])
        return ports
    
    def get_service_info(self, service_name: str) -> Optional[Dict]:
        """
        Obtém informações detalhadas de um serviço Docker.
        
        Args:
            service_name: Nome do serviço ou container
            
        Returns:
            Dicionário com informações do serviço
        """
        try:
            result = subprocess.run(
                ["docker", "inspect", service_name],
                capture_output=True,
                text=True,
                check=True,
                timeout=30
            )
            
            data = json.loads(result.stdout)
            if data:
                container = data[0]
                network_settings = container.get("NetworkSettings", {})
                config = container.get("Config", {})
                
                return {
                    "id": container.get("Id", ""),
                    "name": container.get("Name", "").lstrip('/'),
                    "status": container.get("State", {}).get("Status", ""),
                    "image": config.get("Image", ""),
                    "ports": self._extract_ports(network_settings),
                    "env": config.get("Env", []),
                    "mounts": container.get("Mounts", []),
                    "labels": config.get("Labels", {}),
                    "networks": list(network_settings.get("Networks", {}).keys()),
                    "command": config.get("Cmd", []),
                    "entrypoint": config.get("Entrypoint", []),
                    "working_dir": config.get("WorkingDir", ""),
                    "created": container.get("Created", "")
                }
        except subprocess.CalledProcessError as e:
            logger.error(f"Erro ao inspecionar container {service_name}: {e}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Erro ao parsear JSON do inspect: {e}")
            return None
        except subprocess.TimeoutExpired:
            logger.error(f"Timeout ao inspecionar container {service_name}")
            return None
    
    def _extract_ports(self, network_settings: Dict) -> List[Dict]:
        """Extrai informações de portas do container."""
        ports = []
        port_bindings = network_settings.get("Ports", {})
        
        for container_port, host_bindings in port_bindings.items():
            if host_bindings:
                for binding in host_bindings:
                    ports.append({
                        "container_port": container_port.split('/')[0],
                        "protocol": container_port.split('/')[1] if '/' in container_port else "tcp",
                        "host_ip": binding.get("HostIp", "0.0.0.0"),
                        "host_port": binding.get("HostPort", "")
                    })
            else:
                # Porta exposta mas não mapeada
                ports.append({
                    "container_port": container_port.split('/')[0],
                    "protocol": container_port.split('/')[1] if '/' in container_port else "tcp",
                    "host_ip": None,
                    "host_port": None
                })
        
        return ports
    
    def detect_mcp_services(self) -> List[MCPServerInfo]:
        """
        Detecta serviços que podem ser servidores MCP.
        
        Returns:
            Lista de servidores MCP detectados
        """
        containers = self.list_running_containers()
        mcp_services = []
        
        # Padrões que indicam servidores MCP
        mcp_keywords = [
            'mcp',
            'model-context',
            'model_context',
            'mcp-server',
            'mcp_server'
        ]
        
        for container in containers:
            is_mcp = False
            mcp_name = None
            
            # Verifica nome do container
            if any(keyword in container.name.lower() for keyword in mcp_keywords):
                is_mcp = True
                mcp_name = container.name
            
            # Verifica imagem
            if not is_mcp and container.image:
                if any(keyword in container.image.lower() for keyword in mcp_keywords):
                    is_mcp = True
                    mcp_name = mcp_name or container.name
            
            # Verifica labels do container
            if not is_mcp:
                service_info = self.get_service_info(container.name)
                if service_info:
                    labels = service_info.get("labels", {})
                    for key, value in labels.items():
                        if any(keyword in key.lower() or keyword in str(value).lower() for keyword in mcp_keywords):
                            is_mcp = True
                            mcp_name = mcp_name or container.name
                            break
            
            if is_mcp:
                # Obtém informações detalhadas
                service_info = self.get_service_info(container.name)
                if service_info:
                    mcp_info = MCPServerInfo(
                        name=mcp_name,
                        container_name=container.name,
                        image=container.image or service_info.get("image", ""),
                        ports=container.ports,
                        command=" ".join(service_info.get("command", [])) if service_info.get("command") else None,
                        args=service_info.get("command", []),
                        description=f"Servidor MCP detectado no container {container.name}",
                        enabled=True,
                        detected_at=datetime.now().isoformat()
                    )
                    mcp_services.append(mcp_info)
        
        logger.info(f"Detectados {len(mcp_services)} servidores MCP")
        return mcp_services
    
    def list_compose_services(self) -> List[str]:
        """
        Lista serviços definidos no docker-compose.yml.
        
        Returns:
            Lista de nomes de serviços
        """
        if not self.docker_compose_file.exists():
            return []
        
        try:
            # Tenta com docker compose (versão mais recente)
            result = subprocess.run(
                ["docker", "compose", "config", "--services"],
                capture_output=True,
                text=True,
                check=True,
                timeout=30,
                cwd=self.docker_compose_file.parent
            )
            services = [s.strip() for s in result.stdout.strip().split('\n') if s.strip()]
            logger.info(f"Encontrados {len(services)} serviços no docker-compose.yml")
            return services
        except subprocess.CalledProcessError:
            # Tenta com docker-compose (versão antiga)
            try:
                result = subprocess.run(
                    ["docker-compose", "config", "--services"],
                    capture_output=True,
                    text=True,
                    check=True,
                    timeout=30,
                    cwd=self.docker_compose_file.parent
                )
                services = [s.strip() for s in result.stdout.strip().split('\n') if s.strip()]
                logger.info(f"Encontrados {len(services)} serviços no docker-compose.yml")
                return services
            except subprocess.CalledProcessError as e:
                logger.error(f"Erro ao listar serviços do compose: {e}")
                return []
        except FileNotFoundError:
            logger.error("docker-compose não encontrado")
            return []
        except subprocess.TimeoutExpired:
            logger.error("Timeout ao listar serviços do compose")
            return []
    
    def read_compose_file(self) -> Optional[Dict]:
        """
        Lê o arquivo docker-compose.yml.
        
        Returns:
            Dicionário com o conteúdo do compose ou None em caso de erro
        """
        if not self.docker_compose_file.exists():
            logger.error(f"Arquivo não encontrado: {self.docker_compose_file}")
            return None
        
        try:
            with open(self.docker_compose_file, 'r', encoding='utf-8') as f:
                content = yaml.safe_load(f)
            return content
        except yaml.YAMLError as e:
            logger.error(f"Erro ao parsear YAML: {e}")
            return None
        except Exception as e:
            logger.error(f"Erro ao ler arquivo: {e}")
            return None
    
    def update_compose_file(self, mcp_service: MCPServerInfo, service_config: Optional[Dict] = None) -> bool:
        """
        Atualiza o docker-compose.yml com um novo serviço MCP.
        
        Args:
            mcp_service: Informações do servidor MCP
            service_config: Configuração adicional do serviço (opcional)
            
        Returns:
            True se atualizado com sucesso
        """
        compose_data = self.read_compose_file()
        if not compose_data:
            logger.error("Não foi possível ler o docker-compose.yml")
            return False
        
        # Garante que 'services' existe
        if "services" not in compose_data:
            compose_data["services"] = {}
        
        # Nome do serviço (sanitizado)
        service_name = mcp_service.name.replace('_', '-').replace(' ', '-').lower()
        
        # Se o serviço já existe, atualiza
        if service_name in compose_data["services"]:
            logger.info(f"Serviço {service_name} já existe no compose, atualizando...")
        else:
            logger.info(f"Adicionando novo serviço {service_name} ao compose...")
        
        # Configuração do serviço
        service_def = {
            "image": mcp_service.image,
            "container_name": mcp_service.container_name,
            "networks": ["net"]  # Assume rede padrão
        }
        
        # Adiciona portas se houver
        if mcp_service.ports:
            ports = []
            for port in mcp_service.ports:
                if ':' in port:
                    # Formato host:container
                    ports.append(port)
                else:
                    # Apenas porta do container
                    ports.append(f"{port}:{port}")
            service_def["ports"] = ports
        
        # Adiciona comando se houver
        if mcp_service.command:
            service_def["command"] = mcp_service.command
        
        # Adiciona variáveis de ambiente se houver
        env_vars = {}
        if mcp_service.environment:
            env_vars.update(mcp_service.environment)
        
        # Adiciona configurações customizadas
        if service_config:
            service_def.update(service_config)
        
        if env_vars:
            service_def["environment"] = [f"{k}={v}" for k, v in env_vars.items()]
        
        # Adiciona labels para identificação MCP
        if "labels" not in service_def:
            service_def["labels"] = []
        service_def["labels"].extend([
            "mcp.server=true",
            f"mcp.name={mcp_service.name}",
            f"mcp.detected_at={mcp_service.detected_at}"
        ])
        
        # Atualiza o compose
        compose_data["services"][service_name] = service_def
        
        # Salva o arquivo
        try:
            with open(self.docker_compose_file, 'w', encoding='utf-8') as f:
                yaml.dump(compose_data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
            logger.info(f"docker-compose.yml atualizado com serviço {service_name}")
            return True
        except Exception as e:
            logger.error(f"Erro ao salvar docker-compose.yml: {e}")
            return False


class DockerIntegrationAgent:
    """
    Agente principal de integração Docker.
    
    Coordena detecção de MCPs, envio para Neo4j e Obsidian,
    e atualização do docker-compose.yml.
    """
    
    def __init__(
        self,
        docker_compose_file: str = "docker-compose.yml",
        neo4j_manager: Optional[Neo4jGraphRAGManager] = None,
        obsidian_manager: Optional[ObsidianManager] = None
    ):
        """
        Inicializa o agente de integração.
        
        Args:
            docker_compose_file: Caminho para docker-compose.yml
            neo4j_manager: Instância do gerenciador Neo4j (opcional)
            obsidian_manager: Instância do gerenciador Obsidian (opcional)
        """
        self.detector = DockerMCPDetector(docker_compose_file)
        
        # Inicializa gerenciadores
        if neo4j_manager:
            self.neo4j_manager = neo4j_manager
        elif Neo4jGraphRAGManager:
            try:
                self.neo4j_manager = get_neo4j_manager()
            except Exception as e:
                logger.warning(f"Não foi possível inicializar Neo4j manager: {e}")
                self.neo4j_manager = None
        else:
            self.neo4j_manager = None
        
        if obsidian_manager:
            self.obsidian_manager = obsidian_manager
        elif ObsidianManager:
            vault_path = os.getenv("OBSIDIAN_VAULT_PATH")
            if vault_path:
                self.obsidian_manager = ObsidianManager(vault_path)
            else:
                self.obsidian_manager = ObsidianManager()
        else:
            self.obsidian_manager = None
    
    def scan_and_sync(self, update_compose: bool = True) -> Dict[str, Any]:
        """
        Escaneia containers, detecta MCPs e sincroniza com Neo4j e Obsidian.
        
        Args:
            update_compose: Se True, atualiza docker-compose.yml automaticamente
            
        Returns:
            Dicionário com resultados da operação
        """
        results = {
            "containers_scanned": 0,
            "mcps_detected": 0,
            "neo4j_synced": 0,
            "obsidian_synced": 0,
            "compose_updated": 0,
            "errors": []
        }
        
        try:
            # 1. Detecta servidores MCP
            logger.info("Escaneando containers Docker...")
            mcp_services = self.detector.detect_mcp_services()
            results["mcps_detected"] = len(mcp_services)
            results["containers_scanned"] = len(self.detector.list_running_containers())
            
            if not mcp_services:
                logger.info("Nenhum servidor MCP detectado")
                return results
            
            logger.info(f"Detectados {len(mcp_services)} servidores MCP")
            
            # 2. Sincroniza com Neo4j
            if self.neo4j_manager:
                logger.info("Sincronizando com Neo4j...")
                for mcp in mcp_services:
                    try:
                        mcp_dict = asdict(mcp)
                        if self.neo4j_manager.create_mcp_node(mcp_dict):
                            results["neo4j_synced"] += 1
                    except Exception as e:
                        error_msg = f"Erro ao sincronizar MCP {mcp.name} com Neo4j: {e}"
                        logger.error(error_msg)
                        results["errors"].append(error_msg)
            else:
                logger.warning("Neo4j manager não disponível")
            
            # 3. Sincroniza com Obsidian
            if self.obsidian_manager:
                logger.info("Sincronizando com Obsidian...")
                for mcp in mcp_services:
                    try:
                        mcp_info = {
                            "command": mcp.command,
                            "args": mcp.args,
                            "description": mcp.description,
                            "enabled": mcp.enabled,
                            "ports": mcp.ports,
                            "resources": mcp.resources or [],
                            "tools": mcp.tools or []
                        }
                        note_path = self.obsidian_manager.create_mcp_note(mcp.name, mcp_info)
                        if note_path:
                            results["obsidian_synced"] += 1
                            
                            # Sincroniza nota com Neo4j se disponível
                            if self.neo4j_manager:
                                try:
                                    with open(note_path, 'r', encoding='utf-8') as f:
                                        content = f.read()
                                    self.neo4j_manager.create_obsidian_note_node(note_path, content)
                                    self.neo4j_manager.create_mcp_obsidian_relation(
                                        mcp.name,
                                        note_path.stem,
                                        "DOCUMENTED_IN"
                                    )
                                except Exception as e:
                                    logger.debug(f"Erro ao sincronizar nota Obsidian com Neo4j: {e}")
                    except Exception as e:
                        error_msg = f"Erro ao criar nota Obsidian para {mcp.name}: {e}"
                        logger.error(error_msg)
                        results["errors"].append(error_msg)
            else:
                logger.warning("Obsidian manager não disponível")
            
            # 4. Atualiza docker-compose.yml
            if update_compose:
                logger.info("Atualizando docker-compose.yml...")
                for mcp in mcp_services:
                    try:
                        if self.detector.update_compose_file(mcp):
                            results["compose_updated"] += 1
                    except Exception as e:
                        error_msg = f"Erro ao atualizar compose para {mcp.name}: {e}"
                        logger.error(error_msg)
                        results["errors"].append(error_msg)
            
            logger.info("Sincronização concluída com sucesso")
            return results
            
        except Exception as e:
            error_msg = f"Erro durante sincronização: {e}"
            logger.error(error_msg)
            results["errors"].append(error_msg)
            return results
    
    def get_status(self) -> Dict[str, Any]:
        """
        Obtém status atual do agente e serviços.
        
        Returns:
            Dicionário com status
        """
        status = {
            "docker_available": self._check_docker_available(),
            "containers_running": len(self.detector.list_running_containers()),
            "mcps_detected": len(self.detector.detect_mcp_services()),
            "neo4j_connected": self.neo4j_manager is not None,
            "obsidian_configured": self.obsidian_manager is not None and self.obsidian_manager.vault_path is not None,
            "compose_file_exists": self.detector.docker_compose_file.exists()
        }
        
        if self.neo4j_manager:
            try:
                stats = self.neo4j_manager.get_graph_statistics()
                status["neo4j_stats"] = stats
            except Exception as e:
                logger.debug(f"Erro ao obter estatísticas Neo4j: {e}")
        
        return status
    
    def _check_docker_available(self) -> bool:
        """Verifica se o Docker está disponível."""
        try:
            subprocess.run(
                ["docker", "version"],
                capture_output=True,
                check=True,
                timeout=10
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return False


# Função principal para uso como script
def main():
    """Função principal para execução como script."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Docker Integration Agent - Gerencia servidores MCP")
    parser.add_argument(
        "--scan",
        action="store_true",
        help="Escaneia containers e sincroniza com Neo4j/Obsidian"
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Mostra status do agente"
    )
    parser.add_argument(
        "--no-compose-update",
        action="store_true",
        help="Não atualiza docker-compose.yml durante scan"
    )
    parser.add_argument(
        "--compose-file",
        default="docker-compose.yml",
        help="Caminho para docker-compose.yml"
    )
    
    args = parser.parse_args()
    
    # Inicializa agente
    agent = DockerIntegrationAgent(docker_compose_file=args.compose_file)
    
    if args.status:
        status = agent.get_status()
        print("\n=== Status do Docker Integration Agent ===\n")
        print(json.dumps(status, indent=2, ensure_ascii=False))
    
    if args.scan:
        print("\n=== Escaneando e sincronizando... ===\n")
        results = agent.scan_and_sync(update_compose=not args.no_compose_update)
        print("\n=== Resultados ===\n")
        print(json.dumps(results, indent=2, ensure_ascii=False))
    
    if not args.scan and not args.status:
        parser.print_help()


if __name__ == "__main__":
    main()
