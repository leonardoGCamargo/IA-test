"""
Sistema de Agentes Helper - Agentes especializados que ajudam nossos agentes principais.

Este módulo implementa agentes que:
- Monitoram e otimizam agentes existentes
- Fornecem feedback e sugestões de melhoria
- Ajudam a debugar e resolver problemas
- Ajustam configurações automaticamente
"""

from typing import Dict, List, Optional, Any, TypedDict, Annotated
from dataclasses import dataclass, field
from datetime import datetime
import json
import logging
from pathlib import Path
from enum import Enum

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langgraph.graph import StateGraph, END
from typing_extensions import TypedDict

from src.apps.chains import load_llm, load_embedding_model
from src.agents.orchestrator import get_orchestrator, AgentType

logger = logging.getLogger(__name__)


class AgentStatus(Enum):
    """Status de um agente."""
    HEALTHY = "healthy"
    WARNING = "warning"
    ERROR = "error"
    OPTIMIZING = "optimizing"


@dataclass
class AgentMetrics:
    """Métricas de um agente."""
    name: str
    status: AgentStatus
    performance_score: float = 0.0
    error_count: int = 0
    success_count: int = 0
    avg_response_time: float = 0.0
    last_check: datetime = field(default_factory=datetime.now)
    issues: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)


class AgentHelperState(TypedDict):
    """Estado do sistema de helpers."""
    target_agent: str
    metrics: Dict[str, Any]
    analysis: str
    recommendations: List[str]
    optimizations: List[Dict[str, Any]]


class AgentMonitorHelper:
    """Helper que monitora agentes e coleta métricas."""
    
    def __init__(self):
        """Inicializa o monitor."""
        self.metrics: Dict[str, AgentMetrics] = {}
        self.orchestrator = get_orchestrator()
        
        logger.info("AgentMonitorHelper inicializado")
    
    def monitor_agent(self, agent_name: str) -> AgentMetrics:
        """
        Monitora um agente específico.
        
        Args:
            agent_name: Nome do agente
            
        Returns:
            Métricas do agente
        """
        try:
            status = self.orchestrator.get_system_status()
            
            # Analisa status baseado no tipo de agente
            if agent_name == "mcp_manager":
                agent_data = status.get("mcp_manager", {})
                enabled_count = agent_data.get("enabled_count", 0)
                total_count = agent_data.get("servers_count", 0)
                
                performance = (enabled_count / total_count * 100) if total_count > 0 else 0
                agent_status = AgentStatus.HEALTHY if performance > 50 else AgentStatus.WARNING
                
                issues = []
                if total_count == 0:
                    issues.append("Nenhum servidor MCP configurado")
                if enabled_count == 0 and total_count > 0:
                    issues.append("Nenhum servidor MCP habilitado")
                
            elif agent_name == "neo4j":
                agent_data = status.get("neo4j", {})
                available = agent_data.get("available", False)
                
                performance = 100 if available else 0
                agent_status = AgentStatus.HEALTHY if available else AgentStatus.ERROR
                
                issues = [] if available else ["Neo4j não está disponível"]
                
            elif agent_name == "kestra":
                agent_data = status.get("kestra", {})
                available = agent_data.get("available", False)
                workflows_count = agent_data.get("workflows_count", 0)
                
                performance = 100 if available else 0
                agent_status = AgentStatus.HEALTHY if available else AgentStatus.WARNING
                
                issues = []
                if not available:
                    issues.append("Kestra não está disponível")
                if available and workflows_count == 0:
                    issues.append("Nenhum workflow Kestra configurado")
                
            else:
                performance = 50
                agent_status = AgentStatus.WARNING
                issues = ["Agente desconhecido"]
            
            metrics = AgentMetrics(
                name=agent_name,
                status=agent_status,
                performance_score=performance,
                last_check=datetime.now(),
                issues=issues
            )
            
            self.metrics[agent_name] = metrics
            logger.info(f"Métricas coletadas para {agent_name}: {metrics.status.value}")
            
            return metrics
            
        except Exception as e:
            logger.error(f"Erro ao monitorar agente {agent_name}: {e}")
            return AgentMetrics(
                name=agent_name,
                status=AgentStatus.ERROR,
                issues=[f"Erro ao monitorar: {str(e)}"]
            )
    
    def monitor_all_agents(self) -> Dict[str, AgentMetrics]:
        """Monitora todos os agentes."""
        agents = ["mcp_manager", "neo4j", "kestra", "obsidian", "docker"]
        all_metrics = {}
        
        for agent_name in agents:
            all_metrics[agent_name] = self.monitor_agent(agent_name)
        
        return all_metrics
    
    def get_metrics_report(self) -> Dict[str, Any]:
        """Gera relatório de métricas."""
        all_metrics = self.monitor_all_agents()
        
        total_agents = len(all_metrics)
        healthy_count = sum(1 for m in all_metrics.values() if m.status == AgentStatus.HEALTHY)
        warning_count = sum(1 for m in all_metrics.values() if m.status == AgentStatus.WARNING)
        error_count = sum(1 for m in all_metrics.values() if m.status == AgentStatus.ERROR)
        
        avg_performance = sum(m.performance_score for m in all_metrics.values()) / total_agents if total_agents > 0 else 0
        
        return {
            "total_agents": total_agents,
            "healthy_count": healthy_count,
            "warning_count": warning_count,
            "error_count": error_count,
            "avg_performance": avg_performance,
            "agents": {name: {
                "status": m.status.value,
                "performance_score": m.performance_score,
                "issues": m.issues,
                "suggestions": m.suggestions
            } for name, m in all_metrics.items()}
        }


