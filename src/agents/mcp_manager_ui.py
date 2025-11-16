"""
Interface Streamlit para gerenciar servidores MCP (Model Context Protocol)
"""

import streamlit as st
import asyncio
from src.agents.mcp_manager import MCPManager, MCPServer, get_mcp_manager
from src.agents.mcp_docker_integration import DockerMCPDetector
from src.agents.mcp_obsidian_integration import ObsidianManager
from typing import Optional, Dict
import os
import json

# Importação do Neo4j com tratamento de erro
try:
    from src.agents.mcp_neo4j_integration import Neo4jGraphRAGManager, get_neo4j_manager
    NEO4J_AVAILABLE = True
except ImportError as e:
    NEO4J_AVAILABLE = False
    # Não mostra warning aqui, será mostrado na página específica

# Importação do pyvis para visualização do grafo
try:
    from pyvis.network import Network
    import tempfile
    PYVIS_AVAILABLE = True
except ImportError:
    PYVIS_AVAILABLE = False
    # Não mostra warning aqui, será mostrado na página específica

st.set_page_config(
    page_title="Gerenciador de MCP",
    page_icon="🔌",
    layout="wide"
)

# Inicializa os gerenciadores
manager = get_mcp_manager()
docker_detector = DockerMCPDetector()
obsidian_manager = ObsidianManager()

# Função para obter o gerenciador Neo4j (lazy loading)
def get_neo4j_manager_safe():
    """Obtém o gerenciador Neo4j com tratamento de erro."""
    if not NEO4J_AVAILABLE:
        return None, False
    try:
        return get_neo4j_manager(), True
    except Exception as e:
        return None, False


def create_graph_visualization(graph_data: Dict, height: str = "600px") -> str:
    """
    Cria visualização do grafo usando pyvis.
    
    Args:
        graph_data: Dados do grafo (nós e arestas)
        height: Altura da visualização
        
    Returns:
        Caminho do arquivo HTML gerado
    """
    if not PYVIS_AVAILABLE:
        return None
    
    try:
        # Cria rede
        net = Network(height=height, width="100%", bgcolor="#222222", font_color="white")
        net.set_options("""
        {
            "nodes": {
                "font": {
                    "size": 14
                },
                "scaling": {
                    "min": 10,
                    "max": 30
                }
            },
            "edges": {
                "arrows": {
                    "to": {
                        "enabled": true
                    }
                },
                "smooth": {
                    "type": "continuous"
                }
            },
            "physics": {
                "enabled": true,
                "stabilization": {
                    "iterations": 100
                }
            }
        }
        """)
        
        # Adiciona nós
        node_colors = {
            "MCP": "#4A90E2",
            "RAG": "#50C878",
            "ObsidianNote": "#FF6B6B",
            "Tag": "#FFA500"
        }
        
        for node in graph_data.get("nodes", []):
            node_id = node.get("id", "")
            node_name = node.get("name", node_id)
            node_labels = node.get("label", [])
            
            # Determina cor baseada no tipo
            color = "#808080"  # Cinza padrão
            for label in node_labels:
                if label in node_colors:
                    color = node_colors[label]
                    break
            
            net.add_node(
                node_id,
                label=node_name,
                color=color,
                title=node_name
            )
        
        # Adiciona arestas
        for edge in graph_data.get("edges", []):
            source = edge.get("source", "")
            target = edge.get("target", "")
            relation = edge.get("relation", "")
            
            if source and target:
                net.add_edge(
                    source,
                    target,
                    label=relation,
                    title=relation
                )
        
        # Salva em arquivo temporário
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html", mode="w", encoding="utf-8") as f:
            net.save_graph(f.name)
            return f.name
    except Exception as e:
        st.error(f"Erro ao criar visualização: {e}")
        return None


