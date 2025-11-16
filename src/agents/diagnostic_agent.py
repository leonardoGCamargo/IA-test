"""
Agente de Diagnóstico - Detecta erros, faltas de configuração e problemas no sistema.

Este agente analisa o sistema e identifica:
- Variáveis de ambiente faltando
- Chaves de API ausentes
- Senhas não configuradas
- Problemas de conexão
- Dependências faltando
- Configurações incorretas
"""

import os
import logging
from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import importlib.util

load_dotenv()

logger = logging.getLogger(__name__)


class IssueSeverity(Enum):
    """Severidade do problema."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class IssueCategory(Enum):
    """Categoria do problema."""
    ENVIRONMENT = "environment"
    DATABASE = "database"
    API_KEY = "api_key"
    DEPENDENCY = "dependency"
    CONFIGURATION = "configuration"
    CONNECTION = "connection"
    PERMISSION = "permission"
    OTHER = "other"


@dataclass
class DiagnosticIssue:
    """Representa um problema diagnosticado."""
    id: str
    category: IssueCategory
    severity: IssueSeverity
    title: str
    description: str
    details: Dict[str, Any] = field(default_factory=dict)
    affected_components: List[str] = field(default_factory=list)
    detected_at: datetime = field(default_factory=datetime.now)
    resolved: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário."""
        return {
            "id": self.id,
            "category": self.category.value,
            "severity": self.severity.value,
            "title": self.title,
            "description": self.description,
            "details": self.details,
            "affected_components": self.affected_components,
            "detected_at": self.detected_at.isoformat(),
            "resolved": self.resolved
        }


