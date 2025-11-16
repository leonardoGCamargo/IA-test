"""
System Health Agent - Agente consolidado que combina:
- Diagnostic Agent (detecção de problemas)
- Helper System (monitoramento e otimização)
- Resolution Agent (geração de soluções)

Este agente unificado:
- Detecta problemas no sistema
- Monitora performance dos agentes
- Gera soluções automaticamente
- Otimiza configurações
"""

import os
import logging
from typing import Dict, List, Optional, Any, TypedDict, Annotated
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from dotenv import load_dotenv
import importlib.util

# Importa classes dos agentes originais para reutilizar
from src.agents.diagnostic_agent import (
    DiagnosticIssue, IssueSeverity, IssueCategory,
    DiagnosticAgent
)
from src.agents.resolution_agent import Resolution, ResolutionAgent
from src.agents.agent_helper_system import (
    AgentHelperSystem, AgentMetrics, AgentStatus,
    get_helper_system, get_monitor_helper
)

load_dotenv()
logger = logging.getLogger(__name__)


@dataclass
class SystemHealthReport:
    """Relatório completo de saúde do sistema."""
    diagnostic_issues: List[DiagnosticIssue]
    agent_metrics: Dict[str, AgentMetrics]
    resolutions: List[Resolution]
    optimizations: List[Dict[str, Any]]
    summary: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário."""
        return {
            "diagnostic_issues": [issue.to_dict() for issue in self.diagnostic_issues],
            "agent_metrics": {
                name: {
                    "name": m.name,
                    "status": m.status.value,
                    "performance_score": m.performance_score,
                    "error_count": m.error_count,
                    "success_count": m.success_count,
                    "avg_response_time": m.avg_response_time,
                    "issues": m.issues,
                    "suggestions": m.suggestions
                }
                for name, m in self.agent_metrics.items()
            },
            "resolutions": [r.to_dict() for r in self.resolutions],
            "optimizations": self.optimizations,
            "summary": self.summary,
            "timestamp": self.timestamp.isoformat()
        }


class SystemHealthAgent:
    """
    Agente consolidado de saúde do sistema.
    
    Combina funcionalidades de:
    - Diagnostic Agent: Detecta problemas
    - Helper System: Monitora e otimiza agentes
    - Resolution Agent: Gera soluções
    """
    
    def __init__(self):
        """Inicializa o agente de saúde do sistema."""
        # Componentes internos
        self.diagnostic = DiagnosticAgent()
        self.resolution = ResolutionAgent()
        self.helper = get_helper_system()
        
        logger.info("SystemHealthAgent inicializado (consolidado)")
    
    def run_full_health_check(self) -> SystemHealthReport:
        """
        Executa verificação completa de saúde do sistema.
        
        Returns:
            Relatório completo de saúde
        """
        logger.info("Executando verificação completa de saúde do sistema...")
        
        # 1. Diagnóstico de problemas
        diagnostic_issues = self.diagnostic.run_full_diagnostic()
        logger.info(f"Diagnóstico: {len(diagnostic_issues)} problemas encontrados")
        
        # 2. Monitoramento de agentes
        monitor = get_monitor_helper()
        agent_metrics = monitor.monitor_all_agents()
        logger.info(f"Monitoramento: {len(agent_metrics)} agentes monitorados")
        
        # 3. Geração de soluções
        resolutions = self.resolution.generate_resolutions(diagnostic_issues)
        logger.info(f"Resoluções: {len(resolutions)} soluções geradas")
        
        # 4. Otimizações
        optimizations = []
        for agent_name, metrics in agent_metrics.items():
            if metrics.status in [AgentStatus.WARNING, AgentStatus.ERROR]:
                opt_result = self.helper.optimizer.optimize_agent(agent_name)
                optimizations.append({
                    "agent": agent_name,
                    "optimization": opt_result
                })
        
        # 5. Resumo
        summary = {
            "total_issues": len(diagnostic_issues),
            "critical_issues": len([i for i in diagnostic_issues if i.severity == IssueSeverity.CRITICAL]),
            "high_issues": len([i for i in diagnostic_issues if i.severity == IssueSeverity.HIGH]),
            "total_agents": len(agent_metrics),
            "healthy_agents": len([m for m in agent_metrics.values() if m.status == AgentStatus.HEALTHY]),
            "warning_agents": len([m for m in agent_metrics.values() if m.status == AgentStatus.WARNING]),
            "error_agents": len([m for m in agent_metrics.values() if m.status == AgentStatus.ERROR]),
            "total_resolutions": len(resolutions),
            "total_optimizations": len(optimizations)
        }
        
        report = SystemHealthReport(
            diagnostic_issues=diagnostic_issues,
            agent_metrics=agent_metrics,
            resolutions=resolutions,
            optimizations=optimizations,
            summary=summary
        )
        
        logger.info(f"Verificação completa concluída: {summary}")
        return report
    
    def diagnose_issues(self) -> List[DiagnosticIssue]:
        """Executa apenas diagnóstico de problemas."""
        return self.diagnostic.run_full_diagnostic()
    
    def monitor_agents(self) -> Dict[str, AgentMetrics]:
        """Monitora todos os agentes."""
        monitor = get_monitor_helper()
        return monitor.monitor_all_agents()
    
    def generate_resolutions(self, issues: Optional[List[DiagnosticIssue]] = None) -> List[Resolution]:
        """
        Gera soluções para problemas.
        
        Args:
            issues: Lista de problemas (se None, executa diagnóstico primeiro)
            
        Returns:
            Lista de soluções
        """
        if issues is None:
            issues = self.diagnose_issues()
        return self.resolution.generate_resolutions(issues)
    
    def optimize_agent(self, agent_name: str) -> Dict[str, Any]:
        """Otimiza um agente específico."""
        return self.helper.optimizer.optimize_agent(agent_name)
    
    def get_agent_metrics(self, agent_name: str) -> Optional[AgentMetrics]:
        """Obtém métricas de um agente específico."""
        monitor = get_monitor_helper()
        return monitor.monitor_agent(agent_name)
    
    def get_critical_issues(self) -> List[DiagnosticIssue]:
        """Retorna apenas problemas críticos."""
        return self.diagnostic.get_critical_issues()
    
    def get_resolution(self, issue_id: str) -> Optional[Resolution]:
        """Obtém solução para um problema específico."""
        return self.resolution.get_resolution(issue_id)
    
    def get_summary(self) -> Dict[str, Any]:
        """Retorna resumo do estado do sistema."""
        issues = self.diagnose_issues()
        agents = self.monitor_agents()
        
        return {
            "diagnostic": self.diagnostic.get_summary(),
            "agents": {
                "total": len(agents),
                "healthy": len([m for m in agents.values() if m.status == AgentStatus.HEALTHY]),
                "warning": len([m for m in agents.values() if m.status == AgentStatus.WARNING]),
                "error": len([m for m in agents.values() if m.status == AgentStatus.ERROR])
            },
            "timestamp": datetime.now().isoformat()
        }


# Instância global
_system_health_agent_instance: Optional[SystemHealthAgent] = None


def get_system_health_agent() -> SystemHealthAgent:
    """Retorna a instância global do agente de saúde do sistema."""
    global _system_health_agent_instance
    if _system_health_agent_instance is None:
        _system_health_agent_instance = SystemHealthAgent()
    return _system_health_agent_instance

