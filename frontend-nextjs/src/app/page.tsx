import Link from 'next/link';
import { Activity, Brain, Database, Workflow } from 'lucide-react';

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <div className="container mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold text-white mb-4">
            IA-Test Multi-Agent System
          </h1>
          <p className="text-xl text-slate-300 mb-8">
            Dashboard profissional para gerenciamento de sistema multi-agente
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
          <Link
            href="/dashboard/agents"
            className="bg-white/10 backdrop-blur-lg rounded-lg p-6 hover:bg-white/20 transition-all border border-white/20"
          >
            <Brain className="w-12 h-12 text-purple-400 mb-4" />
            <h2 className="text-xl font-semibold text-white mb-2">Agentes</h2>
            <p className="text-slate-300 text-sm">
              Gerencie e monitore todos os agentes do sistema
            </p>
          </Link>

          <Link
            href="/dashboard/workflows"
            className="bg-white/10 backdrop-blur-lg rounded-lg p-6 hover:bg-white/20 transition-all border border-white/20"
          >
            <Workflow className="w-12 h-12 text-blue-400 mb-4" />
            <h2 className="text-xl font-semibold text-white mb-2">Workflows</h2>
            <p className="text-slate-300 text-sm">
              Visualize e execute workflows Kestra
            </p>
          </Link>

          <Link
            href="/dashboard/memory"
            className="bg-white/10 backdrop-blur-lg rounded-lg p-6 hover:bg-white/20 transition-all border border-white/20"
          >
            <Database className="w-12 h-12 text-green-400 mb-4" />
            <h2 className="text-xl font-semibold text-white mb-2">Memória</h2>
            <p className="text-slate-300 text-sm">
              Explore o grafo de conhecimento Neo4j
            </p>
          </Link>

          <Link
            href="/dashboard/monitoring"
            className="bg-white/10 backdrop-blur-lg rounded-lg p-6 hover:bg-white/20 transition-all border border-white/20"
          >
            <Activity className="w-12 h-12 text-yellow-400 mb-4" />
            <h2 className="text-xl font-semibold text-white mb-2">Monitoramento</h2>
            <p className="text-slate-300 text-sm">
              Métricas e observabilidade em tempo real
            </p>
          </Link>
        </div>

        <div className="bg-white/10 backdrop-blur-lg rounded-lg p-8 border border-white/20">
          <h2 className="text-2xl font-semibold text-white mb-4">
            Arquitetura do Sistema
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-slate-300">
            <div>
              <h3 className="font-semibold text-white mb-2">Frontend</h3>
              <ul className="space-y-1">
                <li>• Next.js 14+ (App Router)</li>
                <li>• TypeScript</li>
                <li>• React Query</li>
                <li>• WebSockets (real-time)</li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold text-white mb-2">Backend</h3>
              <ul className="space-y-1">
                <li>• FastAPI (Python)</li>
                <li>• LangGraph (agentes)</li>
                <li>• Neo4j (memória)</li>
                <li>• LangSmith (observabilidade)</li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold text-white mb-2">Orquestração</h3>
              <ul className="space-y-1">
                <li>• Kestra (workflows)</li>
                <li>• Docker Compose</li>
                <li>• MCP Servers</li>
                <li>• Integração completa</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