class DiagnosticAgent:
    """
    Agente de diagnóstico que detecta problemas no sistema.
    
    Funcionalidades:
    - Verifica variáveis de ambiente
    - Verifica chaves de API
    - Verifica conexões de banco de dados
    - Verifica dependências instaladas
    - Verifica configurações
    - Detecta problemas de permissão
    """
    
    def __init__(self):
        """Inicializa o agente de diagnóstico."""
        self.issues: List[DiagnosticIssue] = []
        # Tenta encontrar o arquivo .env e env.example
        self.env_file = Path(".env")
        if not self.env_file.exists():
            self.env_file = Path("config/.env")
        self.env_example = Path("config/env.example")
        if not self.env_example.exists():
            self.env_example = Path("env.example")
        logger.info("DiagnosticAgent inicializado")
    
    def run_full_diagnostic(self) -> List[DiagnosticIssue]:
        """
        Executa diagnóstico completo do sistema.
        
        Returns:
            Lista de problemas encontrados
        """
        self.issues = []
        
        # Verifica variáveis de ambiente
        self._check_environment_variables()
        
        # Verifica chaves de API
        self._check_api_keys()
        
        # Verifica bancos de dados
        self._check_databases()
        
        # Verifica dependências
        self._check_dependencies()
        
        # Verifica configurações
        self._check_configurations()
        
        # Verifica conexões
        self._check_connections()
        
        # Verifica permissões
        self._check_permissions()
        
        logger.info(f"Diagnóstico completo: {len(self.issues)} problemas encontrados")
        return self.issues
    
    def _check_environment_variables(self) -> None:
        """Verifica variáveis de ambiente."""
        # Variáveis críticas
        critical_vars = {
            "NEO4J_URI": "URI do Neo4j",
            "NEO4J_USERNAME": "Usuário do Neo4j",
            "NEO4J_PASSWORD": "Senha do Neo4j",
        }
        
        # Variáveis opcionais mas importantes
        important_vars = {
            "OLLAMA_BASE_URL": "URL do Ollama",
            "LLM": "Modelo LLM",
            "EMBEDDING_MODEL": "Modelo de embedding",
        }
        
        # Verifica variáveis críticas
        for var, description in critical_vars.items():
            value = os.getenv(var)
            if not value:
                self.issues.append(DiagnosticIssue(
                    id=f"env_missing_{var.lower()}",
                    category=IssueCategory.ENVIRONMENT,
                    severity=IssueSeverity.CRITICAL,
                    title=f"Variável de ambiente faltando: {var}",
                    description=f"A variável de ambiente {var} ({description}) não está configurada.",
                    details={
                        "variable": var,
                        "description": description,
                        "required": True
                    },
                    affected_components=["Neo4j", "Database"]
                ))
        
        # Verifica variáveis importantes
        for var, description in important_vars.items():
            value = os.getenv(var)
            if not value:
                self.issues.append(DiagnosticIssue(
                    id=f"env_missing_{var.lower()}",
                    category=IssueCategory.ENVIRONMENT,
                    severity=IssueSeverity.HIGH,
                    title=f"Variável de ambiente faltando: {var}",
                    description=f"A variável de ambiente {var} ({description}) não está configurada.",
                    details={
                        "variable": var,
                        "description": description,
                        "required": False
                    },
                    affected_components=["LLM", "Embeddings"]
                ))
        
        # Verifica se arquivo .env existe
        if not self.env_file.exists():
            self.issues.append(DiagnosticIssue(
                id="env_file_missing",
                category=IssueCategory.ENVIRONMENT,
                severity=IssueSeverity.HIGH,
                title="Arquivo .env não encontrado",
                description="O arquivo .env não foi encontrado. Crie um arquivo .env baseado no env.example.",
                details={
                    "env_file": str(self.env_file),
                    "env_example": str(self.env_example)
                },
                affected_components=["All"]
            ))
    
    def _check_api_keys(self) -> None:
        """Verifica chaves de API."""
        api_keys = {
            "OPENAI_API_KEY": {
                "description": "Chave da API do OpenAI",
                "required_for": ["OpenAI LLM", "OpenAI Embeddings"],
                "severity": IssueSeverity.MEDIUM
            },
            "GOOGLE_API_KEY": {
                "description": "Chave da API do Google",
                "required_for": ["Google GenAI Embeddings"],
                "severity": IssueSeverity.MEDIUM
            },
            "AWS_ACCESS_KEY_ID": {
                "description": "Chave de acesso AWS",
                "required_for": ["AWS Bedrock"],
                "severity": IssueSeverity.MEDIUM
            },
            "AWS_SECRET_ACCESS_KEY": {
                "description": "Chave secreta AWS",
                "required_for": ["AWS Bedrock"],
                "severity": IssueSeverity.MEDIUM
            },
            "SUPABASE_KEY": {
                "description": "Chave do Supabase",
                "required_for": ["Supabase Database"],
                "severity": IssueSeverity.MEDIUM
            },
            "LANGCHAIN_API_KEY": {
                "description": "Chave da API do LangChain",
                "required_for": ["LangChain Tracing"],
                "severity": IssueSeverity.LOW
            },
        }
        
        for key, info in api_keys.items():
            value = os.getenv(key)
            if not value or value == "":
                # Verifica se é realmente necessário
                llm = os.getenv("LLM", "")
                embedding_model = os.getenv("EMBEDDING_MODEL", "")
                
                is_required = False
                if "OPENAI" in key and ("gpt" in llm.lower() or "openai" in embedding_model.lower()):
                    is_required = True
                elif "GOOGLE" in key and "google" in embedding_model.lower():
                    is_required = True
                elif "AWS" in key and "aws" in llm.lower() or "aws" in embedding_model.lower():
                    is_required = True
                elif "SUPABASE" in key:
                    # Verifica se Supabase está configurado
                    if os.getenv("SUPABASE_URL"):
                        is_required = True
                
                severity = IssueSeverity.CRITICAL if is_required else info["severity"]
                
                self.issues.append(DiagnosticIssue(
                    id=f"api_key_missing_{key.lower()}",
                    category=IssueCategory.API_KEY,
                    severity=severity,
                    title=f"Chave de API faltando: {key}",
                    description=f"A chave de API {key} ({info['description']}) não está configurada.",
                    details={
                        "api_key": key,
                        "description": info["description"],
                        "required_for": info["required_for"],
                        "is_required": is_required
                    },
                    affected_components=info["required_for"]
                ))
    
    def _check_databases(self) -> None:
        """Verifica configurações de bancos de dados."""
        # Neo4j
        neo4j_uri = os.getenv("NEO4J_URI")
        neo4j_username = os.getenv("NEO4J_USERNAME")
        neo4j_password = os.getenv("NEO4J_PASSWORD")
        
        if neo4j_uri and neo4j_username and neo4j_password:
            # Tenta conectar
            try:
                from langchain_neo4j import Neo4jGraph
                graph = Neo4jGraph(
                    url=neo4j_uri,
                    username=neo4j_username,
                    password=neo4j_password,
                    refresh_schema=False
                )
                # Testa conexão
                graph.query("RETURN 1")
            except Exception as e:
                self.issues.append(DiagnosticIssue(
                    id="neo4j_connection_failed",
                    category=IssueCategory.CONNECTION,
                    severity=IssueSeverity.CRITICAL,
                    title="Falha na conexão com Neo4j",
                    description=f"Não foi possível conectar ao Neo4j: {str(e)}",
                    details={
                        "uri": neo4j_uri,
                        "error": str(e)
                    },
                    affected_components=["Neo4j", "GraphRAG"]
                ))
        
        # Supabase
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        
        if supabase_url and not supabase_key:
            self.issues.append(DiagnosticIssue(
                id="supabase_key_missing",
                category=IssueCategory.DATABASE,
                severity=IssueSeverity.HIGH,
                title="Chave do Supabase faltando",
                description="A URL do Supabase está configurada, mas a chave de API não está configurada.",
                details={
                    "url": supabase_url
                },
                affected_components=["Supabase"]
            ))
        
        # Neon
        neon_url = os.getenv("NEON_DATABASE_URL")
        if neon_url:
            try:
                import psycopg2
                conn = psycopg2.connect(neon_url)
                conn.close()
            except ImportError:
                self.issues.append(DiagnosticIssue(
                    id="neon_dependency_missing",
                    category=IssueCategory.DEPENDENCY,
                    severity=IssueSeverity.HIGH,
                    title="Dependência do Neon faltando",
                    description="A biblioteca psycopg2 não está instalada. Instale com: pip install psycopg2-binary",
                    details={
                        "dependency": "psycopg2-binary"
                    },
                    affected_components=["Neon"]
                ))
            except Exception as e:
                self.issues.append(DiagnosticIssue(
                    id="neon_connection_failed",
                    category=IssueCategory.CONNECTION,
                    severity=IssueSeverity.HIGH,
                    title="Falha na conexão com Neon",
                    description=f"Não foi possível conectar ao Neon: {str(e)}",
                    details={
                        "error": str(e)
                    },
                    affected_components=["Neon"]
                ))
        
        # MongoDB
        mongodb_uri = os.getenv("MONGODB_URI")
        if mongodb_uri:
            try:
                from pymongo import MongoClient
                client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=5000)
                client.server_info()
                client.close()
            except ImportError:
                self.issues.append(DiagnosticIssue(
                    id="mongodb_dependency_missing",
                    category=IssueCategory.DEPENDENCY,
                    severity=IssueSeverity.HIGH,
                    title="Dependência do MongoDB faltando",
                    description="A biblioteca pymongo não está instalada. Instale com: pip install pymongo",
                    details={
                        "dependency": "pymongo"
                    },
                    affected_components=["MongoDB"]
                ))
            except Exception as e:
                self.issues.append(DiagnosticIssue(
                    id="mongodb_connection_failed",
                    category=IssueCategory.CONNECTION,
                    severity=IssueSeverity.HIGH,
                    title="Falha na conexão com MongoDB",
                    description=f"Não foi possível conectar ao MongoDB: {str(e)}",
                    details={
                        "error": str(e)
                    },
                    affected_components=["MongoDB"]
                ))
    
    def _check_dependencies(self) -> None:
        """Verifica dependências instaladas."""
        dependencies = {
            "supabase": {
                "package": "supabase",
                "required_for": ["Supabase Database"],
                "severity": IssueSeverity.MEDIUM
            },
            "psycopg2": {
                "package": "psycopg2-binary",
                "required_for": ["Neon Database"],
                "severity": IssueSeverity.MEDIUM
            },
            "pymongo": {
                "package": "pymongo",
                "required_for": ["MongoDB"],
                "severity": IssueSeverity.MEDIUM
            },
            "langchain_neo4j": {
                "package": "langchain-neo4j",
                "required_for": ["Neo4j GraphRAG"],
                "severity": IssueSeverity.CRITICAL
            },
            "langchain_openai": {
                "package": "langchain-openai",
                "required_for": ["OpenAI LLM", "OpenAI Embeddings"],
                "severity": IssueSeverity.MEDIUM
            },
        }
        
        for dep_name, info in dependencies.items():
            try:
                importlib.import_module(dep_name)
            except ImportError:
                # Verifica se é realmente necessário
                is_required = False
                if dep_name == "langchain_neo4j" and os.getenv("NEO4J_URI"):
                    is_required = True
                elif dep_name == "supabase" and os.getenv("SUPABASE_URL"):
                    is_required = True
                elif dep_name == "psycopg2" and os.getenv("NEON_DATABASE_URL"):
                    is_required = True
                elif dep_name == "pymongo" and os.getenv("MONGODB_URI"):
                    is_required = True
                
                severity = IssueSeverity.CRITICAL if is_required else info["severity"]
                
                self.issues.append(DiagnosticIssue(
                    id=f"dependency_missing_{dep_name}",
                    category=IssueCategory.DEPENDENCY,
                    severity=severity,
                    title=f"Dependência faltando: {info['package']}",
                    description=f"A biblioteca {info['package']} não está instalada. Instale com: pip install {info['package']}",
                    details={
                        "package": info["package"],
                        "import_name": dep_name,
                        "install_command": f"pip install {info['package']}"
                    },
                    affected_components=info["required_for"]
                ))
    
    def _check_configurations(self) -> None:
        """Verifica configurações."""
        # Verifica LLM
        llm = os.getenv("LLM", "")
        if not llm:
            self.issues.append(DiagnosticIssue(
                id="llm_not_configured",
                category=IssueCategory.CONFIGURATION,
                severity=IssueSeverity.HIGH,
                title="Modelo LLM não configurado",
                description="O modelo LLM não está configurado. Configure a variável LLM no arquivo .env",
                details={
                    "variable": "LLM",
                    "example_values": ["llama2", "gpt-4", "gpt-3.5"]
                },
                affected_components=["LLM"]
            ))
        
        # Verifica embedding model
        embedding_model = os.getenv("EMBEDDING_MODEL", "")
        if not embedding_model:
            self.issues.append(DiagnosticIssue(
                id="embedding_model_not_configured",
                category=IssueCategory.CONFIGURATION,
                severity=IssueSeverity.HIGH,
                title="Modelo de embedding não configurado",
                description="O modelo de embedding não está configurado. Configure a variável EMBEDDING_MODEL no arquivo .env",
                details={
                    "variable": "EMBEDDING_MODEL",
                    "example_values": ["sentence_transformer", "openai", "ollama"]
                },
                affected_components=["Embeddings"]
            ))
        
        # Verifica Ollama
        ollama_url = os.getenv("OLLAMA_BASE_URL", "")
        if not ollama_url and ("llama" in llm.lower() or "ollama" in embedding_model.lower()):
            self.issues.append(DiagnosticIssue(
                id="ollama_url_not_configured",
                category=IssueCategory.CONFIGURATION,
                severity=IssueSeverity.HIGH,
                title="URL do Ollama não configurada",
                description="A URL do Ollama não está configurada, mas é necessária para o modelo configurado.",
                details={
                    "variable": "OLLAMA_BASE_URL",
                    "default_value": "http://localhost:11434"
                },
                affected_components=["Ollama", "LLM", "Embeddings"]
            ))
    
    def _check_connections(self) -> None:
        """Verifica conexões."""
        # Verifica Ollama
        ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        if ollama_url:
            try:
                try:
                    import requests
                except ImportError:
                    self.issues.append(DiagnosticIssue(
                        id="requests_dependency_missing",
                        category=IssueCategory.DEPENDENCY,
                        severity=IssueSeverity.MEDIUM,
                        title="Dependência faltando: requests",
                        description="A biblioteca requests não está instalada. Instale com: pip install requests",
                        details={
                            "package": "requests",
                            "install_command": "pip install requests"
                        },
                        affected_components=["Ollama"]
                    ))
                    return
                
                response = requests.get(f"{ollama_url}/api/tags", timeout=5)
                if response.status_code != 200:
                    self.issues.append(DiagnosticIssue(
                        id="ollama_not_accessible",
                        category=IssueCategory.CONNECTION,
                        severity=IssueSeverity.HIGH,
                        title="Ollama não acessível",
                        description=f"O Ollama não está acessível em {ollama_url}",
                        details={
                            "url": ollama_url,
                            "status_code": response.status_code
                        },
                        affected_components=["Ollama"]
                    ))
            except Exception as e:
                self.issues.append(DiagnosticIssue(
                    id="ollama_connection_failed",
                    category=IssueCategory.CONNECTION,
                    severity=IssueSeverity.HIGH,
                    title="Falha na conexão com Ollama",
                    description=f"Não foi possível conectar ao Ollama: {str(e)}",
                    details={
                        "url": ollama_url,
                        "error": str(e)
                    },
                    affected_components=["Ollama"]
                ))
    
    def _check_permissions(self) -> None:
        """Verifica permissões."""
        # Verifica se é possível escrever no diretório atual
        try:
            test_file = Path(".test_write_permission")
            test_file.write_text("test")
            test_file.unlink()
        except Exception as e:
            self.issues.append(DiagnosticIssue(
                id="write_permission_denied",
                category=IssueCategory.PERMISSION,
                severity=IssueSeverity.MEDIUM,
                title="Permissão de escrita negada",
                description=f"Não é possível escrever no diretório atual: {str(e)}",
                details={
                    "error": str(e)
                },
                affected_components=["File System"]
            ))
    
    def get_issues_by_severity(self, severity: IssueSeverity) -> List[DiagnosticIssue]:
        """Retorna problemas por severidade."""
        return [issue for issue in self.issues if issue.severity == severity]
    
    def get_issues_by_category(self, category: IssueCategory) -> List[DiagnosticIssue]:
        """Retorna problemas por categoria."""
        return [issue for issue in self.issues if issue.category == category]
    
    def get_critical_issues(self) -> List[DiagnosticIssue]:
        """Retorna apenas problemas críticos."""
        return self.get_issues_by_severity(IssueSeverity.CRITICAL)
    
    def get_summary(self) -> Dict[str, Any]:
        """Retorna resumo do diagnóstico."""
        return {
            "total_issues": len(self.issues),
            "critical": len(self.get_issues_by_severity(IssueSeverity.CRITICAL)),
            "high": len(self.get_issues_by_severity(IssueSeverity.HIGH)),
            "medium": len(self.get_issues_by_severity(IssueSeverity.MEDIUM)),
            "low": len(self.get_issues_by_severity(IssueSeverity.LOW)),
            "info": len(self.get_issues_by_severity(IssueSeverity.INFO)),
            "by_category": {
                category.value: len(self.get_issues_by_category(category))
                for category in IssueCategory
            }
        }


# Instância global do agente
_diagnostic_agent_instance: Optional[DiagnosticAgent] = None


def get_diagnostic_agent() -> DiagnosticAgent:
    """Retorna a instância global do agente de diagnóstico."""
    global _diagnostic_agent_instance
    if _diagnostic_agent_instance is None:
        _diagnostic_agent_instance = DiagnosticAgent()
    return _diagnostic_agent_instance

