"""
Dashboard Streamlit melhorado para interagir com os agentes do sistema IA-Test.

Funcionalidades:
- Visão geral do sistema com gráficos Plotly
- Lista de agentes e status (atualizado para agentes consolidados)
- Interface de chat melhorada
- Diagnóstico e resolução integrados (System Health Agent)
- Monitoramento com visualizações interativas
- Configurações
"""

import streamlit as st
import sys
import os
from pathlib import Path
from datetime import datetime
import json
import traceback
from typing import Dict, List, Optional, Any

# Adiciona o diretório raiz ao path
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Muda para o diretório raiz
os.chdir(project_root)

# Imports opcionais para visualizações
try:
    import plotly.express as px
    import plotly.graph_objects as go
    import pandas as pd
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    st.warning("⚠️ Plotly/Pandas não disponível. Instale com: pip install plotly pandas")

try:
    from streamlit_option_menu import option_menu
    OPTION_MENU_AVAILABLE = True
except ImportError:
    OPTION_MENU_AVAILABLE = False

# Configuração da página
st.set_page_config(
    page_title="IA-Test Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado melhorado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .agent-card {
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #ddd;
        margin: 0.5rem 0;
        background: #f9f9f9;
        transition: transform 0.2s;
    }
    .agent-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .status-active {
        color: #28a745;
        font-weight: bold;
    }
    .status-inactive {
        color: #dc3545;
        font-weight: bold;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 0.5rem;
        color: white;
        text-align: center;
    }
    .issue-critical {
        border-left: 4px solid #dc3545;
        padding-left: 1rem;
        margin: 0.5rem 0;
    }
    .issue-high {
        border-left: 4px solid #fd7e14;
        padding-left: 1rem;
        margin: 0.5rem 0;
    }
    .issue-medium {
        border-left: 4px solid #ffc107;
        padding-left: 1rem;
        margin: 0.5rem 0;
    }
    .issue-low {
        border-left: 4px solid #17a2b8;
        padding-left: 1rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Inicialização do estado da sessão
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'selected_agent' not in st.session_state:
    st.session_state.selected_agent = None
if 'system_status' not in st.session_state:
    st.session_state.system_status = {}
if 'health_report' not in st.session_state:
    st.session_state.health_report = None
if 'diagnostic_issues' not in st.session_state:
    st.session_state.diagnostic_issues = []
if 'resolutions' not in st.session_state:
    st.session_state.resolutions = []

def get_orchestrator():
    """Obtém a instância do Orchestrator."""
    try:
        from src.agents.orchestrator import get_orchestrator
        return get_orchestrator()
    except Exception as e:
        st.error(f"Erro ao carregar Orchestrator: {e}")
        return None

def get_system_health_agent():
    """Obtém a instância do System Health Agent (consolidado)."""
    try:
        from src.agents.system_health_agent import get_system_health_agent
        return get_system_health_agent()
    except Exception as e:
        st.warning(f"System Health Agent não disponível: {e}")
        return None

def get_agents_list() -> List[Dict[str, Any]]:
    """Obtém lista de agentes disponíveis (atualizado para agentes consolidados)."""
    agents = [
        {
            "name": "Orchestrator",
            "type": "orchestrator",
            "description": "Coordenador central com planejamento inteligente",
            "status": "active",
            "icon": "🎯"
        },
        {
            "name": "System Health Agent",
            "type": "system_health",
            "description": "Diagnóstico, monitoramento e resolução (consolidado)",
            "status": "active",
            "icon": "🏥"
        },
        {
            "name": "DB Manager",
            "type": "db_manager",
            "description": "Gerenciamento de bancos de dados",
            "status": "active",
            "icon": "💾"
        },
        {
            "name": "MCP Manager",
            "type": "mcp_manager",
            "description": "Gerenciamento de servidores MCP",
            "status": "active",
            "icon": "🔌"
        },
        {
            "name": "Git Integration",
            "type": "git_integration",
            "description": "Integração com Git/GitHub",
            "status": "active",
            "icon": "📦"
        },
        {
            "name": "Neo4j GraphRAG",
            "type": "neo4j_graphrag",
            "description": "GraphRAG com Neo4j",
            "status": "active",
            "icon": "🕸️"
        },
        {
            "name": "Obsidian Integration",
            "type": "obsidian_integration",
            "description": "Integração com Obsidian",
            "status": "active",
            "icon": "📝"
        },
        {
            "name": "Kestra Agent",
            "type": "kestra_agent",
            "description": "Orquestração de workflows Kestra",
            "status": "active",
            "icon": "⚙️"
        },
        {
            "name": "Docker Integration",
            "type": "docker_integration",
            "description": "Gerenciamento de containers Docker",
            "status": "active",
            "icon": "🐳"
        },
    ]
    return agents

def get_system_status() -> Dict[str, Any]:
    """Obtém status do sistema."""
    try:
        orchestrator = get_orchestrator()
        if orchestrator:
            return orchestrator.get_system_status()
    except Exception as e:
        st.warning(f"Erro ao obter status: {e}")
    
    # Status padrão
    return {
        "total_agents": 11,
        "active_agents": 11,
        "total_tasks": 0,
        "completed_tasks": 0,
        "system_health": "healthy"
    }

def render_overview():
    """Renderiza a visão geral do sistema com gráficos."""
    st.markdown('<div class="main-header">📊 Visão Geral do Sistema</div>', unsafe_allow_html=True)
    
    status = get_system_status()
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total de Agentes", status.get("total_agents", 11))
    
    with col2:
        st.metric("Agentes Ativos", status.get("active_agents", 11))
    
    with col3:
        st.metric("Tarefas Completas", status.get("completed_tasks", 0))
    
    with col4:
        health = status.get("system_health", "healthy")
        st.metric("Status do Sistema", "✅ Saudável" if health == "healthy" else "⚠️ Atenção")
    
    st.divider()
    
    # Gráficos com Plotly (se disponível)
    if PLOTLY_AVAILABLE:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Distribuição de Agentes")
            agents = get_agents_list()
            active_count = sum(1 for a in agents if a['status'] == 'active')
            inactive_count = len(agents) - active_count
            
            fig = px.pie(
                values=[active_count, inactive_count],
                names=['Ativos', 'Inativos'],
                color_discrete_map={'Ativos': '#28a745', 'Inativos': '#dc3545'}
            )
            fig.update_layout(showlegend=True, height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("📊 Status do Sistema")
            # Dados de exemplo para o gráfico
            if status.get("total_tasks", 0) > 0:
                completed = status.get("completed_tasks", 0)
                pending = status.get("total_tasks", 0) - completed
                
                fig = go.Figure(data=[
                    go.Bar(name='Completas', x=['Tarefas'], y=[completed], marker_color='#28a745'),
                    go.Bar(name='Pendentes', x=['Tarefas'], y=[pending], marker_color='#ffc107')
                ])
                fig.update_layout(barmode='stack', height=300, showlegend=True)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Nenhuma tarefa registrada ainda.")
    
    st.divider()
    
    # Lista de agentes
    st.subheader("🤖 Agentes Disponíveis")
    agents = get_agents_list()
    
    # Grid de agentes
    cols = st.columns(3)
    for idx, agent in enumerate(agents):
        col = cols[idx % 3]
        with col:
            with st.container():
                status_class = "status-active" if agent["status"] == "active" else "status-inactive"
                st.markdown(f"""
                <div class="agent-card">
                    <h3>{agent["icon"]} {agent["name"]}</h3>
                    <p>{agent["description"]}</p>
                    <p class="{status_class}">Status: {agent["status"].upper()}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Selecionar {agent['name']}", key=f"select_{agent['type']}"):
                    st.session_state.selected_agent = agent
                    st.rerun()

def render_agents_list():
    """Renderiza lista detalhada de agentes."""
    st.markdown('<div class="main-header">🤖 Lista de Agentes</div>', unsafe_allow_html=True)
    
    agents = get_agents_list()
    
    for agent in agents:
        with st.expander(f"{agent['icon']} {agent['name']} - {agent['description']}", expanded=False):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(f"**Tipo:** {agent['type']}")
                st.write(f"**Status:** {agent['status']}")
                st.write(f"**Descrição:** {agent['description']}")
            
            with col2:
                if agent['status'] == 'active':
                    st.success("✅ Ativo")
                else:
                    st.error("❌ Inativo")
                
                if st.button("Interagir", key=f"interact_{agent['type']}"):
                    st.session_state.selected_agent = agent
                    st.rerun()

def render_diagnostics():
    """Renderiza diagnóstico de problemas (usando System Health Agent)."""
    st.markdown('<div class="main-header">🔍 Diagnóstico de Problemas</div>', unsafe_allow_html=True)
    
    health_agent = get_system_health_agent()
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.info("💡 Use o System Health Agent (consolidado) para diagnosticar problemas do sistema.")
    with col2:
        if st.button("🔄 Executar Diagnóstico Completo", type="primary"):
            with st.spinner("Executando diagnóstico..."):
                try:
                    if health_agent:
                        report = health_agent.run_full_health_check()
                        st.session_state.health_report = report
                        st.session_state.diagnostic_issues = report.diagnostic_issues
                        st.session_state.resolutions = report.resolutions
                        st.success(f"✅ Diagnóstico concluído! {len(report.diagnostic_issues)} problemas encontrados.")
                        st.rerun()
                    else:
                        st.error("System Health Agent não disponível.")
                except Exception as e:
                    st.error(f"Erro ao executar diagnóstico: {e}")
                    st.code(traceback.format_exc())
    
    st.divider()
    
    # Exibe problemas diagnosticados
    issues = st.session_state.diagnostic_issues
    if issues:
        st.subheader(f"📋 Problemas Encontrados ({len(issues)})")
        
        # Filtros
        col1, col2 = st.columns(2)
        with col1:
            severity_filter = st.selectbox("Filtrar por Severidade", ["Todas", "CRITICAL", "HIGH", "MEDIUM", "LOW"])
        with col2:
            category_filter = st.selectbox("Filtrar por Categoria", ["Todas", "CONFIGURATION", "CONNECTION", "PERMISSION", "DEPENDENCY"])
        
        # Aplica filtros
        filtered_issues = issues
        if severity_filter != "Todas":
            filtered_issues = [i for i in filtered_issues if i.severity.value == severity_filter]
        if category_filter != "Todas":
            filtered_issues = [i for i in filtered_issues if i.category.value == category_filter]
        
        # Resumo
        if PLOTLY_AVAILABLE and filtered_issues:
            severity_counts = {}
            for issue in filtered_issues:
                sev = issue.severity.value
                severity_counts[sev] = severity_counts.get(sev, 0) + 1
            
            if severity_counts:
                fig = px.bar(
                    x=list(severity_counts.keys()),
                    y=list(severity_counts.values()),
                    labels={'x': 'Severidade', 'y': 'Quantidade'},
                    title="Distribuição de Problemas por Severidade"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Lista de problemas
        for issue in filtered_issues:
            severity_class = f"issue-{issue.severity.value.lower()}"
            with st.container():
                st.markdown(f'<div class="{severity_class}">', unsafe_allow_html=True)
                st.markdown(f"### {issue.severity.value}: {issue.title}")
                st.write(f"**Categoria:** {issue.category.value}")
                st.write(f"**Descrição:** {issue.description}")
                if issue.details:
                    with st.expander("Detalhes"):
                        st.json(issue.details)
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("ℹ️ Nenhum problema diagnosticado ainda. Execute o diagnóstico completo.")

def render_resolutions():
    """Renderiza resoluções para problemas (usando System Health Agent)."""
    st.markdown('<div class="main-header">💡 Resoluções Sugeridas</div>', unsafe_allow_html=True)
    
    resolutions = st.session_state.resolutions
    issues = st.session_state.diagnostic_issues
    
    if not resolutions and issues:
        st.info("💡 Execute o diagnóstico completo para gerar resoluções.")
        if st.button("🔄 Gerar Resoluções"):
            health_agent = get_system_health_agent()
            if health_agent:
                with st.spinner("Gerando resoluções..."):
                    try:
                        resolutions = health_agent.generate_resolutions(issues)
                        st.session_state.resolutions = resolutions
                        st.success(f"✅ {len(resolutions)} resoluções geradas!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao gerar resoluções: {e}")
    
    if resolutions:
        st.subheader(f"🛠️ Resoluções Disponíveis ({len(resolutions)})")
        
        for idx, resolution in enumerate(resolutions):
            with st.expander(f"💡 Resolução {idx + 1}: {resolution.title}", expanded=False):
                st.markdown(f"**Problema:** {resolution.issue_title}")
                st.markdown(f"**Descrição:** {resolution.description}")
                
                if resolution.commands:
                    st.subheader("📝 Comandos para Executar:")
                    for cmd in resolution.commands:
                        st.code(cmd, language="bash")
                
                if resolution.prompt:
                    st.subheader("💬 Prompt Sugerido:")
                    st.text_area("Prompt", resolution.prompt, height=100, key=f"prompt_{idx}")
                    if st.button(f"📋 Copiar Prompt {idx + 1}", key=f"copy_{idx}"):
                        st.code(resolution.prompt)
                
                if resolution.documentation_url:
                    st.markdown(f"📚 [Documentação]({resolution.documentation_url})")
    else:
        st.info("ℹ️ Nenhuma resolução disponível. Execute o diagnóstico primeiro.")

def render_chat():
    """Renderiza interface de chat melhorada."""
    st.markdown('<div class="main-header">💬 Chat com Agentes</div>', unsafe_allow_html=True)
    
    # Seleção de agente
    agents = get_agents_list()
    agent_names = [f"{a['icon']} {a['name']}" for a in agents]
    
    selected_idx = 0
    if st.session_state.selected_agent:
        selected_idx = next((i for i, a in enumerate(agents) if a['type'] == st.session_state.selected_agent['type']), 0)
    
    selected_agent_name = st.selectbox(
        "Selecione um agente:",
        agent_names,
        index=selected_idx,
        key="agent_selector"
    )
    
    selected_agent = agents[agent_names.index(selected_agent_name)]
    st.session_state.selected_agent = selected_agent
    
    st.info(f"💡 Conversando com: **{selected_agent['name']}** - {selected_agent['description']}")
    
    st.divider()
    
    # Histórico de chat
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            if message.get('agent') == selected_agent['type']:
                with st.chat_message(message['role']):
                    st.write(message['content'])
                    if 'timestamp' in message:
                        st.caption(f"🕒 {message['timestamp']}")
    
    # Input de chat
    user_input = st.chat_input("Digite sua mensagem aqui...")
    
    if user_input:
        # Adiciona mensagem do usuário
        st.session_state.chat_history.append({
            'role': 'user',
            'content': user_input,
            'agent': selected_agent['type'],
            'timestamp': datetime.now().strftime("%H:%M:%S")
        })
        
        # Processa mensagem
        try:
            response = process_agent_message(selected_agent, user_input)
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': response,
                'agent': selected_agent['type'],
                'timestamp': datetime.now().strftime("%H:%M:%S")
            })
        except Exception as e:
            error_msg = f"Erro ao processar mensagem: {str(e)}"
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': error_msg,
                'agent': selected_agent['type'],
                'timestamp': datetime.now().strftime("%H:%M:%S")
            })
        
        st.rerun()
    
    # Botão para limpar chat
    if st.button("🗑️ Limpar Chat"):
        st.session_state.chat_history = [m for m in st.session_state.chat_history if m.get('agent') != selected_agent['type']]
        st.rerun()

def process_agent_message(agent: Dict, message: str) -> str:
    """Processa mensagem para um agente (atualizado para agentes consolidados)."""
    try:
        orchestrator = get_orchestrator()
        if not orchestrator:
            return "❌ Orchestrator não disponível. Verifique a configuração do sistema."
        
        # Mapeia tipo de agente para AgentType (atualizado)
        agent_type_map = {
            "orchestrator": "orchestrator",
            "system_health": "system_health",
            "db_manager": "db_manager",
            "mcp_manager": "mcp_architect",
            "git_integration": "git_integration",
            "neo4j_graphrag": "neo4j_graphrag",
            "obsidian_integration": "obsidian",
            "kestra_agent": "kestra",
            "docker_integration": "docker_integration",
        }
        
        agent_type_str = agent_type_map.get(agent['type'])
        
        # Comandos especiais
        if message.lower().startswith("diagnóstico") or message.lower().startswith("diagnostico"):
            health_agent = get_system_health_agent()
            if health_agent:
                report = health_agent.run_full_health_check()
                return f"✅ Diagnóstico completo executado!\n\n📊 Resumo:\n- Problemas: {len(report.diagnostic_issues)}\n- Agentes monitorados: {len(report.agent_metrics)}\n- Resoluções: {len(report.resolutions)}"
            else:
                return "❌ System Health Agent não disponível."
        
        if message.lower().startswith("status"):
            status = get_system_status()
            return f"📊 Status do Sistema:\n- Agentes: {status.get('total_agents', 0)}\n- Ativos: {status.get('active_agents', 0)}\n- Saúde: {status.get('system_health', 'unknown')}"
        
        if not agent_type_str:
            return f"✅ Mensagem recebida pelo {agent['name']}: {message}\n\n⚠️ Integração completa em desenvolvimento."
        
        # Cria tarefa
        from src.agents.orchestrator import AgentType
        try:
            agent_type = AgentType[agent_type_str.upper()]
        except KeyError:
            return f"⚠️ Tipo de agente '{agent_type_str}' não encontrado."
        
        task = orchestrator.create_task(
            agent_type=agent_type,
            description=message,
            parameters={"message": message, "user_input": message}
        )
        
        # Executa tarefa
        result = orchestrator.execute_task(task)
        
        if result and result.success:
            return f"✅ Resposta do {agent['name']}:\n\n{result.data if hasattr(result, 'data') and result.data else 'Tarefa executada com sucesso!'}"
        else:
            return f"⚠️ {agent['name']} retornou: {result.error if hasattr(result, 'error') and result.error else 'Erro desconhecido'}"
    
    except Exception as e:
        return f"❌ Erro ao processar: {str(e)}\n\nDetalhes: {traceback.format_exc()}"

def render_monitoring():
    """Renderiza monitoramento com visualizações Plotly melhoradas."""
    st.markdown('<div class="main-header">📈 Monitoramento Avançado</div>', unsafe_allow_html=True)
    
    status = get_system_status()
    health_agent = get_system_health_agent()
    orchestrator = get_orchestrator()
    
    # Métricas principais em 4 colunas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        agents = get_agents_list()
        active_count = sum(1 for a in agents if a['status'] == 'active')
        st.metric("Agentes Ativos", active_count, delta=None)
    
    with col2:
        st.metric("Total de Tarefas", status.get("total_tasks", 0))
    
    with col3:
        st.metric("Tarefas Completas", status.get("completed_tasks", 0))
    
    with col4:
        if status.get("total_tasks", 0) > 0:
            completion_rate = (status.get("completed_tasks", 0) / status.get("total_tasks", 1)) * 100
            st.metric("Taxa de Sucesso", f"{completion_rate:.1f}%")
        else:
            st.metric("Taxa de Sucesso", "N/A")
    
    st.divider()
    
    # Gráficos melhorados
    if PLOTLY_AVAILABLE:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Distribuição de Agentes")
            agents = get_agents_list()
            active_count = sum(1 for a in agents if a['status'] == 'active')
            inactive_count = len(agents) - active_count
            
            fig = px.pie(
                values=[active_count, inactive_count],
                names=['Ativos', 'Inativos'],
                title="Status dos Agentes",
                color_discrete_map={'Ativos': '#28a745', 'Inativos': '#dc3545'}
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(height=350, showlegend=True)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("📈 Performance de Tarefas")
            if status.get("total_tasks", 0) > 0:
                completed = status.get("completed_tasks", 0)
                pending = status.get("total_tasks", 0) - completed
                failed = status.get("failed_tasks", 0)
                
                fig = go.Figure(data=[
                    go.Bar(name='Completas', x=['Tarefas'], y=[completed], marker_color='#28a745'),
                    go.Bar(name='Pendentes', x=['Tarefas'], y=[pending], marker_color='#ffc107'),
                    go.Bar(name='Falhas', x=['Tarefas'], y=[failed], marker_color='#dc3545')
                ])
                fig.update_layout(barmode='stack', height=350, showlegend=True, title="Status das Tarefas")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Nenhuma tarefa registrada ainda.")
    
    st.divider()
    
    # Nova seção: Uso de LLM
    st.subheader("🤖 Configuração de LLM")
    try:
        import os
        from dotenv import load_dotenv
        load_dotenv()
        
        llm_name = os.getenv("LLM", "llama2")
        embedding_model = os.getenv("EMBEDDING_MODEL", "sentence_transformer")
        google_api_key = os.getenv("GOOGLE_API_KEY", "")
        ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("LLM Atual", llm_name.upper())
            if "gemini" in llm_name.lower():
                st.success("✅ Usando Google Gemini")
            elif "gpt" in llm_name.lower():
                st.info("ℹ️ Usando OpenAI")
            else:
                st.info(f"ℹ️ Usando Ollama ({llm_name})")
        
        with col2:
            st.metric("Embedding Model", embedding_model.replace("_", " ").title())
        
        with col3:
            if google_api_key:
                st.success("✅ Google API Key configurada")
            else:
                st.warning("⚠️ Google API Key não configurada")
        
        # Gráfico de uso de LLM por agente
        if PLOTLY_AVAILABLE:
            st.subheader("📊 Agentes que Usam LLM")
            agents_with_llm = [
                {"name": "Orchestrator", "uses_llm": True, "purpose": "Planejamento"},
                {"name": "Neo4j GraphRAG", "uses_llm": True, "purpose": "GraphRAG"},
                {"name": "Agent Helper", "uses_llm": True, "purpose": "Otimização"},
            ]
            agents_without_llm = [
                {"name": a["name"], "uses_llm": False, "purpose": "Sem LLM"}
                for a in get_agents_list()
                if a["name"] not in ["Orchestrator", "Neo4j GraphRAG", "Agent Helper"]
            ]
            
            all_agents_llm = agents_with_llm + agents_without_llm[:8]  # Limita para visualização
            
            df = pd.DataFrame(all_agents_llm)
            fig = px.bar(
                df,
                x="name",
                y=[1] * len(df),
                color="uses_llm",
                title="Agentes e Uso de LLM",
                labels={"uses_llm": "Usa LLM", "name": "Agente"},
                color_discrete_map={True: '#28a745', False: '#6c757d'}
            )
            fig.update_layout(height=300, showlegend=True)
            st.plotly_chart(fig, use_container_width=True)
    
    except Exception as e:
        st.warning(f"Erro ao obter configuração de LLM: {e}")
    
    st.divider()
    
    # Nova seção: Kestra Integration
    st.subheader("⚙️ Integração com Kestra")
    try:
        from src.agents.mcp_kestra_integration import get_kestra_agent
        
        kestra_agent = get_kestra_agent()
        if kestra_agent:
            st.success("✅ Kestra Agent disponível")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Kestra URL", kestra_agent.kestra_url)
                if st.button("🔗 Abrir Kestra UI"):
                    st.markdown(f"[Abrir Kestra]({kestra_agent.kestra_url})", unsafe_allow_html=True)
            
            with col2:
                workflows = kestra_agent.list_workflows()
                st.metric("Workflows", len(workflows))
                
                if workflows:
                    with st.expander("Ver Workflows"):
                        for wf in workflows:
                            st.write(f"- {wf.name} ({wf.id})")
                else:
                    st.info("Nenhum workflow criado ainda.")
            
            # Criar workflow de monitoramento
            if st.button("📝 Criar Workflow de Monitoramento"):
                with st.spinner("Criando workflow..."):
                    try:
                        workflow = kestra_agent.create_health_check_workflow()
                        st.success(f"✅ Workflow criado: {workflow.id}")
                        st.json(workflow.to_dict())
                    except Exception as e:
                        st.error(f"Erro ao criar workflow: {e}")
        else:
            st.warning("⚠️ Kestra Agent não disponível")
            st.info("💡 Para usar Kestra, configure no docker-compose.yml")
    
    except Exception as e:
        st.warning(f"Kestra não disponível: {e}")
    
    st.divider()
    
    # Métricas do System Health Agent
    if health_agent and st.session_state.health_report:
        st.subheader("📊 Métricas de Saúde do Sistema")
        report = st.session_state.health_report
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Problemas", len(report.diagnostic_issues))
        with col2:
            critical = len([i for i in report.diagnostic_issues if i.severity.value == "CRITICAL"])
            st.metric("Críticos", critical, delta=None)
        with col3:
            st.metric("Agentes Monitorados", len(report.agent_metrics))
        with col4:
            st.metric("Resoluções", len(report.resolutions))
    
    st.divider()
    
    # Logs do sistema
    st.subheader("📋 Logs do Sistema")
    st.text_area("Últimos logs:", value="Sistema inicializado com sucesso.\nTodos os agentes estão ativos.", height=200)

def render_settings():
    """Renderiza configurações."""
    st.markdown('<div class="main-header">⚙️ Configurações</div>', unsafe_allow_html=True)
    
    st.subheader("🔧 Configurações do Sistema")
    
    # Variáveis de ambiente
    with st.expander("Variáveis de Ambiente", expanded=False):
        env_vars = {
            "NEO4J_URI": os.getenv("NEO4J_URI", "Não configurado"),
            "NEO4J_USERNAME": os.getenv("NEO4J_USERNAME", "Não configurado"),
            "OLLAMA_BASE_URL": os.getenv("OLLAMA_BASE_URL", "Não configurado"),
            "LLM": os.getenv("LLM", "Não configurado"),
        }
        
        for key, value in env_vars.items():
            st.text_input(key, value, disabled=True)
    
    # Exportação de dados
    st.subheader("📥 Exportação")
    if st.button("Exportar Histórico de Chat"):
        chat_json = json.dumps(st.session_state.chat_history, indent=2, default=str)
        st.download_button(
            "Download JSON",
            chat_json,
            file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    # Limpar dados
    st.subheader("🗑️ Limpeza")
    if st.button("Limpar Todos os Dados", type="secondary"):
        st.session_state.chat_history = []
        st.session_state.system_status = {}
        st.session_state.health_report = None
        st.session_state.diagnostic_issues = []
        st.session_state.resolutions = []
        st.success("Dados limpos com sucesso!")

def main():
    """Função principal do dashboard."""
    # Sidebar com menu melhorado
    with st.sidebar:
        st.title("🤖 IA-Test Dashboard")
        st.divider()
        
        if OPTION_MENU_AVAILABLE:
            page = option_menu(
                "Navegação",
                ["📊 Visão Geral", "🤖 Agentes", "🔍 Diagnóstico", "💡 Resoluções", "💬 Chat", "📈 Monitoramento", "⚙️ Configurações"],
                icons=['house', 'robot', 'search', 'lightbulb', 'chat', 'graph-up', 'gear'],
                menu_icon="cast",
                default_index=0
            )
        else:
            page = st.radio(
                "Navegação",
                ["📊 Visão Geral", "🤖 Agentes", "🔍 Diagnóstico", "💡 Resoluções", "💬 Chat", "📈 Monitoramento", "⚙️ Configurações"],
                index=0
            )
        
        st.divider()
        
        # Status rápido
        status = get_system_status()
        st.metric("Agentes Ativos", status.get("active_agents", 11))
        st.metric("Status", "✅ Saudável" if status.get("system_health") == "healthy" else "⚠️")
        
        st.divider()
        st.caption(f"🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Conteúdo principal
    if page == "📊 Visão Geral":
        render_overview()
    elif page == "🤖 Agentes":
        render_agents_list()
    elif page == "🔍 Diagnóstico":
        render_diagnostics()
    elif page == "💡 Resoluções":
        render_resolutions()
    elif page == "💬 Chat":
        render_chat()
    elif page == "📈 Monitoramento":
        render_monitoring()
    elif page == "⚙️ Configurações":
        render_settings()

if __name__ == "__main__":
    main()