def run_async(coro):
    """Executa uma corrotina assíncrona."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)


st.title("🔌 Gerenciador de MCP")
st.markdown("Gerencie servidores MCP (Model Context Protocol) e seus recursos")

# Sidebar para navegação
st.sidebar.title("Navegação")
page = st.sidebar.radio(
    "Páginas",
    ["Servidores", "Adicionar Servidor", "Recursos e Ferramentas", "Docker Integration", "Obsidian Integration", "Neo4j GraphRAG"]
)

# Configuração do Obsidian na sidebar
st.sidebar.divider()
st.sidebar.subheader("⚙️ Configurações")
obsidian_vault = st.sidebar.text_input(
    "Caminho do Vault Obsidian",
    value=os.getenv("OBSIDIAN_VAULT_PATH", ""),
    help="Caminho completo para o vault do Obsidian"
)
if obsidian_vault and obsidian_vault != obsidian_manager.vault_path:
    if obsidian_manager.set_vault_path(obsidian_vault):
        st.sidebar.success("✅ Vault configurado!")
    else:
        st.sidebar.error("❌ Caminho inválido")

if page == "Servidores":
    st.header("📋 Servidores Configurados")
    
    servers = manager.list_servers()
    
    if not servers:
        st.info("Nenhum servidor configurado. Adicione um servidor na página 'Adicionar Servidor'.")
    else:
        # Estatísticas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total de Servidores", len(servers))
        with col2:
            enabled_count = len(manager.list_enabled_servers())
            st.metric("Servidores Habilitados", enabled_count)
        with col3:
            disabled_count = len(servers) - enabled_count
            st.metric("Servidores Desabilitados", disabled_count)
        
        st.divider()
        
        # Lista de servidores
        for server in servers:
            with st.expander(f"{'✅' if server.enabled else '❌'} {server.name}", expanded=False):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**Comando:** `{server.command}`")
                    st.write(f"**Argumentos:** `{' '.join(server.args)}`")
                    if server.description:
                        st.write(f"**Descrição:** {server.description}")
                    if server.env:
                        st.write(f"**Variáveis de Ambiente:** {len(server.env)} definidas")
                
                with col2:
                    if server.enabled:
                        if st.button("Desabilitar", key=f"disable_{server.name}"):
                            manager.disable_server(server.name)
                            st.rerun()
                    else:
                        if st.button("Habilitar", key=f"enable_{server.name}"):
                            manager.enable_server(server.name)
                            st.rerun()
                    
                    if st.button("Verificar Saúde", key=f"health_{server.name}"):
                        with st.spinner("Verificando servidor..."):
                            health = run_async(manager.check_server_health(server.name))
                            if health["status"] == "available":
                                st.success("✅ Servidor disponível")
                            elif health["status"] == "disabled":
                                st.warning("⚠️ Servidor desabilitado")
                            elif health["status"] == "error":
                                st.error(f"❌ Erro: {health.get('error', 'Desconhecido')}")
                            else:
                                st.info(f"ℹ️ Status: {health['status']}")
                    
                    if st.button("Remover", key=f"remove_{server.name}", type="secondary"):
                        if manager.remove_server(server.name):
                            st.success(f"Servidor '{server.name}' removido")
                            st.rerun()
                        else:
                            st.error("Erro ao remover servidor")

elif page == "Adicionar Servidor":
    st.header("➕ Adicionar Novo Servidor MCP")
    
    with st.form("add_server_form"):
        name = st.text_input("Nome do Servidor *", placeholder="ex: filesystem")
        command = st.text_input("Comando *", placeholder="ex: npx, python, node")
        args_input = st.text_area(
            "Argumentos (um por linha) *",
            placeholder="ex:\n-y\n@modelcontextprotocol/server-filesystem\n/path/to/directory",
            help="Digite cada argumento em uma linha separada"
        )
        description = st.text_input("Descrição", placeholder="Descrição opcional do servidor")
        
        # Variáveis de ambiente
        st.subheader("Variáveis de Ambiente (Opcional)")
        env_vars = {}
        env_count = st.number_input("Número de variáveis de ambiente", min_value=0, max_value=10, value=0)
        for i in range(env_count):
            col1, col2 = st.columns(2)
            with col1:
                env_key = st.text_input(f"Chave {i+1}", key=f"env_key_{i}")
            with col2:
                env_value = st.text_input(f"Valor {i+1}", key=f"env_value_{i}", type="default")
            if env_key:
                env_vars[env_key] = env_value
        
        enabled = st.checkbox("Habilitar servidor", value=True)
        
        submitted = st.form_submit_button("Adicionar Servidor", type="primary")
        
        if submitted:
            if not name or not command or not args_input:
                st.error("Por favor, preencha todos os campos obrigatórios (*)")
            elif name in manager.servers:
                st.error(f"Já existe um servidor com o nome '{name}'")
            else:
                args = [arg.strip() for arg in args_input.split('\n') if arg.strip()]
                server = MCPServer(
                    name=name,
                    command=command,
                    args=args,
                    env=env_vars if env_vars else None,
                    enabled=enabled,
                    description=description if description else None
                )
                
                if manager.add_server(server):
                    st.success(f"✅ Servidor '{name}' adicionado com sucesso!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("Erro ao adicionar servidor")

elif page == "Recursos e Ferramentas":
    st.header("🛠️ Recursos e Ferramentas")
    
    enabled_servers = manager.list_enabled_servers()
    
    if not enabled_servers:
        st.warning("Nenhum servidor habilitado. Habilite servidores na página 'Servidores'.")
    else:
        selected_server = st.selectbox(
            "Selecione um servidor",
            [None] + [s.name for s in enabled_servers],
            format_func=lambda x: "Todos os servidores" if x is None else x
        )
        
        tab1, tab2 = st.tabs(["📦 Recursos", "🔧 Ferramentas"])
        
        with tab1:
            st.subheader("Recursos Disponíveis")
            resources = manager.list_resources(selected_server)
            
            if not resources:
                st.info("Nenhum recurso disponível")
            else:
                for server_name, resource_list in resources.items():
                    st.write(f"### Servidor: {server_name}")
                    for resource in resource_list:
                        with st.expander(f"📄 {resource.get('name', 'Recurso sem nome')}"):
                            st.write(f"**URI:** `{resource.get('uri', 'N/A')}`")
                            st.write(f"**Descrição:** {resource.get('description', 'Sem descrição')}")
                            st.write(f"**Tipo MIME:** {resource.get('mimeType', 'N/A')}")
        
        with tab2:
            st.subheader("Ferramentas Disponíveis")
            tools = manager.list_tools(selected_server)
            
            if not tools:
                st.info("Nenhuma ferramenta disponível")
            else:
                for server_name, tool_list in tools.items():
                    st.write(f"### Servidor: {server_name}")
                    for tool in tool_list:
                        with st.expander(f"🔧 {tool.get('name', 'Ferramenta sem nome')}"):
                            st.write(f"**Descrição:** {tool.get('description', 'Sem descrição')}")
                            input_schema = tool.get('inputSchema', {})
                            if input_schema:
                                st.write("**Parâmetros:**")
                                properties = input_schema.get('properties', {})
                                for param_name, param_info in properties.items():
                                    param_type = param_info.get('type', 'N/A')
                                    param_desc = param_info.get('description', 'Sem descrição')
                                    st.write(f"- `{param_name}` ({param_type}): {param_desc}")

elif page == "Docker Integration":
    st.header("🐳 Integração com Docker")
    st.markdown("Detecta e gerencia servidores MCP em execução no Docker")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Atualizar Lista de Containers", type="primary"):
            st.rerun()
    
    with col2:
        if st.button("🔍 Detectar Servidores MCP"):
            detected = docker_detector.detect_mcp_services()
            if detected:
                st.success(f"✅ {len(detected)} servidor(es) MCP detectado(s)")
            else:
                st.info("ℹ️ Nenhum servidor MCP detectado")
    
    st.divider()
    
    # Lista de containers em execução
    st.subheader("📦 Containers Docker em Execução")
    containers = docker_detector.list_running_containers()
    
    if not containers:
        st.warning("Nenhum container Docker em execução encontrado")
    else:
        st.metric("Total de Containers", len(containers))
        
        # Filtro
        filter_text = st.text_input("🔍 Filtrar containers", placeholder="Digite para filtrar...")
        
        filtered_containers = containers
        if filter_text:
            filtered_containers = [
                c for c in containers
                if filter_text.lower() in c.name.lower() or filter_text.lower() in (c.image or "").lower()
            ]
        
        for container in filtered_containers:
            with st.expander(f"🐳 {container.name} - {container.status}", expanded=False):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**Imagem:** `{container.image or 'N/A'}`")
                    st.write(f"**Status:** {container.status}")
                    if container.ports:
                        st.write("**Portas:**")
                        for port in container.ports:
                            st.code(port)
                    if container.container_id:
                        st.write(f"**ID:** `{container.container_id[:12]}`")
                
                with col2:
                    if st.button("📋 Ver Detalhes", key=f"details_{container.name}"):
                        info = docker_detector.get_service_info(container.name)
                        if info:
                            st.json(info)
                    
                    # Botão para criar nota no Obsidian
                    if obsidian_manager.vault_path:
                        if st.button("📝 Criar Nota Obsidian", key=f"obsidian_{container.name}"):
                            mcp_info = {
                                "command": "docker",
                                "args": ["exec", "-it", container.name],
                                "description": f"Container Docker: {container.name}",
                                "enabled": "running" in container.status.lower(),
                                "ports": container.ports,
                                "image": container.image
                            }
                            note_path = obsidian_manager.create_mcp_note(
                                container.name,
                                mcp_info
                            )
                            if note_path:
                                st.success(f"✅ Nota criada: {note_path.name}")
                            else:
                                st.error("❌ Erro ao criar nota")
    
    st.divider()
    
    # Serviços do docker-compose
    st.subheader("📋 Serviços do Docker Compose")
    if st.button("Listar Serviços do Compose"):
        services = docker_detector.list_compose_services()
        if services:
            st.write("Serviços encontrados:")
            for service in services:
                st.write(f"- `{service}`")
        else:
            st.info("Nenhum serviço encontrado ou docker-compose.yml não encontrado")

elif page == "Obsidian Integration":
    st.header("📝 Integração com Obsidian")
    st.markdown("Crie e gerencie notas sobre MCPs e RAGs no Obsidian")
    
    if not obsidian_manager.vault_path:
        st.warning("⚠️ Vault do Obsidian não configurado. Configure na sidebar.")
        st.info("💡 Dica: Defina o caminho do vault do Obsidian na barra lateral")
    else:
        st.success(f"✅ Vault configurado: `{obsidian_manager.vault_path}`")
        
        st.divider()
        
        # Criar nota sobre MCP
        st.subheader("➕ Criar Nota sobre MCP")
        with st.form("create_mcp_note"):
            mcp_name = st.text_input("Nome do Servidor MCP *")
            mcp_command = st.text_input("Comando")
            mcp_args = st.text_area("Argumentos (um por linha)")
            mcp_description = st.text_area("Descrição")
            mcp_enabled = st.checkbox("Habilitado", value=True)
            
            # Selecionar MCPs relacionados
            all_servers = manager.list_servers()
            related_mcps = st.multiselect(
                "MCPs Relacionados",
                [s.name for s in all_servers],
                help="Selecione servidores MCP relacionados para criar links"
            )
            
            submitted = st.form_submit_button("📝 Criar Nota", type="primary")
            
            if submitted:
                if not mcp_name:
                    st.error("Por favor, informe o nome do servidor MCP")
                else:
                    mcp_info = {
                        "command": mcp_command if mcp_command else None,
                        "args": [a.strip() for a in mcp_args.split('\n') if a.strip()] if mcp_args else [],
                        "description": mcp_description if mcp_description else None,
                        "enabled": mcp_enabled
                    }
                    
                    note_path = obsidian_manager.create_mcp_note(
                        mcp_name,
                        mcp_info,
                        related_notes=related_mcps
                    )
                    
                    if note_path:
                        st.success(f"✅ Nota criada com sucesso: `{note_path.name}`")
                        st.balloons()
                    else:
                        st.error("❌ Erro ao criar nota")
        
        st.divider()
        
        # Criar nota sobre RAG
        st.subheader("➕ Criar Nota sobre RAG")
        with st.form("create_rag_note"):
            rag_name = st.text_input("Nome do Sistema RAG *")
            rag_description = st.text_area("Descrição")
            rag_model = st.text_input("Modelo LLM")
            rag_embedding = st.text_input("Modelo de Embedding")
            rag_vector_store = st.text_input("Vector Store")
            rag_enabled = st.checkbox("Sistema Ativo", value=True)
            
            use_cases = st.text_area(
                "Casos de Uso (um por linha)",
                help="Liste os casos de uso do sistema RAG"
            )
            
            # Selecionar MCPs relacionados
            all_servers = manager.list_servers()
            related_mcps = st.multiselect(
                "MCPs Relacionados",
                [s.name for s in all_servers],
                help="Selecione servidores MCP relacionados"
            )
            
            submitted = st.form_submit_button("📝 Criar Nota RAG", type="primary")
            
            if submitted:
                if not rag_name:
                    st.error("Por favor, informe o nome do sistema RAG")
                else:
                    rag_info = {
                        "description": rag_description if rag_description else None,
                        "model": rag_model if rag_model else None,
                        "embedding_model": rag_embedding if rag_embedding else None,
                        "vector_store": rag_vector_store if rag_vector_store else None,
                        "enabled": rag_enabled,
                        "use_cases": [uc.strip() for uc in use_cases.split('\n') if uc.strip()] if use_cases else []
                    }
                    
                    note_path = obsidian_manager.create_rag_note(
                        rag_name,
                        rag_info,
                        related_mcps=related_mcps
                    )
                    
                    if note_path:
                        st.success(f"✅ Nota RAG criada com sucesso: `{note_path.name}`")
                        st.balloons()
                    else:
                        st.error("❌ Erro ao criar nota")
        
        st.divider()
        
        # Conectar notas
        st.subheader("🔗 Conectar Notas")
        st.markdown("Crie links entre notas existentes")
        
        # Lista notas disponíveis
        mcp_notes = obsidian_manager.list_notes("MCP")
        rag_notes = obsidian_manager.list_notes("RAG")
        all_notes = mcp_notes + rag_notes
        
        if all_notes:
            col1, col2 = st.columns(2)
            
            with col1:
                note1_name = st.selectbox(
                    "Nota Origem",
                    [n.stem for n in all_notes],
                    key="note1"
                )
            
            with col2:
                note2_name = st.selectbox(
                    "Nota Destino",
                    [n.stem for n in all_notes],
                    key="note2"
                )
            
            connection_type = st.selectbox(
                "Tipo de Conexão",
                ["relacionado", "usa", "implementa", "depende", "similar"]
            )
            
            if st.button("🔗 Criar Conexão", type="primary"):
                if note1_name == note2_name:
                    st.error("❌ Selecione notas diferentes")
                else:
                    note1_path = next((n for n in all_notes if n.stem == note1_name), None)
                    note2_path = next((n for n in all_notes if n.stem == note2_name), None)
                    
                    if note1_path and note2_path:
                        if obsidian_manager.link_notes(note1_path, note2_path):
                            st.success("✅ Notas conectadas com sucesso!")
                            # Cria nota de conexão
                            obsidian_manager.create_connection_note(
                                note1_name,
                                note2_name,
                                connection_type
                            )
                        else:
                            st.error("❌ Erro ao conectar notas")
        else:
            st.info("ℹ️ Nenhuma nota encontrada. Crie notas primeiro.")
        
        st.divider()
        
        # Buscar notas
        st.subheader("🔍 Buscar Notas")
        search_query = st.text_input("Buscar por conteúdo", placeholder="Digite o termo de busca...")
        
        if search_query:
            matching_notes = obsidian_manager.search_notes(search_query)
            if matching_notes:
                st.write(f"**{len(matching_notes)} nota(s) encontrada(s):**")
                for note_path in matching_notes:
                    st.write(f"- `{note_path.name}` (em `{note_path.parent.name}`)")

elif page == "Neo4j GraphRAG":
    st.header("📊 Neo4j GraphRAG")
    st.markdown("Gerencie o grafo de conhecimento Neo4j e consulte com GraphRAG usando LangGraph")
    
    # Obtém o gerenciador Neo4j
    neo4j_manager, neo4j_available = get_neo4j_manager_safe()
    
    if not neo4j_available:
        st.error("⚠️ Neo4j não está disponível. Verifique a conexão e as variáveis de ambiente.")
        st.info("💡 Configure `NEO4J_URI`, `NEO4J_USERNAME` e `NEO4J_PASSWORD` no arquivo `.env`")
    else:
        st.success("✅ Conectado ao Neo4j")
        
        # Estatísticas do grafo
        st.subheader("📈 Estatísticas do Grafo")
        col1, col2, col3, col4 = st.columns(4)
        
        try:
            stats = neo4j_manager.get_graph_statistics()
            with col1:
                st.metric("MCPs", stats.get("MCP_count", 0))
            with col2:
                st.metric("RAGs", stats.get("RAG_count", 0))
            with col3:
                st.metric("Notas Obsidian", stats.get("ObsidianNote_count", 0))
            with col4:
                st.metric("Relações", stats.get("relation_count", 0))
        except Exception as e:
            st.error(f"Erro ao obter estatísticas: {e}")
        
        st.divider()
        
        # Tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🔄 Importar para Neo4j",
            "➕ Criar Nós",
            "🔍 Consultar GraphRAG",
            "📊 Visualizar Grafo",
            "🔎 Buscar no Grafo"
        ])
        
        with tab1:
            st.subheader("🔄 Importar Dados para Neo4j")
            
            # Importar MCPs
            st.markdown("### Importar MCPs")
            if st.button("📥 Importar Todos os MCPs"):
                servers = manager.list_servers()
                imported = 0
                for server in servers:
                    mcp_info = {
                        "name": server.name,
                        "id": server.name,
                        "command": server.command,
                        "args": server.args,
                        "description": server.description or "",
                        "enabled": server.enabled
                    }
                    if neo4j_manager.create_mcp_node(mcp_info):
                        imported += 1
                st.success(f"✅ {imported} MCP(s) importado(s) para o Neo4j")
            
            # Importar notas do Obsidian
            st.markdown("### Importar Notas do Obsidian")
            if obsidian_manager.vault_path:
                st.info(f"Vault configurado: `{obsidian_manager.vault_path}`")
                if st.button("📥 Importar Todas as Notas do Obsidian"):
                    with st.spinner("Importando notas..."):
                        imported = neo4j_manager.import_obsidian_vault(obsidian_manager.vault_path)
                        st.success(f"✅ {imported} nota(s) importada(s) para o Neo4j")
            else:
                st.warning("⚠️ Vault do Obsidian não configurado. Configure na sidebar.")
        
        with tab2:
            st.subheader("➕ Criar Nós no Grafo")
            
            # Criar nó MCP
            st.markdown("### Criar Nó MCP")
            with st.form("create_mcp_node_form"):
                mcp_name = st.text_input("Nome do MCP *")
                mcp_command = st.text_input("Comando")
                mcp_args = st.text_area("Argumentos (um por linha)")
                mcp_description = st.text_area("Descrição")
                mcp_enabled = st.checkbox("Habilitado", value=True)
                
                submitted = st.form_submit_button("➕ Criar Nó MCP")
                if submitted:
                    if not mcp_name:
                        st.error("Por favor, informe o nome do MCP")
                    else:
                        mcp_info = {
                            "name": mcp_name,
                            "id": mcp_name,
                            "command": mcp_command if mcp_command else "",
                            "args": [a.strip() for a in mcp_args.split('\n') if a.strip()] if mcp_args else [],
                            "description": mcp_description if mcp_description else "",
                            "enabled": mcp_enabled
                        }
                        if neo4j_manager.create_mcp_node(mcp_info):
                            st.success(f"✅ Nó MCP '{mcp_name}' criado com sucesso!")
                        else:
                            st.error("❌ Erro ao criar nó MCP")
            
            st.divider()
            
            # Criar nó RAG
            st.markdown("### Criar Nó RAG")
            with st.form("create_rag_node_form"):
                rag_name = st.text_input("Nome do RAG *")
                rag_description = st.text_area("Descrição")
                rag_model = st.text_input("Modelo LLM")
                rag_embedding = st.text_input("Modelo de Embedding")
                rag_vector_store = st.text_input("Vector Store")
                rag_enabled = st.checkbox("Sistema Ativo", value=True)
                
                submitted = st.form_submit_button("➕ Criar Nó RAG")
                if submitted:
                    if not rag_name:
                        st.error("Por favor, informe o nome do RAG")
                    else:
                        rag_info = {
                            "name": rag_name,
                            "id": rag_name,
                            "description": rag_description if rag_description else "",
                            "model": rag_model if rag_model else "",
                            "embedding_model": rag_embedding if rag_embedding else "",
                            "vector_store": rag_vector_store if rag_vector_store else "",
                            "enabled": rag_enabled
                        }
                        if neo4j_manager.create_rag_node(rag_info):
                            st.success(f"✅ Nó RAG '{rag_name}' criado com sucesso!")
                        else:
                            st.error("❌ Erro ao criar nó RAG")
            
            st.divider()
            
            # Criar relação MCP-RAG
            st.markdown("### Criar Relação MCP-RAG")
            with st.form("create_mcp_rag_relation_form"):
                # Busca MCPs e RAGs existentes
                mcp_query = "MATCH (m:MCP) RETURN m.id as id, m.name as name ORDER BY m.name"
                rag_query = "MATCH (r:RAG) RETURN r.id as id, r.name as name ORDER BY r.name"
                
                mcps = neo4j_manager.query_graph(mcp_query)
                rags = neo4j_manager.query_graph(rag_query)
                
                if mcps and rags:
                    mcp_options = [m["id"] for m in mcps]
                    rag_options = [r["id"] for r in rags]
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        selected_mcp = st.selectbox("MCP", mcp_options)
                    with col2:
                        selected_rag = st.selectbox("RAG", rag_options)
                    
                    relation_type = st.selectbox(
                        "Tipo de Relação",
                        ["USES", "IMPLEMENTS", "DEPENDS_ON", "RELATED_TO"]
                    )
                    
                    submitted = st.form_submit_button("🔗 Criar Relação")
                    if submitted:
                        if neo4j_manager.create_mcp_rag_relation(selected_rag, selected_mcp, relation_type):
                            st.success(f"✅ Relação {relation_type} criada entre RAG '{selected_rag}' e MCP '{selected_mcp}'")
                        else:
                            st.error("❌ Erro ao criar relação")
                else:
                    st.info("ℹ️ Crie MCPs e RAGs primeiro.")
        
        with tab3:
            st.subheader("🔍 Consultar GraphRAG")
            st.markdown("Consulte o grafo de conhecimento usando GraphRAG com LangGraph")
            
            # Nota: Para usar GraphRAG, precisamos de um LLM
            # Por enquanto, vamos apenas buscar no grafo
            query = st.text_input("Digite sua pergunta", placeholder="Ex: Quais MCPs estão relacionados ao sistema RAG?")
            
            if st.button("🔍 Consultar"):
                if query:
                    with st.spinner("Consultando o grafo..."):
                        # Busca no grafo
                        results = neo4j_manager.search_graph(query, limit=10)
                        
                        if results:
                            st.write(f"**{len(results)} resultado(s) encontrado(s):**")
                            for i, result in enumerate(results, 1):
                                with st.expander(f"{i}. {result.get('name', result.get('id', 'Sem nome'))}"):
                                    st.write(f"**Tipo:** {result.get('__label__', 'Unknown')}")
                                    if result.get('description'):
                                        st.write(f"**Descrição:** {result.get('description')}")
                                    if result.get('content'):
                                        st.write(f"**Conteúdo:** {result.get('content')[:500]}...")
                        else:
                            st.info("ℹ️ Nenhum resultado encontrado.")
                else:
                    st.warning("⚠️ Por favor, digite uma pergunta")
        
        with tab4:
            st.subheader("📊 Visualizar Grafo")
            st.markdown("Visualize o grafo de conhecimento Neo4j")
            
            # Filtros
            col1, col2 = st.columns(2)
            with col1:
                node_types_filter = st.multiselect(
                    "Tipos de Nós",
                    ["MCP", "RAG", "ObsidianNote", "Tag"],
                    default=["MCP", "RAG"]
                )
            with col2:
                limit = st.number_input("Limite de Nós", min_value=10, max_value=200, value=50)
            
            # Estado para armazenar dados do grafo
            if "graph_data" not in st.session_state:
                st.session_state.graph_data = None
            
            if st.button("🔄 Atualizar Visualização"):
                try:
                    with st.spinner("Carregando dados do grafo..."):
                        graph_data = neo4j_manager.get_graph_visualization_data(
                            node_types=node_types_filter if node_types_filter else None,
                            limit=limit
                        )
                        st.session_state.graph_data = graph_data
                        
                        if graph_data["nodes"]:
                            # Estatísticas da visualização
                            col1, col2 = st.columns(2)
                            with col1:
                                st.metric("Nós", len(graph_data['nodes']))
                            with col2:
                                st.metric("Arestas", len(graph_data['edges']))
                            
                            # Visualização com pyvis
                            if PYVIS_AVAILABLE:
                                html_file = create_graph_visualization(graph_data)
                                if html_file:
                                    with open(html_file, 'r', encoding='utf-8') as f:
                                        html_content = f.read()
                                    st.components.v1.html(html_content, height=600, scrolling=True)
                                else:
                                    st.error("Erro ao criar visualização do grafo")
                            else:
                                st.warning("⚠️ Pyvis não disponível. Instale com: pip install pyvis")
                                st.json(graph_data)
                        else:
                            st.info("ℹ️ Nenhum dado encontrado no grafo. Crie nós primeiro.")
                except Exception as e:
                    st.error(f"Erro ao carregar dados do grafo: {e}")
            
            # Exibe dados anteriores se disponíveis
            if st.session_state.graph_data and st.session_state.graph_data.get("nodes"):
                st.divider()
                st.subheader("📋 Dados do Grafo")
                with st.expander("Ver dados JSON"):
                    st.json(st.session_state.graph_data)
        
        with tab5:
            st.subheader("🔎 Buscar no Grafo")
            st.markdown("Busque nós e relações no grafo")
            
            search_query = st.text_input("Termo de busca", placeholder="Digite o termo de busca...")
            node_types_search = st.multiselect(
                "Tipos de Nós para Buscar",
                ["MCP", "RAG", "ObsidianNote", "Tag"],
                default=[]
            )
            limit_search = st.number_input("Limite de Resultados", min_value=1, max_value=50, value=10)
            
            if st.button("🔍 Buscar"):
                if search_query:
                    with st.spinner("Buscando no grafo..."):
                        results = neo4j_manager.search_graph(
                            search_query,
                            node_types=node_types_search if node_types_search else None,
                            limit=limit_search
                        )
                        
                        if results:
                            st.write(f"**{len(results)} resultado(s) encontrado(s):**")
                            for i, result in enumerate(results, 1):
                                with st.expander(f"{i}. {result.get('name', result.get('id', 'Sem nome'))}"):
                                    st.write(f"**Tipo:** {result.get('__label__', 'Unknown')}")
                                    st.write(f"**ID:** {result.get('id', 'N/A')}")
                                    if result.get('description'):
                                        st.write(f"**Descrição:** {result.get('description')}")
                                    if result.get('content'):
                                        st.write(f"**Conteúdo:** {result.get('content')[:500]}...")
                                    if result.get('properties'):
                                        st.write("**Propriedades:**")
                                        st.json(result['properties'])
                        else:
                            st.info("ℹ️ Nenhum resultado encontrado.")
                else:
                    st.warning("⚠️ Por favor, digite um termo de busca")

# Footer
st.divider()
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
        <small>Gerenciador de MCP - Model Context Protocol</small>
    </div>
    """,
    unsafe_allow_html=True
)


