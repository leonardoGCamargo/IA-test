'use client';

import { useQuery } from '@tanstack/react-query';
import { useState } from 'react';
import { Brain, Play, Square, RefreshCw } from 'lucide-react';
import { AgentCard } from '@/components/agents/AgentCard';
import { AgentExecutionModal } from '@/components/agents/AgentExecutionModal';
import { api } from '@/lib/api';

export default function AgentsPage() {
  const [selectedAgent, setSelectedAgent] = useState<string | null>(null);

  const { data: agents, isLoading, refetch } = useQuery({
    queryKey: ['agents'],
    queryFn: () => api.getAgents(),
  });

  const { data: systemStatus } = useQuery({
    queryKey: ['system-status'],
    queryFn: () => api.getSystemStatus(),
    refetchInterval: 5000, // Atualiza a cada 5 segundos
  });

  if (isLoading) {
    return (
      <div className="min-h-screen bg-slate-900 p-8">
        <div className="container mx-auto">
          <div className="text-white">Carregando agentes...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-900 p-8">
      <div className="container mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-4 flex items-center gap-3">
            <Brain className="w-10 h-10 text-purple-400" />
            Gerenciamento de Agentes
          </h1>
          <div className="flex gap-4 mb-4">
            <button
              onClick={() => refetch()}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 flex items-center gap-2"
            >
              <RefreshCw className="w-4 h-4" />
              Atualizar
            </button>
          </div>
        </div>

        {systemStatus && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
            <div className="bg-slate-800 rounded-lg p-4 border border-slate-700">
              <div className="text-slate-400 text-sm">Total de Agentes</div>
              <div className="text-2xl font-bold text-white">
                {systemStatus.total_agents || 0}
              </div>
            </div>
            <div className="bg-slate-800 rounded-lg p-4 border border-slate-700">
              <div className="text-slate-400 text-sm">Agentes Ativos</div>
              <div className="text-2xl font-bold text-green-400">
                {systemStatus.active_agents || 0}
              </div>
            </div>
            <div className="bg-slate-800 rounded-lg p-4 border border-slate-700">
              <div className="text-slate-400 text-sm">Tarefas Pendentes</div>
              <div className="text-2xl font-bold text-yellow-400">
                {systemStatus.pending_tasks || 0}
              </div>
            </div>
            <div className="bg-slate-800 rounded-lg p-4 border border-slate-700">
              <div className="text-slate-400 text-sm">Tarefas Concluídas</div>
              <div className="text-2xl font-bold text-blue-400">
                {systemStatus.completed_tasks || 0}
              </div>
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {agents?.map((agent: any) => (
            <AgentCard
              key={agent.id}
              agent={agent}
              onExecute={() => setSelectedAgent(agent.id)}
            />
          ))}
        </div>

        {selectedAgent && (
          <AgentExecutionModal
            agentId={selectedAgent}
            onClose={() => setSelectedAgent(null)}
            messages={[]}
          />
        )}
      </div>
    </div>
  );
}