class AgentOptimizerHelper:
    """Helper que otimiza agentes usando LangChain."""
    
    def __init__(self, llm_name: Optional[str] = None):
        """
        Inicializa o otimizador.
        
        Args:
            llm_name: Nome do modelo LLM
        """
        import os
        from dotenv import load_dotenv
        load_dotenv()
        
        self.llm_name = llm_name or os.getenv("LLM", "llama2")
        self.ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        
        try:
            self.llm = load_llm(
                self.llm_name,
                logger=logger,
                config={"ollama_base_url": self.ollama_base_url}
            )
            logger.info(f"AgentOptimizerHelper inicializado com LLM: {self.llm_name}")
        except Exception as e:
            logger.error(f"Erro ao carregar LLM: {e}")
            raise
        
        self.monitor = AgentMonitorHelper()
        self.orchestrator = get_orchestrator()
        
        # Constrói grafo de otimização
        self.optimizer_graph = self._build_optimizer_graph()
    
    def _build_optimizer_graph(self) -> StateGraph:
        """Constrói grafo de otimização."""
        
        def analyze(state: AgentHelperState) -> AgentHelperState:
            """Analisa métricas e identifica problemas."""
            target_agent = state["target_agent"]
            metrics = state.get("metrics", {})
            
            analysis_prompt = ChatPromptTemplate.from_messages([
                ("system", """Você é um especialista em análise de sistemas.
Analise as métricas do agente e identifique problemas e oportunidades de melhoria."""),
                ("human", f"Agente: {target_agent}\n\nMétricas: {json.dumps(metrics, indent=2)}\n\nAnalise e forneça recomendações.")
            ])
            
            chain = analysis_prompt | self.llm | StrOutputParser()
            analysis = chain.invoke({"target_agent": target_agent, "metrics": metrics})
            
            return {
                **state,
                "analysis": analysis
            }
        
        def recommend(state: AgentHelperState) -> AgentHelperState:
            """Gera recomendações de otimização."""
            analysis = state.get("analysis", "")
            target_agent = state["target_agent"]
            
            recommendation_prompt = ChatPromptTemplate.from_messages([
                ("system", """Você é um consultor especializado em otimização de sistemas.
Baseado na análise, forneça recomendações práticas e acionáveis em JSON:
{
    "recommendations": [
        {"priority": "high|medium|low", "action": "descrição", "impact": "descrição"},
        ...
    ]
}"""),
                ("human", f"Análise: {analysis}\n\nAgente: {target_agent}\n\nRecomendações:")
            ])
            
            chain = recommendation_prompt | self.llm | StrOutputParser()
            recommendations_text = chain.invoke({"analysis": analysis, "target_agent": target_agent})
            
            # Extrai recomendações
            try:
                import re
                json_match = re.search(r'\{.*\}', recommendations_text, re.DOTALL)
                if json_match:
                    recommendations_data = json.loads(json_match.group())
                    recommendations = recommendations_data.get("recommendations", [])
                else:
                    recommendations = [{"priority": "medium", "action": recommendations_text, "impact": "unknown"}]
            except:
                recommendations = [{"priority": "medium", "action": recommendations_text, "impact": "unknown"}]
            
            return {
                **state,
                "recommendations": recommendations
            }
        
        def optimize(state: AgentHelperState) -> AgentHelperState:
            """Aplica otimizações."""
            recommendations = state.get("recommendations", [])
            target_agent = state["target_agent"]
            
            optimizations = []
            for rec in recommendations:
                if rec.get("priority") == "high":
                    # Aplica otimização automática
                    optimization = {
                        "agent": target_agent,
                        "action": rec.get("action", ""),
                        "status": "applied",
                        "timestamp": datetime.now().isoformat()
                    }
                    optimizations.append(optimization)
            
            return {
                **state,
                "optimizations": optimizations
            }
        
        # Constrói grafo
        workflow = StateGraph(AgentHelperState)
        
        workflow.add_node("analyze", analyze)
        workflow.add_node("recommend", recommend)
        workflow.add_node("optimize", optimize)
        
        workflow.set_entry_point("analyze")
        workflow.add_edge("analyze", "recommend")
        workflow.add_edge("recommend", "optimize")
        workflow.add_edge("optimize", END)
        
        return workflow.compile()
    
    def optimize_agent(self, agent_name: str) -> Dict[str, Any]:
        """
        Otimiza um agente específico.
        
        Args:
            agent_name: Nome do agente
            
        Returns:
            Resultado da otimização
        """
        logger.info(f"Otimizando agente: {agent_name}")
        
        # Coleta métricas
        metrics = self.monitor.monitor_agent(agent_name)
        metrics_dict = {
            "status": metrics.status.value,
            "performance_score": metrics.performance_score,
            "issues": metrics.issues
        }
        
        initial_state = {
            "target_agent": agent_name,
            "metrics": metrics_dict,
            "analysis": "",
            "recommendations": [],
            "optimizations": []
        }
        
        try:
            result = self.optimizer_graph.invoke(initial_state)
            
            return {
                "agent": agent_name,
                "analysis": result.get("analysis", ""),
                "recommendations": result.get("recommendations", []),
                "optimizations": result.get("optimizations", [])
            }
        except Exception as e:
            logger.error(f"Erro ao otimizar agente {agent_name}: {e}")
            return {
                "agent": agent_name,
                "error": str(e)
            }


