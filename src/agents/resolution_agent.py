"""
Agente de Resolução - Gera soluções e prompts para resolver problemas.

Este agente analisa problemas diagnosticados e gera:
- Descrições de como resolver
- Prompts para ajudar na resolução
- Comandos para executar
- Links para documentação
"""

import os
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from src.agents.diagnostic_agent import DiagnosticIssue, IssueCategory, IssueSeverity

logger = logging.getLogger(__name__)


@dataclass
class Resolution:
    """Representa uma solução para um problema."""
    issue_id: str
    title: str
    description: str
    steps: List[str] = field(default_factory=list)
    commands: List[str] = field(default_factory=list)
    prompts: List[str] = field(default_factory=list)
    documentation_links: List[str] = field(default_factory=list)
    estimated_time: Optional[str] = None
    difficulty: str = "medium"  # easy, medium, hard
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário."""
        return {
            "issue_id": self.issue_id,
            "title": self.title,
            "description": self.description,
            "steps": self.steps,
            "commands": self.commands,
            "prompts": self.prompts,
            "documentation_links": self.documentation_links,
            "estimated_time": self.estimated_time,
            "difficulty": self.difficulty,
            "created_at": self.created_at.isoformat()
        }


class ResolutionAgent:
    """
    Agente de resolução que gera soluções para problemas.
    
    Funcionalidades:
    - Gera descrições de solução
    - Gera prompts para resolução
    - Gera comandos para executar
    - Fornece links para documentação
    """
    
    def __init__(self):
        """Inicializa o agente de resolução."""
        self.resolutions: Dict[str, Resolution] = {}
        logger.info("ResolutionAgent inicializado")
    
    def generate_resolution(self, issue: DiagnosticIssue) -> Resolution:
        """
        Gera uma solução para um problema.
        
        Args:
            issue: Problema diagnosticado
            
        Returns:
            Solução gerada
        """
        if issue.id in self.resolutions:
            return self.resolutions[issue.id]
        
        resolution = self._create_resolution(issue)
        self.resolutions[issue.id] = resolution
        return resolution
    
    def _create_resolution(self, issue: DiagnosticIssue) -> Resolution:
        """Cria uma solução para um problema."""
        if issue.category == IssueCategory.ENVIRONMENT:
            return self._resolve_environment(issue)
        elif issue.category == IssueCategory.API_KEY:
            return self._resolve_api_key(issue)
        elif issue.category == IssueCategory.DATABASE:
            return self._resolve_database(issue)
        elif issue.category == IssueCategory.DEPENDENCY:
            return self._resolve_dependency(issue)
        elif issue.category == IssueCategory.CONFIGURATION:
            return self._resolve_configuration(issue)
        elif issue.category == IssueCategory.CONNECTION:
            return self._resolve_connection(issue)
        elif issue.category == IssueCategory.PERMISSION:
            return self._resolve_permission(issue)
        else:
            return self._resolve_generic(issue)
    
    def _resolve_environment(self, issue: DiagnosticIssue) -> Resolution:
        """Resolve problemas de ambiente."""
        var_name = issue.details.get("variable", "")
        description = issue.details.get("description", "")
        
        resolution = Resolution(
            issue_id=issue.id,
            title=f"Configurar variável de ambiente: {var_name}",
            description=f"Configure a variável de ambiente {var_name} ({description}) no arquivo .env",
            difficulty="easy",
            estimated_time="5 minutos"
        )
        
        if issue.id == "env_file_missing":
            resolution.steps = [
                "1. Verifique se o arquivo env.example existe",
                "2. Copie o arquivo env.example para .env",
                "3. Configure as variáveis necessárias no arquivo .env",
                "4. Verifique se o arquivo .env está no diretório raiz do projeto"
            ]
            resolution.commands = [
                "cp env.example .env",
                "cp config/env.example .env"
            ]
            resolution.prompts = [
                f"Crie um arquivo .env baseado no env.example e configure as variáveis necessárias. "
                f"A variável {var_name} é obrigatória e deve ser configurada."
            ]
        else:
            resolution.steps = [
                f"1. Abra o arquivo .env",
                f"2. Adicione a linha: {var_name}=seu_valor_aqui",
                f"3. Substitua 'seu_valor_aqui' pelo valor apropriado",
                f"4. Salve o arquivo",
                f"5. Reinicie a aplicação se necessário"
            ]
            resolution.commands = [
                f"echo '{var_name}=seu_valor_aqui' >> .env"
            ]
            resolution.prompts = [
                f"Configure a variável de ambiente {var_name} ({description}) no arquivo .env. "
                f"Esta variável é {'obrigatória' if issue.details.get('required', False) else 'opcional'} "
                f"para os seguintes componentes: {', '.join(issue.affected_components)}."
            ]
        
        resolution.documentation_links = [
            "https://docs.python.org/3/library/os.html#os.environ",
            "https://pypi.org/project/python-dotenv/"
        ]
        
        return resolution
    
    def _resolve_api_key(self, issue: DiagnosticIssue) -> Resolution:
        """Resolve problemas de chave de API."""
        api_key = issue.details.get("api_key", "")
        description = issue.details.get("description", "")
        required_for = issue.details.get("required_for", [])
        is_required = issue.details.get("is_required", False)
        
        resolution = Resolution(
            issue_id=issue.id,
            title=f"Obter e configurar chave de API: {api_key}",
            description=f"Obtenha uma chave de API {api_key} ({description}) e configure-a no arquivo .env",
            difficulty="medium",
            estimated_time="10-15 minutos"
        )
        
        if "OPENAI" in api_key:
            resolution.steps = [
                "1. Acesse https://platform.openai.com/api-keys",
                "2. Faça login na sua conta OpenAI",
                "3. Clique em 'Create new secret key'",
                "4. Copie a chave gerada",
                "5. Adicione a chave no arquivo .env: OPENAI_API_KEY=sua_chave_aqui",
                "6. Salve o arquivo"
            ]
            resolution.documentation_links = [
                "https://platform.openai.com/api-keys",
                "https://platform.openai.com/docs/guides/authentication"
            ]
            resolution.prompts = [
                f"Obtenha uma chave de API da OpenAI em https://platform.openai.com/api-keys. "
                f"Esta chave é necessária para usar modelos OpenAI como GPT-4 ou embeddings OpenAI. "
                f"Configure a chave no arquivo .env como: OPENAI_API_KEY=sua_chave_aqui"
            ]
        elif "GOOGLE" in api_key:
            resolution.steps = [
                "1. Acesse https://makersuite.google.com/app/apikey",
                "2. Faça login na sua conta Google",
                "3. Clique em 'Create API Key'",
                "4. Copie a chave gerada",
                "5. Adicione a chave no arquivo .env: GOOGLE_API_KEY=sua_chave_aqui",
                "6. Salve o arquivo"
            ]
            resolution.documentation_links = [
                "https://makersuite.google.com/app/apikey",
                "https://ai.google.dev/docs"
            ]
            resolution.prompts = [
                f"Obtenha uma chave de API do Google em https://makersuite.google.com/app/apikey. "
                f"Esta chave é necessária para usar modelos Google GenAI ou embeddings Google. "
                f"Configure a chave no arquivo .env como: GOOGLE_API_KEY=sua_chave_aqui"
            ]
        elif "AWS" in api_key:
            resolution.steps = [
                "1. Acesse https://aws.amazon.com/",
                "2. Faça login na sua conta AWS",
                "3. Vá para IAM > Users > Security credentials",
                "4. Crie uma nova chave de acesso",
                "5. Copie a Access Key ID e Secret Access Key",
                "6. Adicione as chaves no arquivo .env:",
                "   AWS_ACCESS_KEY_ID=sua_access_key_id",
                "   AWS_SECRET_ACCESS_KEY=sua_secret_access_key",
                "   AWS_DEFAULT_REGION=us-east-1",
                "7. Salve o arquivo"
            ]
            resolution.documentation_links = [
                "https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html",
                "https://aws.amazon.com/bedrock/"
            ]
            resolution.prompts = [
                f"Obtenha credenciais AWS em https://aws.amazon.com/. "
                f"Você precisará criar uma Access Key ID e Secret Access Key no IAM. "
                f"Configure as chaves no arquivo .env como: "
                f"AWS_ACCESS_KEY_ID=sua_access_key_id e AWS_SECRET_ACCESS_KEY=sua_secret_access_key"
            ]
        elif "SUPABASE" in api_key:
            resolution.steps = [
                "1. Acesse https://supabase.com/",
                "2. Faça login na sua conta Supabase",
                "3. Vá para o seu projeto",
                "4. Vá para Settings > API",
                "5. Copie a 'anon public' key",
                "6. Adicione a chave no arquivo .env: SUPABASE_KEY=sua_chave_aqui",
                "7. Salve o arquivo"
            ]
            resolution.documentation_links = [
                "https://supabase.com/docs/guides/api",
                "https://supabase.com/docs/guides/getting-started"
            ]
            resolution.prompts = [
                f"Obtenha uma chave de API do Supabase em https://supabase.com/. "
                f"Você precisará criar um projeto e copiar a 'anon public' key. "
                f"Configure a chave no arquivo .env como: SUPABASE_KEY=sua_chave_aqui"
            ]
        else:
            resolution.steps = [
                f"1. Obtenha uma chave de API para {description}",
                f"2. Adicione a chave no arquivo .env: {api_key}=sua_chave_aqui",
                f"3. Salve o arquivo"
            ]
            resolution.prompts = [
                f"Obtenha uma chave de API para {description} e configure-a no arquivo .env como: {api_key}=sua_chave_aqui"
            ]
        
        if is_required:
            resolution.description += " (OBRIGATÓRIA para os componentes configurados)"
        else:
            resolution.description += " (Opcional, mas recomendada)"
        
        return resolution
    
    def _resolve_database(self, issue: DiagnosticIssue) -> Resolution:
        """Resolve problemas de banco de dados."""
        resolution = Resolution(
            issue_id=issue.id,
            title=issue.title,
            description=issue.description,
            difficulty="medium",
            estimated_time="15-30 minutos"
        )
        
        if "supabase" in issue.id:
            resolution.steps = [
                "1. Acesse https://supabase.com/",
                "2. Crie uma conta ou faça login",
                "3. Crie um novo projeto",
                "4. Copie a URL do projeto e a chave de API",
                "5. Configure no arquivo .env:",
                "   SUPABASE_URL=https://seu-projeto.supabase.co",
                "   SUPABASE_KEY=sua_chave_aqui",
                "6. Salve o arquivo"
            ]
            resolution.documentation_links = [
                "https://supabase.com/docs/guides/getting-started",
                "https://supabase.com/docs/guides/api"
            ]
        elif "neon" in issue.id:
            resolution.steps = [
                "1. Acesse https://neon.tech/",
                "2. Crie uma conta ou faça login",
                "3. Crie um novo projeto",
                "4. Copie a connection string",
                "5. Configure no arquivo .env:",
                "   NEON_DATABASE_URL=postgresql://usuario:senha@host/database",
                "6. Salve o arquivo"
            ]
            resolution.documentation_links = [
                "https://neon.tech/docs",
                "https://neon.tech/docs/connect/connect-from-any-app"
            ]
        elif "mongodb" in issue.id:
            resolution.steps = [
                "1. Acesse https://www.mongodb.com/cloud/atlas",
                "2. Crie uma conta ou faça login",
                "3. Crie um novo cluster",
                "4. Crie um usuário e senha",
                "5. Copie a connection string",
                "6. Configure no arquivo .env:",
                "   MONGODB_URI=mongodb://usuario:senha@host:porta/database",
                "7. Salve o arquivo"
            ]
            resolution.documentation_links = [
                "https://www.mongodb.com/docs/atlas/getting-started/",
                "https://www.mongodb.com/docs/atlas/connect-to-cluster/"
            ]
        
        resolution.prompts = [
            f"Configure o banco de dados conforme descrito acima. "
            f"Certifique-se de que todas as credenciais estão corretas e que o banco de dados está acessível."
        ]
        
        return resolution
    
    def _resolve_dependency(self, issue: DiagnosticIssue) -> Resolution:
        """Resolve problemas de dependência."""
        package = issue.details.get("package", "")
        install_command = issue.details.get("install_command", f"pip install {package}")
        
        resolution = Resolution(
            issue_id=issue.id,
            title=f"Instalar dependência: {package}",
            description=f"Instale a biblioteca {package} usando pip",
            difficulty="easy",
            estimated_time="2-5 minutos"
        )
        
        resolution.steps = [
            f"1. Abra um terminal",
            f"2. Execute o comando: {install_command}",
            f"3. Aguarde a instalação completar",
            f"4. Verifique se a instalação foi bem-sucedida"
        ]
        
        resolution.commands = [
            install_command,
            f"pip show {package}  # Verificar instalação"
        ]
        
        resolution.prompts = [
            f"Instale a biblioteca {package} executando o comando: {install_command}. "
            f"Esta biblioteca é necessária para os seguintes componentes: {', '.join(issue.affected_components)}."
        ]
        
        resolution.documentation_links = [
            f"https://pypi.org/project/{package}/"
        ]
        
        return resolution
    
    def _resolve_configuration(self, issue: DiagnosticIssue) -> Resolution:
        """Resolve problemas de configuração."""
        variable = issue.details.get("variable", "")
        example_values = issue.details.get("example_values", [])
        
        resolution = Resolution(
            issue_id=issue.id,
            title=f"Configurar: {variable}",
            description=f"Configure a variável {variable} no arquivo .env",
            difficulty="easy",
            estimated_time="5 minutos"
        )
        
        resolution.steps = [
            f"1. Abra o arquivo .env",
            f"2. Adicione a linha: {variable}=valor_aqui",
            f"3. Escolha um valor apropriado",
            f"4. Salve o arquivo"
        ]
        
        if example_values:
            resolution.steps.append(f"5. Valores de exemplo: {', '.join(example_values)}")
        
        resolution.commands = [
            f"echo '{variable}=valor_aqui' >> .env"
        ]
        
        resolution.prompts = [
            f"Configure a variável {variable} no arquivo .env. "
            f"Valores de exemplo: {', '.join(example_values) if example_values else 'consulte a documentação'}."
        ]
        
        return resolution
    
    def _resolve_connection(self, issue: DiagnosticIssue) -> Resolution:
        """Resolve problemas de conexão."""
        error = issue.details.get("error", "")
        url = issue.details.get("url", "")
        
        resolution = Resolution(
            issue_id=issue.id,
            title=f"Resolver problema de conexão: {issue.title}",
            description=f"Verifique a conexão e as configurações: {error}",
            difficulty="medium",
            estimated_time="10-20 minutos"
        )
        
        if "neo4j" in issue.id:
            resolution.steps = [
                "1. Verifique se o Neo4j está em execução",
                "2. Verifique se a URI está correta (neo4j://localhost:7687 ou neo4j://database:7687)",
                "3. Verifique se o usuário e senha estão corretos",
                "4. Teste a conexão manualmente",
                "5. Verifique se há firewalls bloqueando a conexão"
            ]
            resolution.commands = [
                "docker ps | grep neo4j  # Verificar se Neo4j está rodando",
                "curl http://localhost:7474  # Testar conexão"
            ]
        elif "ollama" in issue.id:
            resolution.steps = [
                "1. Verifique se o Ollama está em execução",
                "2. Verifique se a URL está correta (http://localhost:11434)",
                "3. Teste a conexão: curl http://localhost:11434/api/tags",
                "4. Verifique se há firewalls bloqueando a conexão",
                "5. Reinicie o Ollama se necessário"
            ]
            resolution.commands = [
                "ollama serve  # Iniciar Ollama",
                "curl http://localhost:11434/api/tags  # Testar conexão"
            ]
        else:
            resolution.steps = [
                "1. Verifique se o serviço está em execução",
                "2. Verifique se a URL/URI está correta",
                "3. Verifique se as credenciais estão corretas",
                "4. Teste a conexão manualmente",
                "5. Verifique se há firewalls bloqueando a conexão"
            ]
        
        resolution.prompts = [
            f"Resolva o problema de conexão verificando: "
            f"1. Se o serviço está em execução, "
            f"2. Se a URL/URI está correta ({url}), "
            f"3. Se as credenciais estão corretas, "
            f"4. Se há firewalls bloqueando a conexão. "
            f"Erro: {error}"
        ]
        
        return resolution
    
    def _resolve_permission(self, issue: DiagnosticIssue) -> Resolution:
        """Resolve problemas de permissão."""
        resolution = Resolution(
            issue_id=issue.id,
            title="Resolver problema de permissão",
            description="Verifique as permissões do diretório e arquivos",
            difficulty="medium",
            estimated_time="5-10 minutos"
        )
        
        resolution.steps = [
            "1. Verifique as permissões do diretório atual",
            "2. Verifique se você tem permissão de escrita",
            "3. Altere as permissões se necessário",
            "4. Verifique se o usuário atual tem acesso"
        ]
        
        resolution.commands = [
            "ls -la  # Verificar permissões",
            "chmod 755 .  # Dar permissão de escrita",
            "whoami  # Verificar usuário atual"
        ]
        
        resolution.prompts = [
            "Resolva o problema de permissão verificando as permissões do diretório e arquivos. "
            "Certifique-se de que você tem permissão de escrita no diretório atual."
        ]
        
        return resolution
    
    def _resolve_generic(self, issue: DiagnosticIssue) -> Resolution:
        """Resolve problemas genéricos."""
        return Resolution(
            issue_id=issue.id,
            title=issue.title,
            description=issue.description,
            difficulty="medium",
            estimated_time="10-15 minutos",
            steps=[
                "1. Analise o problema descrito",
                "2. Consulte a documentação",
                "3. Verifique as configurações",
                "4. Teste a solução",
                "5. Verifique se o problema foi resolvido"
            ],
            prompts=[
                f"Resolva o problema: {issue.description}. "
                f"Analise o problema e encontre uma solução apropriada."
            ]
        )
    
    def generate_resolutions(self, issues: List[DiagnosticIssue]) -> List[Resolution]:
        """
        Gera soluções para uma lista de problemas.
        
        Args:
            issues: Lista de problemas
            
        Returns:
            Lista de soluções
        """
        return [self.generate_resolution(issue) for issue in issues]
    
    def get_resolution(self, issue_id: str) -> Optional[Resolution]:
        """Retorna uma solução por ID."""
        return self.resolutions.get(issue_id)
    
    def get_all_resolutions(self) -> List[Resolution]:
        """Retorna todas as soluções."""
        return list(self.resolutions.values())


# Instância global do agente
_resolution_agent_instance: Optional[ResolutionAgent] = None


def get_resolution_agent() -> ResolutionAgent:
    """Retorna a instância global do agente de resolução."""
    global _resolution_agent_instance
    if _resolution_agent_instance is None:
        _resolution_agent_instance = ResolutionAgent()
    return _resolution_agent_instance

