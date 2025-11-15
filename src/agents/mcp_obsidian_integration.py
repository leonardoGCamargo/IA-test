"""
Integração com Obsidian para criar e gerenciar notas sobre MCPs e RAGs.
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ObsidianManager:
    """Gerencia notas no Obsidian."""
    
    def __init__(self, vault_path: Optional[str] = None):
        """
        Inicializa o gerenciador Obsidian.
        
        Args:
            vault_path: Caminho para o vault do Obsidian. Se None, tenta detectar automaticamente.
        """
        self.vault_path = self._detect_vault_path(vault_path)
        if not self.vault_path:
            logger.warning("Vault do Obsidian não encontrado. Use set_vault_path() para configurar.")
    
    def _detect_vault_path(self, vault_path: Optional[str]) -> Optional[Path]:
        """Tenta detectar o caminho do vault do Obsidian."""
        if vault_path:
            path = Path(vault_path)
            if path.exists() and path.is_dir():
                return path
            return None
        
        # Locais comuns do Obsidian
        common_paths = [
            Path.home() / "Documents" / "Obsidian",
            Path.home() / "Obsidian",
            Path.home() / ".obsidian",
        ]
        
        for path in common_paths:
            if path.exists() and path.is_dir():
                # Verifica se é um vault (tem pasta .obsidian)
                if (path / ".obsidian").exists():
                    return path
        
        return None
    
    def set_vault_path(self, vault_path: str) -> bool:
        """
        Define o caminho do vault do Obsidian.
        
        Args:
            vault_path: Caminho para o vault
            
        Returns:
            True se o caminho for válido
        """
        if not vault_path:
            return False
        path = Path(vault_path)
        if path.exists() and path.is_dir():
            self.vault_path = path
            logger.info(f"Vault do Obsidian configurado: {path}")
            return True
        logger.warning(f"Caminho do vault inválido: {vault_path}")
        return False
    
    def create_note(self, title: str, content: str, folder: str = "") -> Optional[Path]:
        """
        Cria uma nova nota no Obsidian.
        
        Args:
            title: Título da nota
            content: Conteúdo da nota (Markdown)
            folder: Pasta onde criar a nota (opcional)
            
        Returns:
            Caminho do arquivo criado ou None em caso de erro
        """
        if not self.vault_path:
            logger.error("Vault do Obsidian não configurado")
            return None
        
        # Sanitiza o título para nome de arquivo
        filename = self._sanitize_filename(title) + ".md"
        
        # Define o caminho completo
        if folder:
            note_path = self.vault_path / folder / filename
            note_path.parent.mkdir(parents=True, exist_ok=True)
        else:
            note_path = self.vault_path / filename
        
        try:
            with open(note_path, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"Nota criada: {note_path}")
            return note_path
        except Exception as e:
            logger.error(f"Erro ao criar nota: {e}")
            return None
    
    def _sanitize_filename(self, filename: str) -> str:
        """Sanitiza um nome de arquivo removendo caracteres inválidos."""
        # Remove caracteres inválidos
        filename = re.sub(r'[<>:"/\\|?*]', '', filename)
        # Remove espaços extras
        filename = ' '.join(filename.split())
        return filename
    
    def create_mcp_note(self, mcp_name: str, mcp_info: Dict, related_notes: List[str] = None) -> Optional[Path]:
        """
        Cria uma nota sobre um servidor MCP.
        
        Args:
            mcp_name: Nome do servidor MCP
            mcp_info: Informações do servidor MCP
            related_notes: Lista de nomes de notas relacionadas para criar links
            
        Returns:
            Caminho do arquivo criado
        """
        content = f"""# {mcp_name}

> **Tipo:** Servidor MCP  
> **Criado em:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Informações do Servidor

"""
        
        if mcp_info.get("command"):
            content += f"- **Comando:** `{mcp_info['command']}`\n"
        
        if mcp_info.get("args"):
            content += f"- **Argumentos:** `{' '.join(mcp_info['args'])}`\n"
        
        if mcp_info.get("description"):
            content += f"- **Descrição:** {mcp_info['description']}\n"
        
        if mcp_info.get("enabled") is not None:
            status = "✅ Habilitado" if mcp_info['enabled'] else "❌ Desabilitado"
            content += f"- **Status:** {status}\n"
        
        if mcp_info.get("ports"):
            content += f"\n## Portas\n\n"
            for port in mcp_info['ports']:
                content += f"- `{port}`\n"
        
        if mcp_info.get("resources"):
            content += f"\n## Recursos Disponíveis\n\n"
            for resource in mcp_info['resources']:
                content += f"- **{resource.get('name', 'Recurso sem nome')}**\n"
                if resource.get('description'):
                    content += f"  - {resource['description']}\n"
        
        if mcp_info.get("tools"):
            content += f"\n## Ferramentas Disponíveis\n\n"
            for tool in mcp_info['tools']:
                content += f"- **{tool.get('name', 'Ferramenta sem nome')}**\n"
                if tool.get('description'):
                    content += f"  - {tool['description']}\n"
        
        if related_notes:
            content += f"\n## Notas Relacionadas\n\n"
            for note in related_notes:
                note_link = f"[[{note}]]"
                content += f"- {note_link}\n"
        
        content += f"""

## Tags

#mcp #servidor-mcp

---

