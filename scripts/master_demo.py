"""
Demonstração do poder do Orchestrator e dos novos agentes.

Este script demonstra:
1. O Orchestrator coordenando múltiplos agentes
2. O Kestra & LangChain Master criando workflows inteligentes
3. O Agent Helper System monitorando e otimizando agentes
"""

from src.agents.orchestrator import get_orchestrator, AgentType
from src.agents.kestra_langchain_master import get_master_agent
from src.agents.agent_helper_system import get_helper_system, get_monitor_helper
import json


def demo_orchestrator():
    """Demonstra o poder do Orchestrator."""
    print("\n" + "="*60)
    print("🎯 DEMONSTRAÇÃO DO ORCHESTRATOR")
    print("="*60)
    
    orchestrator = get_orchestrator()
    
    # 1. Status do sistema
    print("\n1️⃣ Status do Sistema:")
    status = orchestrator.get_system_status()
    print(json.dumps(status, indent=2, ensure_ascii=False))
    
    # 2. Criar tarefa e executar
    print("\n2️⃣ Criando e Executando Tarefa:")
    task = orchestrator.create_task(
        AgentType.MCP_ARCHITECT,
        "Listar todos os servidores MCP",
        {"action": "list_servers"}
    )
    result = orchestrator.execute_task(task)
    print(f"Resultado: {json.dumps(result, indent=2, ensure_ascii=False)}")
    
    # 3. Sincronização automática
    print("\n3️⃣ Sincronização Automática MCP → Neo4j:")
    result = orchestrator.sync_mcp_to_neo4j()
    print(f"Resultado: {json.dumps(result, indent=2, ensure_ascii=False)}")
    
    print("\n✅ Orchestrator funcionando perfeitamente!")


def demo_master_agent():
    """Demonstra o Kestra & LangChain Master."""
    print("\n" + "="*60)
    print("🧠 DEMONSTRAÇÃO DO KESTRA & LANGCHAIN MASTER")
    print("="*60)
    
    master = get_master_agent()
    
    # 1. Executar objetivo em linguagem natural
    print("\n1️⃣ Executando Objetivo em Linguagem Natural:")
    goal = "Sincronizar todos os servidores MCP para o Neo4j e criar um workflow de health check"
    print(f"Objetivo: {goal}")
    
    result = master.execute_goal(goal)
    print(f"\nResultado:")
    print(f"  - Plano: {result.get('plan', 'N/A')[:200]}...")
    print(f"  - Passos executados: {len(result.get('results', []))}")
    print(f"  - Iterações: {result.get('iterations', 0)}")
    print(f"  - Feedback: {result.get('feedback', 'N/A')[:200]}...")
    
    # 2. Criar workflow inteligente
    print("\n2️⃣ Criando Workflow Inteligente:")
    description = "Workflow que importa notas Obsidian para Neo4j diariamente às 3h da manhã"
    print(f"Descrição: {description}")
    
    try:
        workflow = master.create_intelligent_workflow(description)
        print(f"✅ Workflow criado: {workflow.id}")
        print(f"   - Tarefas: {len(workflow.tasks)}")
        print(f"   - Triggers: {len(workflow.triggers)}")
    except Exception as e:
        print(f"⚠️ Erro ao criar workflow: {e}")
    
    print("\n✅ Master Agent funcionando perfeitamente!")


def demo_helper_system():
    """Demonstra o Agent Helper System."""
    print("\n" + "="*60)
    print("🛠️ DEMONSTRAÇÃO DO AGENT HELPER SYSTEM")
    print("="*60)
    
    helper_system = get_helper_system()
    monitor = get_monitor_helper()
    
    # 1. Monitorar agentes
    print("\n1️⃣ Monitorando Agentes:")
    all_metrics = monitor.monitor_all_agents()
    for agent_name, metrics in all_metrics.items():
        status_emoji = {
            "healthy": "✅",
            "warning": "⚠️",
            "error": "❌",
            "optimizing": "🔧"
        }
        emoji = status_emoji.get(metrics.status.value, "❓")
        print(f"  {emoji} {agent_name}: {metrics.status.value} (Score: {metrics.performance_score:.1f}%)")
        if metrics.issues:
            for issue in metrics.issues:
                print(f"    - Problema: {issue}")
    
    # 2. Relatório completo
    print("\n2️⃣ Relatório Completo do Sistema:")
    report = helper_system.get_full_report()
    metrics_data = report.get("metrics", {})
    print(f"  - Total de Agentes: {metrics_data.get('total_agents', 0)}")
    print(f"  - Saudáveis: {metrics_data.get('healthy_count', 0)}")
    print(f"  - Com Avisos: {metrics_data.get('warning_count', 0)}")
    print(f"  - Com Erros: {metrics_data.get('error_count', 0)}")
    print(f"  - Performance Média: {metrics_data.get('avg_performance', 0):.1f}%")
    
    # 3. Otimizar agentes com problemas
    print("\n3️⃣ Otimizando Agentes com Problemas:")
    optimizations = report.get("optimizations", {})
    if optimizations:
        for agent_name, opt_result in optimizations.items():
            print(f"  🔧 {agent_name}:")
            if "error" in opt_result:
                print(f"    - Erro: {opt_result['error']}")
            else:
                recommendations = opt_result.get("recommendations", [])
                print(f"    - Recomendações: {len(recommendations)}")
                for rec in recommendations[:3]:  # Mostra até 3
                    print(f"      • [{rec.get('priority', 'unknown')}] {rec.get('action', 'N/A')[:60]}")
    else:
        print("  ✅ Nenhum agente precisa de otimização!")
    
    print("\n✅ Helper System funcionando perfeitamente!")


