"""
Agente Gerenciador de Banco de Dados - Suporte para Supabase, Neon e MongoDB.

Este módulo fornece uma interface unificada para gerenciar diferentes tipos de bancos de dados,
permitindo que o sistema trabalhe com Supabase (PostgreSQL), Neon (PostgreSQL) e MongoDB
dentro dos limites de cada plataforma.
"""

import os
import logging
from typing import Dict, List, Optional, Any, Union
from enum import Enum
from dataclasses import dataclass, asdict
from datetime import datetime
from dotenv import load_dotenv

# Importações condicionais
try:
    from supabase import create_client, Client
    from langchain_community.vectorstores import SupabaseVectorStore
    from langchain_openai import OpenAIEmbeddings
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    Client = None

try:
    import psycopg2
    from psycopg2 import pool
    from langchain_community.vectorstores import PGVector
    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False

try:
    from pymongo import MongoClient
    from pymongo.database import Database
    from langchain_community.vectorstores import MongoDBAtlasVectorSearch
    MONGODB_AVAILABLE = True
except ImportError:
    MONGODB_AVAILABLE = False
    MongoClient = None

load_dotenv()

logger = logging.getLogger(__name__)


class DatabaseType(Enum):
    """Tipos de banco de dados suportados."""
    SUPABASE = "supabase"
    NEON = "neon"
    MONGODB = "mongodb"
    NEO4J = "neo4j"  # Mantido para compatibilidade


