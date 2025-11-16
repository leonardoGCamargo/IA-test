"""
Integração com Neo4j para GraphRAG e gerenciamento de grafo de conhecimento.
Conecta MCPs, RAGs e notas do Obsidian em um grafo Neo4j.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import logging
from dotenv import load_dotenv

from langchain_neo4j import Neo4jGraph, Neo4jVector
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langgraph.graph import StateGraph, END
from typing_extensions import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

from src.apps.chains import load_llm, load_embedding_model
from src.agents.mcp_obsidian_integration import ObsidianManager

load_dotenv()

logger = logging.getLogger(__name__)


def add_messages(left: List[BaseMessage], right: List[BaseMessage]) -> List[BaseMessage]:
    """Adiciona mensagens ao estado."""
    return left + right


class GraphState(TypedDict):
    """Estado do grafo para GraphRAG."""
    messages: Annotated[List[BaseMessage], add_messages]
    context: str
    question: str


class Neo4jGraphRAGManager:
    """Gerencia grafo de conhecimento Neo4j e GraphRAG com LangGraph."""
    
    def __init__(
        self,
        neo4j_uri: Optional[str] = None,
        neo4j_username: Optional[str] = None,
        neo4j_password: Optional[str] = None,
        llm_name: Optional[str] = None,
        embedding_model_name: Optional[str] = None
    ):
        """
        Inicializa o gerenciador Neo4j GraphRAG.
        
        Args:
            neo4j_uri: URI de conexão do Neo4j
            neo4j_username: Usuário do Neo4j
            neo4j_password: Senha do Neo4j
            llm_name: Nome do modelo LLM
            embedding_model_name: Nome do modelo de embedding
        """
        # Default URI adapts to Docker environment
        # Check if running in Docker by checking for .dockerenv file or NEO4J_URI env var
        is_docker = os.path.exists("/.dockerenv") or os.getenv("NEO4J_URI", "").startswith("neo4j://database")
        default_uri = "neo4j://database:7687" if is_docker else "neo4j://localhost:7687"
        self.neo4j_uri = neo4j_uri or os.getenv("NEO4J_URI", default_uri)
        self.neo4j_username = neo4j_username or os.getenv("NEO4J_USERNAME", "neo4j")
        self.neo4j_password = neo4j_password or os.getenv("NEO4J_PASSWORD", "password")
        self.llm_name = llm_name or os.getenv("LLM", "llama2")
        self.embedding_model_name = embedding_model_name or os.getenv("EMBEDDING_MODEL", "sentence_transformer")
        
        # Configurações adicionais
        self.ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        
        # Conecta ao Neo4j
        try:
            self.graph = Neo4jGraph(
                url=self.neo4j_uri,
                username=self.neo4j_username,
                password=self.neo4j_password,
                refresh_schema=False
            )
            logger.info("Conectado ao Neo4j com sucesso")
        except Exception as e:
            logger.error(f"Erro ao conectar ao Neo4j: {e}")
            raise
        
        # Carrega modelos
        try:
            self.llm = load_llm(
                self.llm_name,
                logger=logger,
                config={"ollama_base_url": self.ollama_base_url}
            )
            self.embeddings, self.embedding_dimension = load_embedding_model(
                self.embedding_model_name,
                logger=logger,
                config={"ollama_base_url": self.ollama_base_url}
            )
            logger.info(f"Modelos carregados: LLM={self.llm_name}, Embedding={self.embedding_model_name}")
        except Exception as e:
            logger.error(f"Erro ao carregar modelos: {e}")
            raise
        
        # Cria índices e constraints
        self._create_constraints()
        self._create_indexes()
        
        # Inicializa GraphRAG chain
        self.graphrag_chain = None
        self._build_graphrag_chain()
    
    def _create_constraints(self) -> None:
        """Cria constraints no Neo4j."""
        constraints = [
            "CREATE CONSTRAINT mcp_id IF NOT EXISTS FOR (m:MCP) REQUIRE (m.id) IS UNIQUE",
            "CREATE CONSTRAINT rag_id IF NOT EXISTS FOR (r:RAG) REQUIRE (r.id) IS UNIQUE",
            "CREATE CONSTRAINT obsidian_note_id IF NOT EXISTS FOR (n:ObsidianNote) REQUIRE (n.id) IS UNIQUE",
            "CREATE CONSTRAINT tag_name IF NOT EXISTS FOR (t:Tag) REQUIRE (t.name) IS UNIQUE",
        ]
        
        for constraint in constraints:
            try:
                self.graph.query(constraint)
            except Exception as e:
                logger.debug(f"Constraint já existe ou erro: {e}")
    
    def _create_indexes(self) -> None:
        """Cria índices no Neo4j."""
        indexes = [
            f"CREATE VECTOR INDEX mcp_embedding IF NOT EXISTS FOR (m:MCP) ON m.embedding OPTIONS {{indexConfig: {{`vector.dimensions`: {self.embedding_dimension}, `vector.similarity_function`: 'cosine'}}}}",
            f"CREATE VECTOR INDEX rag_embedding IF NOT EXISTS FOR (r:RAG) ON r.embedding OPTIONS {{indexConfig: {{`vector.dimensions`: {self.embedding_dimension}, `vector.similarity_function`: 'cosine'}}}}",
            f"CREATE VECTOR INDEX obsidian_embedding IF NOT EXISTS FOR (n:ObsidianNote) ON n.embedding OPTIONS {{indexConfig: {{`vector.dimensions`: {self.embedding_dimension}, `vector.similarity_function`: 'cosine'}}}}",
        ]
        
        for index in indexes:
            try:
                self.graph.query(index)
            except Exception as e:
                logger.debug(f"Índice já existe ou erro: {e}")
    
    def _build_graphrag_chain(self) -> None:
        """Constrói a chain de GraphRAG usando LangGraph."""
        try:
            # Cria o grafo LangGraph
            workflow = StateGraph(GraphState)
            
            # Adiciona nós
            workflow.add_node("retrieve", self._retrieve_context)
            workflow.add_node("generate", self._generate_answer)
            
            # Define o fluxo
            workflow.set_entry_point("retrieve")
            workflow.add_edge("retrieve", "generate")
            workflow.add_edge("generate", END)
            
            # Compila o grafo
            self.graphrag_chain = workflow.compile()
            logger.info("GraphRAG chain construída com sucesso")
        except Exception as e:
            logger.error(f"Erro ao construir GraphRAG chain: {e}")
            self.graphrag_chain = None
    
    def _retrieve_context(self, state: GraphState) -> GraphState:
        """Recupera contexto do grafo Neo4j."""
        question = state["question"]
        
        # Busca no grafo usando Cypher
        query = """
        MATCH (n)
        WHERE n.description CONTAINS $query 
           OR n.name CONTAINS $query
           OR (n:ObsidianNote AND n.content CONTAINS $query)
        WITH n, 
             CASE 
               WHEN n.description CONTAINS $query THEN 1.0
               WHEN n.name CONTAINS $query THEN 0.8
               ELSE 0.5
             END AS score
        RETURN n, score
        ORDER BY score DESC
        LIMIT 5
        """
        
        try:
            results = self.graph.query(query, {"query": question})
            context_parts = []
            
            for record in results:
                node = record.get("n")
                if node:
                    # Converte Node do Neo4j para dicionário
                    node_dict = dict(node)
                    node_type = list(node.labels)[0] if hasattr(node, 'labels') and node.labels else "Unknown"
                    name = node_dict.get("name", node_dict.get("id", "Unknown"))
                    description = node_dict.get("description", node_dict.get("content", ""))
                    
                    context_parts.append(
                        f"{node_type}: {name}\n{description[:500] if description else 'Sem descrição'}"
                    )
            
            context = "\n\n".join(context_parts) if context_parts else "Nenhum contexto encontrado"
            
            return {
                **state,
                "context": context
            }
        except Exception as e:
            logger.error(f"Erro ao recuperar contexto: {e}")
            return {
                **state,
                "context": "Erro ao recuperar contexto"
            }
    
    def _generate_answer(self, state: GraphState) -> GraphState:
        """Gera resposta usando LLM."""
        question = state["question"]
        context = state.get("context", "")
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Você é um assistente especializado em analisar grafos de conhecimento.
Use o contexto fornecido do grafo Neo4j para responder à pergunta.
Se o contexto não contiver informações suficientes, diga que não tem informações suficientes.

Contexto do grafo:
{context}"""),
            ("human", "{question}")
        ])
        
        try:
            chain = prompt | self.llm | StrOutputParser()
            answer = chain.invoke({"context": context, "question": question})
            
            return {
                **state,
                "messages": state["messages"] + [AIMessage(content=answer)]
            }
        except Exception as e:
            logger.error(f"Erro ao gerar resposta: {e}")
            return {
                **state,
                "messages": state["messages"] + [AIMessage(content="Erro ao gerar resposta.")]
            }
    
    def query_graphrag(self, question: str) -> str:
        """
        Consulta o grafo usando GraphRAG.
        
        Args:
            question: Pergunta a ser respondida
            
        Returns:
            Resposta gerada
        """
        if not self.graphrag_chain:
            return "GraphRAG chain não está disponível"
        
        try:
            initial_state = {
                "messages": [HumanMessage(content=question)],
                "context": "",
                "question": question
            }
            
            result = self.graphrag_chain.invoke(initial_state)
            
            # Extrai a resposta das mensagens
            if result.get("messages"):
                last_message = result["messages"][-1]
                if isinstance(last_message, AIMessage):
                    return last_message.content
            
            return "Não foi possível gerar uma resposta"
        except Exception as e:
            logger.error(f"Erro ao consultar GraphRAG: {e}")
            return f"Erro: {str(e)}"
    
    def create_mcp_node(self, mcp_info: Dict[str, Any]) -> bool:
        """
        Cria um nó MCP no grafo.
        
        Args:
            mcp_info: Informações do MCP
            
        Returns:
            True se criado com sucesso
        """
        try:
            # Gera embedding para descrição
            description = mcp_info.get("description", "")
            if description:
                embedding = self.embeddings.embed_query(description)
            else:
                embedding = [0.0] * self.embedding_dimension
            
            # Prepara dados
            mcp_id = mcp_info.get("id", mcp_info.get("name", ""))
            name = mcp_info.get("name", mcp_id)
            command = mcp_info.get("command", "")
            args = mcp_info.get("args", [])
            enabled = mcp_info.get("enabled", True)
            
            query = """
            MERGE (m:MCP {id: $id})
            SET m.name = $name,
                m.command = $command,
                m.args = $args,
                m.description = $description,
                m.enabled = $enabled,
                m.embedding = $embedding,
                m.created_at = datetime()
            RETURN m
            """
            
            # Converte lista de args para string se necessário
            if isinstance(args, list):
                args = args
            else:
                args = []
            
            self.graph.query(query, {
                "id": mcp_id,
                "name": name,
                "command": command,
                "args": args,
                "description": description,
                "enabled": enabled,
                "embedding": embedding
            })
            
            logger.info(f"Nó MCP '{name}' criado com sucesso")
            return True
        except Exception as e:
            logger.error(f"Erro ao criar nó MCP: {e}")
            return False
    
    def create_rag_node(self, rag_info: Dict[str, Any]) -> bool:
        """
        Cria um nó RAG no grafo.
        
        Args:
            rag_info: Informações do RAG
            
        Returns:
            True se criado com sucesso
        """
        try:
            # Gera embedding para descrição
            description = rag_info.get("description", "")
            if description:
                embedding = self.embeddings.embed_query(description)
            else:
                embedding = [0.0] * self.embedding_dimension
            
            # Prepara dados
            rag_id = rag_info.get("id", rag_info.get("name", ""))
            name = rag_info.get("name", rag_id)
            model = rag_info.get("model", "")
            embedding_model = rag_info.get("embedding_model", "")
            vector_store = rag_info.get("vector_store", "")
            enabled = rag_info.get("enabled", True)
            
            query = """
            MERGE (r:RAG {id: $id})
            SET r.name = $name,
                r.description = $description,
                r.model = $model,
                r.embedding_model = $embedding_model,
                r.vector_store = $vector_store,
                r.enabled = $enabled,
                r.embedding = $embedding,
                r.created_at = datetime()
            RETURN r
            """
            
            self.graph.query(query, {
                "id": rag_id,
                "name": name,
                "description": description,
                "model": model,
                "embedding_model": embedding_model,
                "vector_store": vector_store,
                "enabled": enabled,
                "embedding": embedding
            })
            
            logger.info(f"Nó RAG '{name}' criado com sucesso")
            return True
        except Exception as e:
            logger.error(f"Erro ao criar nó RAG: {e}")
            return False
    
    def create_obsidian_note_node(self, note_path: Path, content: str) -> bool:
        """
        Cria um nó ObsidianNote no grafo.
        
        Args:
            note_path: Caminho do arquivo da nota
            content: Conteúdo da nota
            
        Returns:
            True se criado com sucesso
        """
        try:
            # Gera embedding para conteúdo
            if content:
                embedding = self.embeddings.embed_query(content)
            else:
                embedding = [0.0] * self.embedding_dimension
            
            # Extrai título e metadados
            note_id = note_path.stem
            title = note_path.stem
            folder = note_path.parent.name if note_path.parent.name else "root"
            
            # Extrai tags do conteúdo (formato #tag)
            tags = re.findall(r'#(\w+)', content)
            
            # Extrai links do conteúdo (formato [[link]])
            links = re.findall(r'\[\[([^\]]+)\]\]', content)
            
            query = """
            MERGE (n:ObsidianNote {id: $id})
            ON CREATE SET n.title = $title,
                n.content = $content,
                n.folder = $folder,
                n.path = $path,
                n.embedding = $embedding,
                n.created_at = datetime(),
                n.updated_at = datetime()
            ON MATCH SET n.content = $content,
                n.updated_at = datetime(),
                n.embedding = $embedding
            WITH n
            FOREACH (tagName IN $tags |
                MERGE (t:Tag {name: tagName})
                MERGE (n)-[:TAGGED]->(t)
            )
            RETURN n
            """
            
            self.graph.query(query, {
                "id": note_id,
                "title": title,
                "content": content,
                "folder": folder,
                "path": str(note_path),
                "embedding": embedding,
                "tags": tags
            })
            
            # Cria relações com outras notas mencionadas
            for link in links:
                self._create_note_link(note_id, link)
            
            logger.info(f"Nó ObsidianNote '{title}' criado com sucesso")
            return True
        except Exception as e:
            logger.error(f"Erro ao criar nó ObsidianNote: {e}")
            return False
    
    def _create_note_link(self, source_id: str, target_id: str) -> None:
        """Cria relação entre notas."""
        try:
            query = """
            MATCH (source:ObsidianNote {id: $source_id})
            MATCH (target:ObsidianNote {id: $target_id})
            MERGE (source)-[:LINKS_TO]->(target)
            """
            self.graph.query(query, {
                "source_id": source_id,
                "target_id": target_id
            })
        except Exception as e:
            logger.debug(f"Erro ao criar link entre notas: {e}")
    
    def create_mcp_rag_relation(self, rag_id: str, mcp_id: str, relation_type: str = "USES") -> bool:
        """
        Cria relação entre RAG e MCP.
        
        Args:
            rag_id: ID do RAG
            mcp_id: ID do MCP
            relation_type: Tipo de relação (USES, IMPLEMENTS, DEPENDS_ON, RELATED_TO)
            
        Returns:
            True se criado com sucesso
        """
        try:
            query = f"""
            MATCH (r:RAG {{id: $rag_id}})
            MATCH (m:MCP {{id: $mcp_id}})
            MERGE (r)-[:{relation_type}]->(m)
            RETURN r, m
            """
            self.graph.query(query, {
                "rag_id": rag_id,
                "mcp_id": mcp_id
            })
            logger.info(f"Relação {relation_type} criada entre RAG '{rag_id}' e MCP '{mcp_id}'")
            return True
        except Exception as e:
            logger.error(f"Erro ao criar relação: {e}")
            return False
    
    def create_mcp_obsidian_relation(self, mcp_id: str, note_id: str, relation_type: str = "DOCUMENTED_IN") -> bool:
        """
        Cria relação entre MCP e nota Obsidian.
        
        Args:
            mcp_id: ID do MCP
            note_id: ID da nota Obsidian
            relation_type: Tipo de relação
            
        Returns:
            True se criado com sucesso
        """
        try:
            query = f"""
            MATCH (m:MCP {{id: $mcp_id}})
            MATCH (n:ObsidianNote {{id: $note_id}})
            MERGE (m)-[:{relation_type}]->(n)
            RETURN m, n
            """
            self.graph.query(query, {
                "mcp_id": mcp_id,
                "note_id": note_id
            })
            logger.info(f"Relação {relation_type} criada entre MCP '{mcp_id}' e nota '{note_id}'")
            return True
        except Exception as e:
            logger.error(f"Erro ao criar relação: {e}")
            return False
    
    def import_obsidian_vault(self, vault_path: Path) -> int:
        """
        Importa todas as notas do vault Obsidian para o Neo4j.
        
        Args:
            vault_path: Caminho do vault Obsidian
            
        Returns:
            Número de notas importadas
        """
        imported = 0
        
        if not vault_path.exists():
            logger.error(f"Vault não encontrado: {vault_path}")
            return 0
        
        # Busca todos os arquivos .md
        for md_file in vault_path.rglob("*.md"):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Cria nó da nota
                if self.create_obsidian_note_node(md_file, content):
                    imported += 1
            except Exception as e:
                logger.error(f"Erro ao importar nota {md_file}: {e}")
        
        logger.info(f"{imported} notas importadas do vault Obsidian")
        return imported
    
    def query_graph(self, cypher_query: str, parameters: Optional[Dict] = None) -> List[Dict]:
        """
        Executa uma query Cypher no grafo.
        
        Args:
            cypher_query: Query Cypher
            parameters: Parâmetros da query
            
        Returns:
            Resultados da query
        """
        try:
            results = self.graph.query(cypher_query, parameters or {})
            converted_results = []
            
            for record in results:
                # O Neo4jGraph retorna Record objects que podem ser convertidos para dict
                try:
                    # Tenta converter diretamente para dict
                    converted_record = dict(record)
                    
                    # Converte valores que são Nodes do Neo4j
                    for key, value in converted_record.items():
                        if hasattr(value, 'labels') or (hasattr(value, '__class__') and 'Node' in str(value.__class__)):
                            # É um Node do Neo4j - extrai propriedades
                            if hasattr(value, 'items'):
                                # Se já tem items, é um dict-like
                                converted_record[key] = dict(value)
                            elif hasattr(value, '__dict__'):
                                # Tenta usar __dict__
                                converted_record[key] = {k: v for k, v in value.__dict__.items() if not k.startswith('_')}
                            else:
                                # Tenta acessar diretamente
                                try:
                                    converted_record[key] = {k: getattr(value, k) for k in dir(value) if not k.startswith('_')}
                                except:
                                    converted_record[key] = str(value)
                        elif isinstance(value, list):
                            # Lista de valores
                            converted_record[key] = [
                                dict(v) if (hasattr(v, 'labels') or (hasattr(v, '__class__') and 'Node' in str(v.__class__))) else v
                                for v in value
                            ]
                    
                    converted_results.append(converted_record)
                except Exception as e:
                    # Se falhar, tenta usar get() do Record
                    logger.debug(f"Erro ao converter record: {e}")
                    try:
                        converted_record = {k: record.get(k) for k in record.keys()}
                        converted_results.append(converted_record)
                    except:
                        continue
            
            return converted_results
        except Exception as e:
            logger.error(f"Erro ao executar query: {e}")
            return []
    
    def search_graph(self, query: str, node_types: Optional[List[str]] = None, limit: int = 10) -> List[Dict]:
        """
        Busca no grafo por texto.
        
        Args:
            query: Texto de busca
            node_types: Tipos de nós para buscar (None para todos)
            limit: Limite de resultados
            
        Returns:
            Lista de nós encontrados
        """
        node_filter = ""
        if node_types:
            labels = ":".join(node_types)
            node_filter = f":{labels}"
        
        cypher_query = f"""
        MATCH (n{node_filter})
        WHERE n.name CONTAINS $query 
           OR n.description CONTAINS $query
           OR (n:ObsidianNote AND n.content CONTAINS $query)
        RETURN n, labels(n) as __label__
        LIMIT $limit
        """
        
        results = self.query_graph(cypher_query, {
            "query": query,
            "limit": limit
        })
        
        # Converte resultados para dicionário
        nodes = []
        for record in results:
            node = record.get("n", {})
            node_labels = record.get("__label__", [])
            
            # Se node já é um dicionário, usa diretamente
            if isinstance(node, dict):
                node_dict = node.copy()
                node_dict["__label__"] = node_labels
                nodes.append(node_dict)
            else:
                # Tenta converter Node para dicionário
                try:
                    node_dict = dict(node) if hasattr(node, '__dict__') else {}
                    node_dict["__label__"] = node_labels
                    nodes.append(node_dict)
                except Exception as e:
                    logger.debug(f"Erro ao converter nó: {e}")
                    continue
        
        return nodes
    
    def get_graph_statistics(self) -> Dict[str, int]:
        """
        Obtém estatísticas do grafo.
        
        Returns:
            Dicionário com estatísticas
        """
        stats = {}
        
        queries = {
            "MCP_count": "MATCH (m:MCP) RETURN count(m) as count",
            "RAG_count": "MATCH (r:RAG) RETURN count(r) as count",
            "ObsidianNote_count": "MATCH (n:ObsidianNote) RETURN count(n) as count",
            "Tag_count": "MATCH (t:Tag) RETURN count(t) as count",
            "relation_count": "MATCH ()-[r]->() RETURN count(r) as count"
        }
        
        for key, query in queries.items():
            try:
                results = self.query_graph(query)
                if results:
                    stats[key] = results[0].get("count", 0)
                else:
                    stats[key] = 0
            except Exception as e:
                logger.error(f"Erro ao obter estatística {key}: {e}")
                stats[key] = 0
        
        return stats
    
    def get_graph_visualization_data(self, node_types: Optional[List[str]] = None, limit: int = 50) -> Dict[str, List]:
        """
        Obtém dados para visualização do grafo.
        
        Args:
            node_types: Tipos de nós para incluir (None para todos)
            limit: Limite de nós
            
        Returns:
            Dicionário com nós e arestas
        """
        node_filter = ""
        if node_types:
            labels = ":".join(node_types)
            node_filter = f":{labels}"
        
        # Busca nós
        nodes_query = f"""
        MATCH (n{node_filter})
        RETURN n.id as id, n.name as name, labels(n) as label
        LIMIT $limit
        """
        
        nodes_results = self.query_graph(nodes_query, {"limit": limit})
        
        # Busca relações
        relations_query = f"""
        MATCH (a{node_filter})-[r]->(b{node_filter})
        RETURN a.id as source, b.id as target, type(r) as relation
        LIMIT $limit
        """
        
        relations_results = self.query_graph(relations_query, {"limit": limit})
        
        # Formata nós
        nodes = []
        for record in nodes_results:
            nodes.append({
                "id": record.get("id", ""),
                "name": record.get("name", ""),
                "label": record.get("label", [])
            })
        
        # Formata arestas
        edges = []
        for record in relations_results:
            edges.append({
                "source": record.get("source", ""),
                "target": record.get("target", ""),
                "relation": record.get("relation", "")
            })
        
        return {
            "nodes": nodes,
            "edges": edges
        }


# Instância global do gerenciador
_neo4j_manager_instance: Optional[Neo4jGraphRAGManager] = None


def get_neo4j_manager() -> Neo4jGraphRAGManager:
    """Retorna a instância global do gerenciador Neo4j."""
    global _neo4j_manager_instance
    if _neo4j_manager_instance is None:
        _neo4j_manager_instance = Neo4jGraphRAGManager()
    return _neo4j_manager_instance
