"""
Módulo Git Integration - Gerenciamento de Git e GitHub.

Este módulo fornece integração com Git e GitHub para:
- Gerenciamento de repositórios
- Commits automáticos
- Push para GitHub
- Criação de branches
- Gestão de tags
- Integração com Pull Requests
"""

from typing import Dict, List, Optional, Any
import subprocess
import logging
import os
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
import json

logger = logging.getLogger(__name__)


class GitAction(Enum):
    """Ações disponíveis do Git."""
    STATUS = "status"
    ADD = "add"
    COMMIT = "commit"
    PUSH = "push"
    PULL = "pull"
    BRANCH = "branch"
    CHECKOUT = "checkout"
    TAG = "tag"
    LOG = "log"
    DIFF = "diff"
    REMOTE = "remote"
    CLONE = "clone"
    CREATE_BRANCH = "create_branch"
    DELETE_BRANCH = "delete_branch"
    MERGE = "merge"
    REBASE = "rebase"


@dataclass
class GitStatus:
    """Status do repositório Git."""
    branch: str
    is_clean: bool
    untracked_files: List[str]
    modified_files: List[str]
    deleted_files: List[str]
    staged_files: List[str]
    ahead: int
    behind: int


@dataclass
class CommitInfo:
    """Informações de um commit."""
    hash: str
    message: str
    author: str
    date: str
    files_changed: int


