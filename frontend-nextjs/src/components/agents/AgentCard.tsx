'use client';

import { Brain, Play, CheckCircle, XCircle, Clock } from 'lucide-react';

interface AgentCardProps {
  agent: {
    id: string;
    name: string;
    type: string;
    status: string;
    description?: string;
  };
  onExecute: () => void;
}

export function AgentCard({ agent, onExecute }: AgentCardProps) {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'text-green-400';
      case 'idle':
        return 'text-yellow-400';
      case 'error':
        return 'text-red-400';
      default:
        return 'text-slate-400';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'active':
        return <CheckCircle className="w-4 h-4 text-green-400" />;
      case 'error':
        return <XCircle className="w-4 h-4 text-red-400" />;
      default:
        return <Clock className="w-4 h-4 text-yellow-400" />;
    }
  };

  return (
    <div className="bg-slate-800 rounded-lg p-6 border border-slate-700 hover:border-purple-500 transition-all">
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <Brain className="w-8 h-8 text-purple-400" />
          <div>
            <h3 className="text-lg font-semibold text-white">{agent.name}</h3>
            <p className="text-sm text-slate-400">{agent.type}</p>
          </div>
        </div>
        {getStatusIcon(agent.status)}
      </div>

      {agent.description && (
        <p className="text-slate-300 text-sm mb-4">{agent.description}</p>
      )}

      <div className="flex items-center justify-between">
        <span className={`text-sm font-medium ${getStatusColor(agent.status)}`}>
          {agent.status}
        </span>
        <button
          onClick={onExecute}
          className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 flex items-center gap-2 text-sm"
        >
          <Play className="w-4 h-4" />
          Executar
        </button>
      </div>
    </div>
  );
}