class AgentTunerHelper:
    """Helper que ajusta configurações de agentes automaticamente."""
    
    def __init__(self, llm_name: Optional[str] = None):
        """
        Inicializa o tuner.
        
        Args:
            llm_name: Nome do modelo LLM
        """
        import os
        from dotenv import load_dotenv
        load_dotenv()
        
        self.llm_name = llm_name or os.getenv("LLM", "llama2")
        self.ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        
        try:
            self.llm = load_llm(
                self.llm_name,
                logger=logger,
                config={"ollama_base_url": self.ollama_base_url}
            )
            logger.info(f"AgentTunerHelper inicializado")
        except Exception as e:
            logger.error(f"Erro ao carregar LLM: {e}")
            raise
        
        self.monitor = AgentMonitorHelper()
    
    def tune_agent_prompt(self, agent_name: str, current_behavior: str, desired_behavior: str) -> str:
        """
        Ajusta prompt de um agente.
        
        Args:
            agent_name: Nome do agente
            current_behavior: Comportamento atual
            desired_behavior: Comportamento desejado
            
        Returns:
            Prompt ajustado
        """
        tuning_prompt = ChatPromptTemplate.from_messages([
            ("system", """Você é um especialista em ajuste fino de prompts.
Ajuste o prompt para melhorar o comportamento do agente mantendo a funcionalidade original."""),
            ("human", f"""Agente: {agent_name}
Comportamento Atual: {current_behavior}
Comportamento Desejado: {desired_behavior}

Ajuste o prompt do agente:""")
        ])
        
        chain = tuning_prompt | self.llm | StrOutputParser()
        tuned_prompt = chain.invoke({
            "agent_name": agent_name,
            "current_behavior": current_behavior,
            "desired_behavior": desired_behavior
        })
        
        logger.info(f"Prompt ajustado para {agent_name}")
        return tuned_prompt
    
    def tune_agent_config(self, agent_name: str, current_config: Dict[str, Any], issues: List[str]) -> Dict[str, Any]:
        """
        Ajusta configuração de um agente.
        
        Args:
            agent_name: Nome do agente
            current_config: Configuração atual
            issues: Problemas identificados
            
        Returns:
            Configuração ajustada
        """
        tuning_prompt = ChatPromptTemplate.from_messages([
            ("system", """Você é um especialista em configuração de sistemas.
Ajuste a configuração para resolver os problemas identificados."""),
            ("human", f"""Agente: {agent_name}
Configuração Atual: {json.dumps(current_config, indent=2)}
Problemas: {', '.join(issues)}

Forneça configuração ajustada em JSON:""")
        ])
        
        chain = tuning_prompt | self.llm | StrOutputParser()
        tuned_config_text = chain.invoke({
            "agent_name": agent_name,
            "current_config": current_config,
            "issues": issues
        })
        
        try:
            import re
            json_match = re.search(r'\{.*\}', tuned_config_text, re.DOTALL)
            if json_match:
                tuned_config = json.loads(json_match.group())
                logger.info(f"Configuração ajustada para {agent_name}")
                return tuned_config
            else:
                return current_config
        except:
            logger.warning(f"Não foi possível parsear configuração ajustada para {agent_name}")
            return current_config