*Nota gerada automaticamente pelo Gerenciador de MCP*
"""
        
        return self.create_note(mcp_name, content, folder="MCP")
    
    def create_rag_note(self, rag_name: str, rag_info: Dict, related_mcps: List[str] = None) -> Optional[Path]:
        """
        Cria uma nota sobre RAG (Retrieval-Augmented Generation).
        
        Args:
            rag_name: Nome do sistema RAG
            rag_info: Informações do sistema RAG
            related_mcps: Lista de servidores MCP relacionados
            
        Returns:
            Caminho do arquivo criado
        """
        content = f"""# {rag_name}

> **Tipo:** Sistema RAG (Retrieval-Augmented Generation)  
> **Criado em:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Informações do Sistema

"""
        
        if rag_info.get("description"):
            content += f"{rag_info['description']}\n\n"
        
        if rag_info.get("model"):
            content += f"- **Modelo:** {rag_info['model']}\n"
        
        if rag_info.get("embedding_model"):
            content += f"- **Modelo de Embedding:** {rag_info['embedding_model']}\n"
        
        if rag_info.get("vector_store"):
            content += f"- **Vector Store:** {rag_info['vector_store']}\n"
        
        if rag_info.get("enabled"):
            content += f"- **Status:** ✅ Ativo\n"
        else:
            content += f"- **Status:** ❌ Inativo\n"
        
        if related_mcps:
            content += f"\n## Servidores MCP Relacionados\n\n"
            for mcp in related_mcps:
                mcp_link = f"[[{mcp}]]"
                content += f"- {mcp_link}\n"
        
        if rag_info.get("use_cases"):
            content += f"\n## Casos de Uso\n\n"
            for use_case in rag_info['use_cases']:
                content += f"- {use_case}\n"
        
        content += f"""

## Tags

#rag #retrieval-augmented-generation #ia

---

*Nota gerada automaticamente pelo Gerenciador de MCP*
"""
        
        return self.create_note(rag_name, content, folder="RAG")
    
    def create_connection_note(self, source: str, target: str, connection_type: str = "relacionado") -> Optional[Path]:
        """
        Cria uma nota de conexão entre duas notas.
        
        Args:
            source: Nome da nota origem
            target: Nome da nota destino
            connection_type: Tipo de conexão
            
        Returns:
            Caminho do arquivo criado
        """
        note_name = f"{source} → {target}"
        content = f"""# {note_name}

> **Tipo de Conexão:** {connection_type}  
> **Criado em:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Conexão

[[{source}]] → [[{target}]]

## Descrição

Esta nota documenta a conexão entre [[{source}]] e [[{target}]].

## Tags

#conexão #{connection_type}

---

*Nota gerada automaticamente pelo Gerenciador de MCP*
"""
        
        return self.create_note(note_name, content, folder="Conexões")
    
    def link_notes(self, note1_path: Path, note2_path: Path) -> bool:
        """
        Cria links bidirecionais entre duas notas.
        
        Args:
            note1_path: Caminho da primeira nota
            note2_path: Caminho da segunda nota
            
        Returns:
            True se os links foram criados com sucesso
        """
        try:
            # Lê as notas
            with open(note1_path, 'r', encoding='utf-8') as f:
                content1 = f.read()
            
            with open(note2_path, 'r', encoding='utf-8') as f:
                content2 = f.read()
            
            # Extrai os nomes das notas (sem extensão)
            name1 = note1_path.stem
            name2 = note2_path.stem
            
            # Adiciona links se não existirem
            link1 = f"[[{name2}]]"
            link2 = f"[[{name1}]]"
            
            if link1 not in content1:
                # Adiciona seção de links relacionados se não existir
                if "## Notas Relacionadas" not in content1:
                    content1 += f"\n## Notas Relacionadas\n\n"
                else:
                    content1 += "\n"
                content1 += f"- {link1}\n"
            
            if link2 not in content2:
                if "## Notas Relacionadas" not in content2:
                    content2 += f"\n## Notas Relacionadas\n\n"
                else:
                    content2 += "\n"
                content2 += f"- {link2}\n"
            
            # Salva as notas atualizadas
            with open(note1_path, 'w', encoding='utf-8') as f:
                f.write(content1)
            
            with open(note2_path, 'w', encoding='utf-8') as f:
                f.write(content2)
            
            logger.info(f"Links criados entre {name1} e {name2}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao criar links: {e}")
            return False
    
    def list_notes(self, folder: str = "") -> List[Path]:
        """
        Lista todas as notas em uma pasta.
        
        Args:
            folder: Pasta para listar (vazio para raiz)
            
        Returns:
            Lista de caminhos de notas
        """
        if not self.vault_path:
            return []
        
        if folder:
            notes_path = self.vault_path / folder
        else:
            notes_path = self.vault_path
        
        if not notes_path.exists():
            return []
        
        return list(notes_path.glob("*.md"))
    
    def search_notes(self, query: str, folder: str = "") -> List[Path]:
        """
        Busca notas por conteúdo.
        
        Args:
            query: Termo de busca
            folder: Pasta para buscar (vazio para todas)
            
        Returns:
            Lista de notas que contêm o termo
        """
        notes = self.list_notes(folder)
        matching_notes = []
        
        for note_path in notes:
            try:
                with open(note_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if query.lower() in content.lower():
                        matching_notes.append(note_path)
            except Exception:
                continue
        
        return matching_notes

