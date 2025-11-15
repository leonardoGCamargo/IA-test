"""
Gerenciador de MCP (Model Context Protocol)
Gerencia servidores MCP, recursos e ferramentas disponíveis.
"""

import os
import json
import subprocess
import asyncio
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path
from dotenv import load_dotenv
import logging

# Tenta carregar o .env padrão, ou usa o arquivo específico se fornecido
env_file = os.getenv("MCP_ENV_FILE", ".env")
if os.path.exists(env_file):
    load_dotenv(env_file)
else:
    # Tenta carregar o arquivo específico se existir
    specific_env = "e15fdb03f6467054904bd1a6eee67b8b6839bbbc4d2e4ec3419781663c81fd57.env"
    if os.path.exists(specific_env):
        load_dotenv(specific_env)
    else:
        # Tenta carregar o .env padrão em qualquer caso
        load_dotenv()

logger = logging.getLogger(__name__)


@dataclass
class MCPServer:
    """Representa um servidor MCP configurado."""
    name: str
    command: str
    args: List[str]
    env: Optional[Dict[str, str]] = None
    enabled: bool = True
    description: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Converte o servidor para dicionário."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'MCPServer':
        """Cria um servidor a partir de um dicionário."""
        return cls(**data)


class MCPManager:
    """Gerenciador de servidores MCP."""
    
    def __init__(self, config_file: str = "mcp_servers.json"):
        """
        Inicializa o gerenciador MCP.
        
        Args:
            config_file: Caminho para o arquivo de configuração JSON
        """
        self.config_file = Path(config_file)
        self.servers: Dict[str, MCPServer] = {}
        self.active_connections: Dict[str, Any] = {}
        self.load_config()
    
    def load_config(self) -> None:
        """Carrega configuração de servidores do arquivo JSON."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.servers = {
                        name: MCPServer.from_dict(server_data)
                        for name, server_data in data.items()
                    }
                logger.info(f"Configuração carregada: {len(self.servers)} servidores")
            except Exception as e:
                logger.error(f"Erro ao carregar configuração: {e}")
                self.servers = {}
        else:
            # Configuração padrão com alguns servidores comuns
            self._init_default_servers()
            self.save_config()
    
    def _init_default_servers(self) -> None:
        """Inicializa servidores MCP padrão."""
        default_servers = {
            "filesystem": MCPServer(
                name="filesystem",
                command="npx",
                args=["-y", "@modelcontextprotocol/server-filesystem", os.getcwd()],
                description="Servidor MCP para acesso ao sistema de arquivos",
                enabled=False
            ),
            "git": MCPServer(
                name="git",
                command="npx",
                args=["-y", "@modelcontextprotocol/server-git", os.getcwd()],
                description="Servidor MCP para operações Git",
                enabled=False
            ),
        }
        self.servers.update(default_servers)
    
    def save_config(self) -> bool:
        """Salva configuração de servidores no arquivo JSON."""
        try:
            data = {
                name: server.to_dict()
                for name, server in self.servers.items()
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info("Configuração salva com sucesso")
            return True
        except Exception as e:
            logger.error(f"Erro ao salvar configuração: {e}")
            return False
    
    def add_server(self, server: MCPServer) -> bool:
        """
        Adiciona um novo servidor MCP.
        
        Args:
            server: Instância de MCPServer
            
        Returns:
            True se adicionado com sucesso
        """
        self.servers[server.name] = server
        return self.save_config()
    
    def remove_server(self, name: str) -> bool:
        """
        Remove um servidor MCP.
        
        Args:
            name: Nome do servidor
            
        Returns:
            True se removido com sucesso
        """
        if name in self.servers:
            del self.servers[name]
            if name in self.active_connections:
                del self.active_connections[name]
            return self.save_config()
        return False
    
    def get_server(self, name: str) -> Optional[MCPServer]:
        """Retorna um servidor pelo nome."""
        return self.servers.get(name)
    
    def list_servers(self) -> List[MCPServer]:
        """Lista todos os servidores configurados."""
        return list(self.servers.values())
    
    def list_enabled_servers(self) -> List[MCPServer]:
        """Lista apenas servidores habilitados."""
        return [s for s in self.servers.values() if s.enabled]
    
    def enable_server(self, name: str) -> bool:
        """Habilita um servidor."""
        if name in self.servers:
            self.servers[name].enabled = True
            return self.save_config()
        return False
    
    def disable_server(self, name: str) -> bool:
        """Desabilita um servidor."""
        if name in self.servers:
            self.servers[name].enabled = False
            return self.save_config()
        return False
    
    async def check_server_health(self, name: str) -> Dict[str, Any]:
        """
        Verifica a saúde de um servidor MCP.
        
        Args:
            name: Nome do servidor
            
        Returns:
            Dicionário com informações de saúde
        """
        server = self.get_server(name)
        if not server:
            return {"status": "not_found", "error": "Servidor não encontrado"}
        
        if not server.enabled:
            return {"status": "disabled", "message": "Servidor desabilitado"}
        
        try:
            # Tenta executar o comando para verificar se está disponível
            cmd = [server.command] + server.args
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=os.environ.copy() if not server.env else {**os.environ, **server.env}
            )
            
            # Aguarda um pouco para ver se o processo inicia
            try:
                await asyncio.wait_for(process.wait(), timeout=2.0)
                stdout, stderr = await process.communicate()
                return {
                    "status": "available",
                    "stdout": stdout.decode() if stdout else "",
                    "stderr": stderr.decode() if stderr else ""
                }
            except asyncio.TimeoutError:
                process.kill()
                return {
                    "status": "available",
                    "message": "Servidor respondeu (processo iniciado)"
                }
        except FileNotFoundError:
            return {
                "status": "error",
                "error": f"Comando '{server.command}' não encontrado"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def get_server_info(self, name: str) -> Dict[str, Any]:
        """
        Retorna informações detalhadas sobre um servidor.
        
        Args:
            name: Nome do servidor
            
        Returns:
            Dicionário com informações do servidor
        """
        server = self.get_server(name)
        if not server:
            return {"error": "Servidor não encontrado"}
        
        info = {
            "name": server.name,
            "command": server.command,
            "args": server.args,
            "enabled": server.enabled,
            "description": server.description,
            "is_connected": name in self.active_connections
        }
        
        return info
    
    def list_resources(self, server_name: Optional[str] = None) -> Dict[str, List[Dict]]:
        """
        Lista recursos disponíveis dos servidores MCP.
        
        Args:
            server_name: Nome do servidor (None para todos)
            
        Returns:
            Dicionário mapeando nome do servidor para lista de recursos
        """
        resources = {}
        
        servers_to_check = [server_name] if server_name else self.servers.keys()
        
        for name in servers_to_check:
            server = self.get_server(name)
            if server and server.enabled:
                # Em uma implementação real, isso se conectaria ao servidor MCP
                # e listaria os recursos disponíveis usando o protocolo MCP
                resources[name] = [
                    {
                        "uri": f"mcp://{name}/resource/example",
                        "name": "Exemplo de Recurso",
                        "description": "Recurso de exemplo do servidor MCP",
                        "mimeType": "text/plain"
                    }
                ]
        
        return resources
    
    def list_tools(self, server_name: Optional[str] = None) -> Dict[str, List[Dict]]:
        """
        Lista ferramentas disponíveis dos servidores MCP.
        
        Args:
            server_name: Nome do servidor (None para todos)
            
        Returns:
            Dicionário mapeando nome do servidor para lista de ferramentas
        """
        tools = {}
        
        servers_to_check = [server_name] if server_name else self.servers.keys()
        
        for name in servers_to_check:
            server = self.get_server(name)
            if server and server.enabled:
                # Em uma implementação real, isso se conectaria ao servidor MCP
                # e listaria as ferramentas disponíveis usando o protocolo MCP
                tools[name] = [
                    {
                        "name": "example_tool",
                        "description": "Ferramenta de exemplo",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "param": {
                                    "type": "string",
                                    "description": "Parâmetro de exemplo"
                                }
                            }
                        }
                    }
                ]
        
        return tools
    
    def connect_server(self, name: str) -> bool:
        """
        Conecta a um servidor MCP.
        
        Args:
            name: Nome do servidor
            
        Returns:
            True se conectado com sucesso
        """
        server = self.get_server(name)
        if not server or not server.enabled:
            return False
        
        if name in self.active_connections:
            return True  # Já está conectado
        
        try:
            # Em uma implementação real, isso iniciaria uma conexão com o servidor MCP
            # usando stdio, HTTP ou outro transporte
            from datetime import datetime
            self.active_connections[name] = {
                "server": server,
                "connected_at": datetime.now().isoformat(),
                "status": "connected"
            }
            logger.info(f"Servidor MCP '{name}' conectado")
            return True
        except Exception as e:
            logger.error(f"Erro ao conectar servidor '{name}': {e}")
            return False
    
    def disconnect_server(self, name: str) -> bool:
        """
        Desconecta de um servidor MCP.
        
        Args:
            name: Nome do servidor
            
        Returns:
            True se desconectado com sucesso
        """
        if name in self.active_connections:
            del self.active_connections[name]
            logger.info(f"Servidor MCP '{name}' desconectado")
            return True
        return False
    
    def get_server_status(self, name: str) -> Dict[str, Any]:
        """
        Retorna o status de um servidor MCP.
        
        Args:
            name: Nome do servidor
            
        Returns:
            Dicionário com status do servidor
        """
        server = self.get_server(name)
        if not server:
            return {"status": "not_found"}
        
        is_connected = name in self.active_connections
        connection_info = self.active_connections.get(name, {})
        
        return {
            "name": name,
            "enabled": server.enabled,
            "connected": is_connected,
            "connection_info": connection_info,
            "command": server.command,
            "description": server.description
        }
    
    def get_all_servers_status(self) -> Dict[str, Dict[str, Any]]:
        """
        Retorna o status de todos os servidores MCP.
        
        Returns:
            Dicionário mapeando nome do servidor para seu status
        """
        return {
            name: self.get_server_status(name)
            for name in self.servers.keys()
        }


# Instância global do gerenciador
_manager_instance: Optional[MCPManager] = None


def get_mcp_manager() -> MCPManager:
    """Retorna a instância global do gerenciador MCP."""
    global _manager_instance
    if _manager_instance is None:
        _manager_instance = MCPManager()
    return _manager_instance