class AgentHelperSystem:
    """Sistema completo de helpers para agentes."""
    
    def __init__(self):
        """Inicializa o sistema de helpers."""
        self.monitor = AgentMonitorHelper()
        self.optimizer = AgentOptimizerHelper()
        self.tuner = AgentTunerHelper()
        
        logger.info("AgentHelperSystem inicializado")
    
    def get_full_report(self) -> Dict[str, Any]:
        """Gera relatório completo do sistema."""
        metrics_report = self.monitor.get_metrics_report()
        
        # Otimiza agentes com problemas
        agents_needing_optimization = [
            name for name, data in metrics_report.get("agents", {}).items()
            if data.get("status") in ["warning", "error"]
        ]
        
        optimizations = {}
        for agent_name in agents_needing_optimization:
            optimizations[agent_name] = self.optimizer.optimize_agent(agent_name)
        
        return {
            "metrics": metrics_report,
            "optimizations": optimizations,
            "timestamp": datetime.now().isoformat()
        }


# Instâncias globais
_monitor_helper_instance: Optional[AgentMonitorHelper] = None
_optimizer_helper_instance: Optional[AgentOptimizerHelper] = None
_tuner_helper_instance: Optional[AgentTunerHelper] = None
_helper_system_instance: Optional[AgentHelperSystem] = None


def get_monitor_helper() -> AgentMonitorHelper:
    """Retorna instância global do monitor."""
    global _monitor_helper_instance
    if _monitor_helper_instance is None:
        _monitor_helper_instance = AgentMonitorHelper()
    return _monitor_helper_instance


def get_optimizer_helper() -> AgentOptimizerHelper:
    """Retorna instância global do otimizador."""
    global _optimizer_helper_instance
    if _optimizer_helper_instance is None:
        _optimizer_helper_instance = AgentOptimizerHelper()
    return _optimizer_helper_instance


def get_tuner_helper() -> AgentTunerHelper:
    """Retorna instância global do tuner."""
    global _tuner_helper_instance
    if _tuner_helper_instance is None:
        _tuner_helper_instance = AgentTunerHelper()
    return _tuner_helper_instance


def get_helper_system() -> AgentHelperSystem:
    """Retorna instância global do sistema de helpers."""
    global _helper_system_instance
    if _helper_system_instance is None:
        _helper_system_instance = AgentHelperSystem()
    return _helper_system_instance