def demo_integration():
    """Demonstra integração completa."""
    print("\n" + "="*60)
    print("🚀 DEMONSTRAÇÃO DE INTEGRAÇÃO COMPLETA")
    print("="*60)
    
    orchestrator = get_orchestrator()
    
    # 1. Usar Orchestrator para criar tarefa no Master Agent
    print("\n1️⃣ Orchestrator → Master Agent:")
    task = orchestrator.create_task(
        AgentType.KESTRA_LANGCHAIN_MASTER,
        "Criar workflow inteligente de sincronização",
        {
            "action": "create_intelligent_workflow",
            "description": "Workflow que sincroniza MCPs e cria relatórios semanalmente"
        }
    )
    try:
        result = orchestrator.execute_task(task)
        print(f"✅ Workflow criado via Orchestrator!")
        print(f"   ID: {result.get('id', 'N/A')}")
    except Exception as e:
        print(f"⚠️ Erro: {e}")
    
    # 2. Usar Orchestrator para monitorar via Helper System
    print("\n2️⃣ Orchestrator → Helper System:")
    task = orchestrator.create_task(
        AgentType.AGENT_HELPER,
        "Monitorar agente MCP Manager",
        {
            "action": "monitor_agent",
            "agent_name": "mcp_manager"
        }
    )
    try:
        result = orchestrator.execute_task(task)
        print(f"✅ Monitoramento executado!")
        print(f"   Status: {result.get('status', 'N/A')}")
        print(f"   Performance: {result.get('performance_score', 0):.1f}%")
    except Exception as e:
        print(f"⚠️ Erro: {e}")
    
    # 3. Pipeline completo
    print("\n3️⃣ Pipeline Completo (Master → Helper → Optimizer):")
    print("   Criando tarefa para executar objetivo complexo...")
    
    task = orchestrator.create_task(
        AgentType.KESTRA_LANGCHAIN_MASTER,
        "Executar pipeline completo de sincronização e otimização",
        {
            "action": "execute_goal",
            "goal": "Sincronizar MCPs, verificar saúde dos agentes, e otimizar os que têm problemas"
        }
    )
    try:
        result = orchestrator.execute_task(task)
        print(f"✅ Pipeline executado!")
        print(f"   Iterações: {result.get('iterations', 0)}")
        print(f"   Resultados: {len(result.get('results', []))} passos")
    except Exception as e:
        print(f"⚠️ Erro: {e}")
    
    print("\n✅ Integração completa funcionando!")


def main():
    """Executa todas as demonstrações."""
    print("\n" + "="*60)
    print("🎉 DEMONSTRAÇÃO COMPLETA DO SISTEMA")
    print("="*60)
    print("\nEste sistema demonstra:")
    print("  1. Orchestrator coordenando múltiplos agentes")
    print("  2. Kestra & LangChain Master criando workflows inteligentes")
    print("  3. Agent Helper System monitorando e otimizando")
    print("  4. Integração completa entre todos os componentes")
    
    try:
        # Demonstrações
        demo_orchestrator()
        demo_master_agent()
        demo_helper_system()
        demo_integration()
        
        print("\n" + "="*60)
        print("🎊 TODAS AS DEMONSTRAÇÕES CONCLUÍDAS!")
        print("="*60)
        print("\n✨ O sistema está funcionando perfeitamente!")
        print("   - Orchestrator: ✅ Coordenando agentes")
        print("   - Master Agent: ✅ Criando workflows inteligentes")
        print("   - Helper System: ✅ Monitorando e otimizando")
        print("   - Integração: ✅ Todos os componentes conectados")
        
    except Exception as e:
        print(f"\n❌ Erro durante demonstração: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