class GitIntegrationAgent:
    """Agente para integração com Git e GitHub."""
    
    def __init__(self, repo_path: Optional[str] = None):
        """
        Inicializa o agente Git.
        
        Args:
            repo_path: Caminho do repositório (default: diretório atual)
        """
        self.repo_path = Path(repo_path) if repo_path else Path.cwd()
        self.git_path = self.repo_path / ".git"
        
        if not self.git_path.exists():
            logger.warning(f"Repositório Git não encontrado em {self.repo_path}")
        
        logger.info(f"Git Integration Agent inicializado em {self.repo_path}")
    
    def _run_git_command(self, command: List[str], check: bool = True) -> tuple[str, str, int]:
        """
        Executa um comando Git.
        
        Args:
            command: Lista com comando e argumentos
            check: Se True, lança exceção em caso de erro
            
        Returns:
            Tuple (stdout, stderr, return_code)
        """
        try:
            result = subprocess.run(
                ["git"] + command,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=check
            )
            return result.stdout.strip(), result.stderr.strip(), result.returncode
        except subprocess.CalledProcessError as e:
            logger.error(f"Erro ao executar comando Git: {' '.join(command)}")
            logger.error(f"Erro: {e.stderr}")
            if check:
                raise
            return e.stdout.strip(), e.stderr.strip(), e.returncode
    
    def get_status(self) -> GitStatus:
        """Obtém o status do repositório."""
        stdout, _, _ = self._run_git_command(["status", "--porcelain"], check=False)
        stdout_branch, _, _ = self._run_git_command(["branch", "--show-current"], check=False)
        stdout_ahead, _, _ = self._run_git_command(["rev-list", "--count", "HEAD..@{u}"], check=False)
        stdout_behind, _, _ = self._run_git_command(["rev-list", "--count", "@{u}..HEAD"], check=False)
        
        branch = stdout_branch.strip() if stdout_branch else "unknown"
        ahead = int(stdout_ahead.strip()) if stdout_ahead.strip() else 0
        behind = int(stdout_behind.strip()) if stdout_behind.strip() else 0
        
        untracked = []
        modified = []
        deleted = []
        staged = []
        
        for line in stdout.split('\n'):
            if not line.strip():
                continue
            status = line[:2]
            file = line[3:]
            
            if status == '??':
                untracked.append(file)
            elif status.startswith('D'):
                deleted.append(file)
            elif status[0] in ['M', 'A', 'R']:
                staged.append(file)
            elif status[1] in ['M', 'D']:
                modified.append(file)
        
        is_clean = len(untracked) == 0 and len(modified) == 0 and len(deleted) == 0 and len(staged) == 0
        
        return GitStatus(
            branch=branch,
            is_clean=is_clean,
            untracked_files=untracked,
            modified_files=modified,
            deleted_files=deleted,
            staged_files=staged,
            ahead=ahead,
            behind=behind
        )
    
    def add_files(self, files: Optional[List[str]] = None, all_files: bool = False) -> bool:
        """
        Adiciona arquivos ao staging.
        
        Args:
            files: Lista de arquivos para adicionar
            all_files: Se True, adiciona todos os arquivos
        """
        if all_files:
            _, _, return_code = self._run_git_command(["add", "-A"])
        elif files:
            _, _, return_code = self._run_git_command(["add"] + files)
        else:
            logger.warning("Nenhum arquivo especificado para adicionar")
            return False
        
        return return_code == 0
    
    def commit(self, message: str, author: Optional[str] = None) -> bool:
        """
        Cria um commit.
        
        Args:
            message: Mensagem do commit
            author: Autor do commit (formato: "Nome <email>")
        """
        cmd = ["commit", "-m", message]
        if author:
            cmd.extend(["--author", author])
        
        _, stderr, return_code = self._run_git_command(cmd, check=False)
        
        if return_code == 0:
            logger.info(f"Commit criado: {message}")
            return True
        else:
            if "nothing to commit" in stderr.lower():
                logger.info("Nada para commitar")
            else:
                logger.error(f"Erro ao criar commit: {stderr}")
            return False
    
    def push(self, remote: str = "origin", branch: Optional[str] = None, force: bool = False) -> bool:
        """
        Faz push para o repositório remoto.
        
        Args:
            remote: Nome do remote (default: origin)
            branch: Nome da branch (default: branch atual)
            force: Se True, força o push
        """
        cmd = ["push"]
        if force:
            cmd.append("--force")
        if branch:
            cmd.extend([remote, branch])
        else:
            status = self.get_status()
            cmd.extend([remote, status.branch])
        
        _, stderr, return_code = self._run_git_command(cmd, check=False)
        
        if return_code == 0:
            logger.info(f"Push realizado para {remote}/{branch or 'current'}")
            return True
        else:
            logger.error(f"Erro ao fazer push: {stderr}")
            return False
    
    def pull(self, remote: str = "origin", branch: Optional[str] = None) -> bool:
        """
        Faz pull do repositório remoto.
        
        Args:
            remote: Nome do remote
            branch: Nome da branch
        """
        cmd = ["pull", remote]
        if branch:
            cmd.append(branch)
        
        _, stderr, return_code = self._run_git_command(cmd, check=False)
        
        if return_code == 0:
            logger.info(f"Pull realizado de {remote}/{branch or 'current'}")
            return True
        else:
            logger.error(f"Erro ao fazer pull: {stderr}")
            return False
    
    def create_branch(self, branch_name: str, checkout: bool = True) -> bool:
        """
        Cria uma nova branch.
        
        Args:
            branch_name: Nome da branch
            checkout: Se True, faz checkout da branch
        """
        cmd = ["checkout", "-b", branch_name] if checkout else ["branch", branch_name]
        _, stderr, return_code = self._run_git_command(cmd, check=False)
        
        if return_code == 0:
            logger.info(f"Branch '{branch_name}' criada")
            return True
        else:
            logger.error(f"Erro ao criar branch: {stderr}")
            return False
    
    def checkout(self, branch_name: str) -> bool:
        """Faz checkout de uma branch."""
        _, stderr, return_code = self._run_git_command(["checkout", branch_name], check=False)
        
        if return_code == 0:
            logger.info(f"Checkout realizado para '{branch_name}'")
            return True
        else:
            logger.error(f"Erro ao fazer checkout: {stderr}")
            return False
    
    def get_remotes(self) -> Dict[str, str]:
        """Obtém lista de remotes."""
        stdout, _, _ = self._run_git_command(["remote", "-v"], check=False)
        remotes = {}
        
        for line in stdout.split('\n'):
            if not line.strip():
                continue
            parts = line.split()
            if len(parts) >= 2:
                name = parts[0]
                url = parts[1]
                remotes[name] = url
        
        return remotes
    
    def get_recent_commits(self, limit: int = 10) -> List[CommitInfo]:
        """Obtém commits recentes."""
        format_str = "%H|%s|%an|%ad"
        stdout, _, _ = self._run_git_command(
            ["log", f"-{limit}", f"--format={format_str}", "--date=short"],
            check=False
        )
        
        commits = []
        for line in stdout.split('\n'):
            if not line.strip():
                continue
            parts = line.split('|')
            if len(parts) >= 4:
                commits.append(CommitInfo(
                    hash=parts[0][:8],
                    message=parts[1],
                    author=parts[2],
                    date=parts[3]
                ))
        
        return commits
    
    def tag(self, tag_name: str, message: Optional[str] = None, push: bool = False) -> bool:
        """
        Cria uma tag.
        
        Args:
            tag_name: Nome da tag
            message: Mensagem da tag
            push: Se True, faz push da tag
        """
        cmd = ["tag"]
        if message:
            cmd.extend(["-a", tag_name, "-m", message])
        else:
            cmd.append(tag_name)
        
        _, stderr, return_code = self._run_git_command(cmd, check=False)
        
        if return_code == 0:
            logger.info(f"Tag '{tag_name}' criada")
            if push:
                self._run_git_command(["push", "origin", tag_name], check=False)
            return True
        else:
            logger.error(f"Erro ao criar tag: {stderr}")
            return False
    
    def execute_action(self, action: str, parameters: Dict[str, Any]) -> Any:
        """
        Executa uma ação do Git.
        
        Args:
            action: Nome da ação
            parameters: Parâmetros da ação
            
        Returns:
            Resultado da ação
        """
        try:
            if action == "status":
                return self.get_status().__dict__
            
            elif action == "add":
                files = parameters.get("files")
                all_files = parameters.get("all_files", False)
                return self.add_files(files, all_files)
            
            elif action == "commit":
                message = parameters.get("message", "Auto commit")
                author = parameters.get("author")
                return self.commit(message, author)
            
            elif action == "push":
                remote = parameters.get("remote", "origin")
                branch = parameters.get("branch")
                force = parameters.get("force", False)
                return self.push(remote, branch, force)
            
            elif action == "pull":
                remote = parameters.get("remote", "origin")
                branch = parameters.get("branch")
                return self.pull(remote, branch)
            
            elif action == "create_branch":
                branch_name = parameters.get("branch_name")
                checkout = parameters.get("checkout", True)
                return self.create_branch(branch_name, checkout)
            
            elif action == "checkout":
                branch_name = parameters.get("branch_name")
                return self.checkout(branch_name)
            
            elif action == "remotes":
                return self.get_remotes()
            
            elif action == "recent_commits":
                limit = parameters.get("limit", 10)
                commits = self.get_recent_commits(limit)
                return [commit.__dict__ for commit in commits]
            
            elif action == "tag":
                tag_name = parameters.get("tag_name")
                message = parameters.get("message")
                push = parameters.get("push", False)
                return self.tag(tag_name, message, push)
            
            elif action == "full_sync":
                # Faz add, commit e push em uma operação
                status = self.get_status()
                if not status.is_clean:
                    self.add_files(all_files=True)
                    message = parameters.get("message", "Auto commit: atualizações do sistema")
                    if self.commit(message):
                        return self.push(parameters.get("remote", "origin"))
                return True
            
            else:
                raise ValueError(f"Ação não suportada: {action}")
        
        except Exception as e:
            logger.error(f"Erro ao executar ação '{action}': {e}", exc_info=True)
            raise


# Singleton
_git_agent_instance: Optional[GitIntegrationAgent] = None

def get_git_agent(repo_path: Optional[str] = None) -> GitIntegrationAgent:
    """Retorna instância global do Git Agent."""
    global _git_agent_instance
    if _git_agent_instance is None:
        _git_agent_instance = GitIntegrationAgent(repo_path)
    return _git_agent_instance

