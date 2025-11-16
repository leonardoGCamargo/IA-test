"""
Interface Streamlit para Dashboard de Agentes.

Este módulo fornece uma interface visual para:
- Conversar com os agentes
- Visualizar problemas diagnosticados
- Ver soluções e prompts de resolução
"""

import streamlit as st
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import json
import sys
import os
from pathlib import Path

# Adiciona o diretório raiz ao path
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Muda para o diretório raiz do projeto
os.chdir(project_root)

from src.agents.diagnostic_agent import (
    get_diagnostic_agent, DiagnosticIssue, IssueSeverity, IssueCategory
)
from src.agents.resolution_agent import (
    get_resolution_agent, Resolution
)
from src.agents.orchestrator import get_orchestrator, AgentType

logger = logging.getLogger(__name__)

# Configuração da página
st.set_page_config(
    page_title="Dashboard de Agentes",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .issue-card {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border-left: 4px solid;
    }
    .issue-critical {
        background-color: #fee;
        border-color: #c33;
    }
    .issue-high {
        background-color: #ffe;
        border-color: #cc3;
    }
    .issue-medium {
        background-color: #eff;
        border-color: #3cc;
    }
    .issue-low {
        background-color: #efe;
        border-color: #3c3;
    }
    .resolution-card {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        background-color: #f9f9f9;
        border: 1px solid #ddd;
    }
    .command-box {
        background-color: #2d2d2d;
        color: #f8f8f2;
        padding: 1rem;
        border-radius: 0.5rem;
        font-family: monospace;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)


def init_session_state():
    """Inicializa o estado da sessão."""
    if "diagnostic_agent" not in st.session_state:
        st.session_state.diagnostic_agent = get_diagnostic_agent()
    if "resolution_agent" not in st.session_state:
        st.session_state.resolution_agent = get_resolution_agent()
    if "orchestrator" not in st.session_state:
        st.session_state.orchestrator = get_orchestrator()
    if "issues" not in st.session_state:
        st.session_state.issues = []
    if "resolutions" not in st.session_state:
        st.session_state.resolutions = []
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "diagnostic_run" not in st.session_state:
        st.session_state.diagnostic_run = False


def run_diagnostic():
    """Executa diagnóstico completo."""
    with st.spinner("Executando diagnóstico..."):
        issues = st.session_state.diagnostic_agent.run_full_diagnostic()
        st.session_state.issues = issues
        st.session_state.diagnostic_run = True
        
        # Gera soluções para os problemas
        resolutions = st.session_state.resolution_agent.generate_resolutions(issues)
        st.session_state.resolutions = resolutions
        
        st.success(f"Diagnóstico concluído! {len(issues)} problemas encontrados.")


def get_severity_color(severity: IssueSeverity) -> str:
    """Retorna a cor para a severidade."""
    colors = {
        IssueSeverity.CRITICAL: "#c33",
        IssueSeverity.HIGH: "#cc3",
        IssueSeverity.MEDIUM: "#3cc",
        IssueSeverity.LOW: "#3c3",
        IssueSeverity.INFO: "#999"
    }
    return colors.get(severity, "#999")


def get_severity_class(severity: IssueSeverity) -> str:
    """Retorna a classe CSS para a severidade."""
    classes = {
        IssueSeverity.CRITICAL: "issue-critical",
        IssueSeverity.HIGH: "issue-high",
        IssueSeverity.MEDIUM: "issue-medium",
        IssueSeverity.LOW: "issue-low",
        IssueSeverity.INFO: "issue-low"
    }
    return classes.get(severity, "issue-low")


def render_issue_card(issue: DiagnosticIssue):
    """Renderiza um cartão de problema."""
    severity_class = get_severity_class(issue.severity)
    severity_color = get_severity_color(issue.severity)
    
    st.markdown(f"""
        <div class="issue-card {severity_class}">
            <h3 style="color: {severity_color}; margin-top: 0;">{issue.title}</h3>
            <p><strong>Categoria:</strong> {issue.category.value} | <strong>Severidade:</strong> {issue.severity.value}</p>
            <p>{issue.description}</p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.expander("Ver detalhes"):
        st.json(issue.to_dict())


def render_resolution_card(resolution: Resolution):
    """Renderiza um cartão de solução."""
    st.markdown(f"""
        <div class="resolution-card">
            <h3>{resolution.title}</h3>
            <p>{resolution.description}</p>
        </div>
    """, unsafe_allow_html=True)
    
    if resolution.steps:
        st.markdown("### Passos para resolver:")
        for i, step in enumerate(resolution.steps, 1):
            st.markdown(f"{step}")
    
    if resolution.commands:
        st.markdown("### Comandos:")
        for command in resolution.commands:
            st.markdown(f'<div class="command-box">{command}</div>', unsafe_allow_html=True)
            st.code(command, language="bash")
    
    if resolution.prompts:
        st.markdown("### Prompts:")
        for i, prompt in enumerate(resolution.prompts, 1):
            st.markdown(f"**Prompt {i}:**")
            st.info(prompt)
    
    if resolution.documentation_links:
        st.markdown("### Links de documentação:")
        for link in resolution.documentation_links:
            st.markdown(f"- [{link}]({link})")
    
    if resolution.estimated_time:
        st.markdown(f"**Tempo estimado:** {resolution.estimated_time}")
    
    if resolution.difficulty:
        st.markdown(f"**Dificuldade:** {resolution.difficulty}")


def render_chat_interface():
    """Renderiza a interface de chat."""
    st.markdown("## 💬 Conversa com Agentes")
    
    # Botão para limpar chat
    if st.button("🗑️ Limpar Chat", key="clear_chat"):
        st.session_state.chat_history = []
        st.rerun()
    
    # Exibe histórico de chat
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Input de chat
    user_input = st.chat_input("Digite sua mensagem aqui...")
    
    if user_input:
        # Adiciona mensagem do usuário ao histórico
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input
        })
        
        # Processa mensagem e adiciona resposta ao histórico
        try:
            response = process_chat_message(user_input)
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": response
            })
            st.rerun()
        except Exception as e:
            import traceback
            error_msg = f"Erro ao processar mensagem: {str(e)}"
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": error_msg
            })
            st.error(error_msg)
            st.rerun()
    


def process_chat_message(message: str) -> str:
    """Processa uma mensagem de chat."""
    message_lower = message.lower()
    
    # Comandos de diagnóstico
    if "diagnóstico" in message_lower or "diagnostic" in message_lower:
        issues = st.session_state.diagnostic_agent.run_full_diagnostic()
        st.session_state.issues = issues
        resolutions = st.session_state.resolution_agent.generate_resolutions(issues)
        st.session_state.resolutions = resolutions
        st.session_state.diagnostic_run = True
        
        summary = st.session_state.diagnostic_agent.get_summary()
        return f"Diagnóstico executado! {summary['total_issues']} problemas encontrados. " \
               f"Críticos: {summary['critical']}, Altos: {summary['high']}, Médios: {summary['medium']}."
    
    # Consulta de status
    elif "status" in message_lower:
        status = st.session_state.orchestrator.get_system_status()
        return f"Status do sistema:\n{json.dumps(status, indent=2, default=str)}"
    
    # Lista de agentes
    elif "agentes" in message_lower or "agents" in message_lower:
        agents = [
            "MCP Manager",
            "Docker Integration",
            "Obsidian",
            "Neo4j GraphRAG",
            "Kestra",
            "Git Integration",
            "Database Manager",
            "Diagnostic Agent",
            "Resolution Agent"
        ]
        return f"Agentes disponíveis:\n" + "\n".join(f"- {agent}" for agent in agents)
    
    # Resposta padrão
    else:
        return f"Recebi sua mensagem: {message}. Como posso ajudá-lo? " \
               f"Você pode pedir um diagnóstico, verificar o status do sistema, ou listar os agentes disponíveis."


def render_issues_tab():
    """Renderiza a aba de problemas."""
    st.markdown("## 🔍 Problemas Diagnosticados")
    
    # Botão para executar diagnóstico
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("🔄 Executar Diagnóstico", type="primary"):
            run_diagnostic()
    
    with col2:
        if st.session_state.diagnostic_run:
            st.success("✅ Diagnóstico executado")
    
    if not st.session_state.issues:
        st.info("Nenhum problema encontrado. Execute o diagnóstico para verificar o sistema.")
        return
    
    # Resumo
    summary = st.session_state.diagnostic_agent.get_summary()
    st.markdown("### 📊 Resumo")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total", summary["total_issues"])
    with col2:
        st.metric("Críticos", summary["critical"], delta_color="inverse")
    with col3:
        st.metric("Altos", summary["high"], delta_color="inverse")
    with col4:
        st.metric("Médios", summary["medium"])
    with col5:
        st.metric("Baixos", summary["low"])
    
    # Filtros
    st.markdown("### 🔽 Filtros")
    col1, col2 = st.columns(2)
    with col1:
        selected_severity = st.multiselect(
            "Severidade",
            options=[s.value for s in IssueSeverity],
            default=[s.value for s in IssueSeverity]
        )
    with col2:
        selected_category = st.multiselect(
            "Categoria",
            options=[c.value for c in IssueCategory],
            default=[c.value for c in IssueCategory]
        )
    
    # Filtra problemas
    filtered_issues = [
        issue for issue in st.session_state.issues
        if issue.severity.value in selected_severity
        and issue.category.value in selected_category
    ]
    
    # Exibe problemas
    st.markdown("### 📋 Problemas")
    if not filtered_issues:
        st.info("Nenhum problema encontrado com os filtros selecionados.")
    else:
        for issue in filtered_issues:
            render_issue_card(issue)


def render_resolutions_tab():
    """Renderiza a aba de resoluções."""
    st.markdown("## 🛠️ Soluções e Resoluções")
    
    if not st.session_state.resolutions:
        st.info("Nenhuma solução disponível. Execute o diagnóstico primeiro.")
        return
    
    # Filtros
    st.markdown("### 🔽 Filtros")
    col1, col2 = st.columns(2)
    with col1:
        selected_difficulty = st.multiselect(
            "Dificuldade",
            options=["easy", "medium", "hard"],
            default=["easy", "medium", "hard"]
        )
    with col2:
        search_term = st.text_input("Buscar", placeholder="Digite para buscar...")
    
    # Filtra soluções
    filtered_resolutions = [
        resolution for resolution in st.session_state.resolutions
        if resolution.difficulty in selected_difficulty
        and (not search_term or search_term.lower() in resolution.title.lower() or search_term.lower() in resolution.description.lower())
    ]
    
    # Exibe soluções
    st.markdown("### 📋 Soluções")
    if not filtered_resolutions:
        st.info("Nenhuma solução encontrada com os filtros selecionados.")
    else:
        for resolution in filtered_resolutions:
            render_resolution_card(resolution)


def render_dashboard_tab():
    """Renderiza a aba de dashboard."""
    st.markdown("## 📊 Dashboard do Sistema")
    
    # Status do sistema
    status = st.session_state.orchestrator.get_system_status()
    
    # Métricas principais
    st.markdown("### 📈 Métricas Principais")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Agentes Disponíveis", sum(1 for v in status.values() if isinstance(v, dict) and v.get("available", False)))
    with col2:
        st.metric("Bancos de Dados", status.get("db_manager", {}).get("databases_count", 0))
    with col3:
        st.metric("Tarefas Pendentes", status.get("tasks", {}).get("pending", 0))
    with col4:
        st.metric("Tarefas Concluídas", status.get("tasks", {}).get("completed", 0))
    
    # Status detalhado
    st.markdown("### 📋 Status Detalhado")
    st.json(status)


def main():
    """Função principal."""
    init_session_state()
    
    # Header
    st.markdown('<div class="main-header">🤖 Dashboard de Agentes</div>', unsafe_allow_html=True)
    
    # Abas
    tab1, tab2, tab3, tab4 = st.tabs([
        "💬 Conversa",
        "🔍 Problemas",
        "🛠️ Resoluções",
        "📊 Dashboard"
    ])
    
    with tab1:
        render_chat_interface()
    
    with tab2:
        render_issues_tab()
    
    with tab3:
        render_resolutions_tab()
    
    with tab4:
        render_dashboard_tab()
    
    # Sidebar
    with st.sidebar:
        st.markdown("## ⚙️ Configurações")
        
        st.markdown("### 🔄 Ações Rápidas")
        if st.button("🔄 Executar Diagnóstico Completo"):
            run_diagnostic()
        
        if st.button("🔄 Atualizar Status"):
            status = st.session_state.orchestrator.get_system_status()
            st.json(status)
        
        st.markdown("### 📊 Informações")
        if st.session_state.diagnostic_run:
            summary = st.session_state.diagnostic_agent.get_summary()
            st.markdown(f"**Problemas encontrados:** {summary['total_issues']}")
            st.markdown(f"**Críticos:** {summary['critical']}")
            st.markdown(f"**Altos:** {summary['high']}")
            st.markdown(f"**Médios:** {summary['medium']}")
        
        st.markdown("### 🔗 Links Úteis")
        st.markdown("- [Documentação](./docs/AGENT_DASHBOARD_README.md)")
        st.markdown("- [Diagnostic Agent](./docs/DIAGNOSTIC_AGENT_README.md)")
        st.markdown("- [Resolution Agent](./docs/RESOLUTION_AGENT_README.md)")
        st.markdown("- [Database Manager](./docs/DB_MANAGER_README.md)")


if __name__ == "__main__":
    main()