@dataclass
class DatabaseConfig:
    """Configuração de conexão com banco de dados."""
    db_type: DatabaseType
    name: str
    uri: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None
    database: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    api_key: Optional[str] = None
    project_id: Optional[str] = None
    connection_string: Optional[str] = None
    enabled: bool = True
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte configuração para dicionário."""
        return {
            "db_type": self.db_type.value,
            "name": self.name,
            "uri": self.uri,
            "host": self.host,
            "port": self.port,
            "database": self.database,
            "username": self.username,
            "password": "***" if self.password else None,
            "api_key": "***" if self.api_key else None,
            "project_id": self.project_id,
            "connection_string": "***" if self.connection_string else None,
            "enabled": self.enabled,
            "metadata": self.metadata
        }


@dataclass
class QueryResult:
    """Resultado de uma query."""
    success: bool
    data: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None
    rows_affected: int = 0
    execution_time: float = 0.0


class DatabaseManager:
    """
    Gerenciador unificado de bancos de dados.
    
    Suporta:
    - Supabase (PostgreSQL com recursos adicionais)
    - Neon (PostgreSQL serverless)
    - MongoDB (NoSQL)
    - Neo4j (Graph database - mantido para compatibilidade)
    """
    
    def __init__(self):
        """Inicializa o gerenciador de bancos de dados."""
        self.configs: Dict[str, DatabaseConfig] = {}
        self.connections: Dict[str, Any] = {}
        self._load_default_configs()
        logger.info("DatabaseManager inicializado")
    
    def _load_default_configs(self) -> None:
        """Carrega configurações padrão do ambiente."""
        # Supabase
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        if supabase_url and supabase_key:
            self.add_database(DatabaseConfig(
                db_type=DatabaseType.SUPABASE,
                name="default_supabase",
                uri=supabase_url,
                api_key=supabase_key,
                metadata={"service_role_key": os.getenv("SUPABASE_SERVICE_ROLE_KEY")}
            ))
        
        # Neon
        neon_connection_string = os.getenv("NEON_DATABASE_URL")
        if neon_connection_string:
            self.add_database(DatabaseConfig(
                db_type=DatabaseType.NEON,
                name="default_neon",
                connection_string=neon_connection_string,
                metadata={"project_id": os.getenv("NEON_PROJECT_ID")}
            ))
        
        # MongoDB
        mongodb_uri = os.getenv("MONGODB_URI")
        if mongodb_uri:
            self.add_database(DatabaseConfig(
                db_type=DatabaseType.MONGODB,
                name="default_mongodb",
                uri=mongodb_uri,
                database=os.getenv("MONGODB_DATABASE", "default"),
                metadata={"atlas": os.getenv("MONGODB_ATLAS", "false") == "true"}
            ))
    
    def add_database(self, config: DatabaseConfig) -> bool:
        """
        Adiciona uma configuração de banco de dados.
        
        Args:
            config: Configuração do banco de dados
            
        Returns:
            True se adicionado com sucesso
        """
        try:
            self.configs[config.name] = config
            logger.info(f"Configuração de banco '{config.name}' adicionada ({config.db_type.value})")
            return True
        except Exception as e:
            logger.error(f"Erro ao adicionar configuração de banco: {e}")
            return False
    
    def remove_database(self, name: str) -> bool:
        """
        Remove uma configuração de banco de dados.
        
        Args:
            name: Nome da configuração
            
        Returns:
            True se removido com sucesso
        """
        try:
            if name in self.configs:
                # Fecha conexão se existir
                if name in self.connections:
                    self._close_connection(name)
                del self.configs[name]
                logger.info(f"Configuração de banco '{name}' removida")
                return True
            return False
        except Exception as e:
            logger.error(f"Erro ao remover configuração de banco: {e}")
            return False
    
    def get_database(self, name: str) -> Optional[DatabaseConfig]:
        """Retorna configuração de banco de dados."""
        return self.configs.get(name)
    
    def list_databases(self) -> List[Dict[str, Any]]:
        """Lista todas as configurações de bancos de dados."""
        return [config.to_dict() for config in self.configs.values()]
    
    def connect(self, name: str) -> bool:
        """
        Conecta a um banco de dados.
        
        Args:
            name: Nome da configuração
            
        Returns:
            True se conectado com sucesso
        """
        if name not in self.configs:
            logger.error(f"Configuração de banco '{name}' não encontrada")
            return False
        
        config = self.configs[name]
        
        if not config.enabled:
            logger.warning(f"Banco '{name}' está desabilitado")
            return False
        
        try:
            if config.db_type == DatabaseType.SUPABASE:
                if not SUPABASE_AVAILABLE:
                    logger.error("Supabase não está disponível (biblioteca não instalada)")
                    return False
                client = create_client(config.uri, config.api_key)
                self.connections[name] = client
                logger.info(f"Conectado ao Supabase: {name}")
                return True
            
            elif config.db_type == DatabaseType.NEON:
                if not PSYCOPG2_AVAILABLE:
                    logger.error("Neon não está disponível (psycopg2 não instalado)")
                    return False
                conn = psycopg2.connect(config.connection_string)
                self.connections[name] = conn
                logger.info(f"Conectado ao Neon: {name}")
                return True
            
            elif config.db_type == DatabaseType.MONGODB:
                if not MONGODB_AVAILABLE:
                    logger.error("MongoDB não está disponível (pymongo não instalado)")
                    return False
                client = MongoClient(config.uri)
                db = client[config.database]
                self.connections[name] = {"client": client, "database": db}
                logger.info(f"Conectado ao MongoDB: {name}")
                return True
            
            else:
                logger.error(f"Tipo de banco não suportado: {config.db_type}")
                return False
        
        except Exception as e:
            logger.error(f"Erro ao conectar ao banco '{name}': {e}")
            return False
    
    def _close_connection(self, name: str) -> None:
        """Fecha conexão com banco de dados."""
        if name not in self.connections:
            return
        
        try:
            connection = self.connections[name]
            config = self.configs[name]
            
            if config.db_type == DatabaseType.NEON:
                if connection:
                    connection.close()
            elif config.db_type == DatabaseType.MONGODB:
                if isinstance(connection, dict) and "client" in connection:
                    connection["client"].close()
            
            del self.connections[name]
            logger.info(f"Conexão com '{name}' fechada")
        except Exception as e:
            logger.error(f"Erro ao fechar conexão com '{name}': {e}")
    
    def disconnect(self, name: str) -> bool:
        """
        Desconecta de um banco de dados.
        
        Args:
            name: Nome da configuração
            
        Returns:
            True se desconectado com sucesso
        """
        try:
            self._close_connection(name)
            return True
        except Exception as e:
            logger.error(f"Erro ao desconectar do banco '{name}': {e}")
            return False
    
    def execute_query(self, name: str, query: str, parameters: Optional[Dict[str, Any]] = None) -> QueryResult:
        """
        Executa uma query no banco de dados.
        
        Args:
            name: Nome da configuração
            query: Query a executar
            parameters: Parâmetros da query
            
        Returns:
            Resultado da query
        """
        import time
        start_time = time.time()
        
        if name not in self.configs:
            return QueryResult(
                success=False,
                error=f"Configuração de banco '{name}' não encontrada"
            )
        
        config = self.configs[name]
        
        # Conecta se necessário
        if name not in self.connections:
            if not self.connect(name):
                return QueryResult(
                    success=False,
                    error=f"Falha ao conectar ao banco '{name}'"
                )
        
        try:
            connection = self.connections[name]
            
            if config.db_type == DatabaseType.SUPABASE:
                return self._execute_supabase_query(connection, query, parameters)
            
            elif config.db_type == DatabaseType.NEON:
                return self._execute_neon_query(connection, query, parameters)
            
            elif config.db_type == DatabaseType.MONGODB:
                return self._execute_mongodb_query(connection, query, parameters)
            
            else:
                return QueryResult(
                    success=False,
                    error=f"Tipo de banco não suportado: {config.db_type}"
                )
        
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"Erro ao executar query no banco '{name}': {e}")
            return QueryResult(
                success=False,
                error=str(e),
                execution_time=execution_time
            )
        finally:
            execution_time = time.time() - start_time
    
    def _execute_supabase_query(self, client: Client, query: str, parameters: Optional[Dict[str, Any]]) -> QueryResult:
        """Executa query no Supabase."""
        import time
        start_time = time.time()
        
        try:
            # Supabase usa RPC ou queries SQL via PostgREST
            # Para queries SQL diretas, precisamos usar a API REST
            if query.strip().upper().startswith("SELECT"):
                # Query SELECT - usar select()
                # Por enquanto, retornamos erro indicando que queries SQL diretas
                # precisam ser feitas via RPC ou REST API
                return QueryResult(
                    success=False,
                    error="Queries SQL diretas no Supabase precisam ser feitas via RPC ou REST API. Use execute_rpc() ou execute_rest()"
                )
            else:
                # Para outras queries, usar RPC
                return QueryResult(
                    success=False,
                    error="Use execute_rpc() para chamadas de função no Supabase"
                )
        except Exception as e:
            execution_time = time.time() - start_time
            return QueryResult(
                success=False,
                error=str(e),
                execution_time=execution_time
            )
    
    def _execute_neon_query(self, conn, query: str, parameters: Optional[Dict[str, Any]]) -> QueryResult:
        """Executa query no Neon (PostgreSQL)."""
        import time
        start_time = time.time()
        
        try:
            cursor = conn.cursor()
            
            if parameters:
                cursor.execute(query, parameters)
            else:
                cursor.execute(query)
            
            # Verifica se é SELECT
            if query.strip().upper().startswith("SELECT"):
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                data = [dict(zip(columns, row)) for row in rows]
                rows_affected = len(data)
            else:
                conn.commit()
                data = None
                rows_affected = cursor.rowcount
            
            cursor.close()
            execution_time = time.time() - start_time
            
            return QueryResult(
                success=True,
                data=data,
                rows_affected=rows_affected,
                execution_time=execution_time
            )
        except Exception as e:
            conn.rollback()
            execution_time = time.time() - start_time
            return QueryResult(
                success=False,
                error=str(e),
                execution_time=execution_time
            )
    
    def _execute_mongodb_query(self, connection: Dict[str, Any], query: str, parameters: Optional[Dict[str, Any]]) -> QueryResult:
        """Executa query no MongoDB."""
        import time
        start_time = time.time()
        
        try:
            db = connection["database"]
            
            # MongoDB não usa SQL, então precisamos converter ou usar operações diretas
            # Por enquanto, retornamos erro indicando que operações MongoDB
            # precisam ser feitas via métodos específicos
            return QueryResult(
                success=False,
                error="Operações MongoDB precisam ser feitas via métodos específicos (insert_one, find, etc.). Use execute_mongodb_operation()"
            )
        except Exception as e:
            execution_time = time.time() - start_time
            return QueryResult(
                success=False,
                error=str(e),
                execution_time=execution_time
            )
    
    def execute_rpc(self, name: str, function_name: str, parameters: Optional[Dict[str, Any]] = None) -> QueryResult:
        """
        Executa função RPC no Supabase.
        
        Args:
            name: Nome da configuração
            function_name: Nome da função
            parameters: Parâmetros da função
            
        Returns:
            Resultado da execução
        """
        import time
        start_time = time.time()
        
        if name not in self.connections:
            if not self.connect(name):
                return QueryResult(
                    success=False,
                    error=f"Falha ao conectar ao banco '{name}'"
                )
        
        config = self.configs[name]
        
        if config.db_type != DatabaseType.SUPABASE:
            return QueryResult(
                success=False,
                error="RPC é suportado apenas no Supabase"
            )
        
        try:
            client = self.connections[name]
            result = client.rpc(function_name, parameters or {}).execute()
            
            execution_time = time.time() - start_time
            
            return QueryResult(
                success=True,
                data=result.data if hasattr(result, 'data') else None,
                execution_time=execution_time
            )
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"Erro ao executar RPC '{function_name}': {e}")
            return QueryResult(
                success=False,
                error=str(e),
                execution_time=execution_time
            )
    
    def execute_mongodb_operation(self, name: str, collection: str, operation: str, 
                                  filter_dict: Optional[Dict[str, Any]] = None,
                                  document: Optional[Dict[str, Any]] = None,
                                  update: Optional[Dict[str, Any]] = None) -> QueryResult:
        """
        Executa operação no MongoDB.
        
        Args:
            name: Nome da configuração
            collection: Nome da coleção
            operation: Tipo de operação (find, insert_one, update_one, delete_one, etc.)
            filter: Filtro para operações
            document: Documento para inserção/atualização
            update: Atualização para operações update
            
        Returns:
            Resultado da operação
        """
        import time
        start_time = time.time()
        
        if name not in self.connections:
            if not self.connect(name):
                return QueryResult(
                    success=False,
                    error=f"Falha ao conectar ao banco '{name}'"
                )
        
        config = self.configs[name]
        
        if config.db_type != DatabaseType.MONGODB:
            return QueryResult(
                success=False,
                error="Operações MongoDB são suportadas apenas em bancos MongoDB"
            )
        
        try:
            db = self.connections[name]["database"]
            coll = db[collection]
            
            if operation == "find":
                cursor = coll.find(filter_dict or {})
                data = list(cursor)
                rows_affected = len(data)
            elif operation == "find_one":
                data = [coll.find_one(filter_dict or {})]
                rows_affected = 1 if data[0] else 0
            elif operation == "insert_one":
                result = coll.insert_one(document or {})
                data = [{"inserted_id": str(result.inserted_id)}]
                rows_affected = 1
            elif operation == "update_one":
                result = coll.update_one(filter_dict or {}, update or {})
                data = [{"matched_count": result.matched_count, "modified_count": result.modified_count}]
                rows_affected = result.modified_count
            elif operation == "delete_one":
                result = coll.delete_one(filter_dict or {})
                data = [{"deleted_count": result.deleted_count}]
                rows_affected = result.deleted_count
            else:
                return QueryResult(
                    success=False,
                    error=f"Operação '{operation}' não suportada"
                )
            
            execution_time = time.time() - start_time
            
            return QueryResult(
                success=True,
                data=data,
                rows_affected=rows_affected,
                execution_time=execution_time
            )
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"Erro ao executar operação MongoDB '{operation}': {e}")
            return QueryResult(
                success=False,
                error=str(e),
                execution_time=execution_time
            )
    
    def get_status(self, name: str) -> Dict[str, Any]:
        """
        Obtém status de um banco de dados.
        
        Args:
            name: Nome da configuração
            
        Returns:
            Status do banco de dados
        """
        if name not in self.configs:
            return {
                "available": False,
                "error": f"Configuração de banco '{name}' não encontrada"
            }
        
        config = self.configs[name]
        is_connected = name in self.connections
        
        status = {
            "name": name,
            "type": config.db_type.value,
            "enabled": config.enabled,
            "connected": is_connected,
            "available": True
        }
        
        # Testa conexão se não estiver conectado
        if not is_connected and config.enabled:
            test_connection = self.connect(name)
            status["connected"] = test_connection
            if not test_connection:
                status["error"] = "Falha ao conectar"
        
        return status
    
    def list_tables(self, name: str) -> List[str]:
        """
        Lista tabelas de um banco de dados.
        
        Args:
            name: Nome da configuração
            
        Returns:
            Lista de tabelas
        """
        if name not in self.configs:
            return []
        
        config = self.configs[name]
        
        try:
            if config.db_type == DatabaseType.SUPABASE:
                # Supabase usa a mesma estrutura do PostgreSQL
                query = """
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                """
                result = self.execute_query(name, query)
                if result.success and result.data:
                    return [row["table_name"] for row in result.data]
            
            elif config.db_type == DatabaseType.NEON:
                query = """
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                """
                result = self.execute_query(name, query)
                if result.success and result.data:
                    return [row["table_name"] for row in result.data]
            
            elif config.db_type == DatabaseType.MONGODB:
                if name in self.connections:
                    db = self.connections[name]["database"]
                    return db.list_collection_names()
        
        except Exception as e:
            logger.error(f"Erro ao listar tabelas: {e}")
        
        return []


# Instância global do gerenciador
_db_manager_instance: Optional[DatabaseManager] = None


def get_db_manager() -> DatabaseManager:
    """Retorna a instância global do gerenciador de bancos de dados."""
    global _db_manager_instance
    if _db_manager_instance is None:
        _db_manager_instance = DatabaseManager()
    return _db_manager_instance

