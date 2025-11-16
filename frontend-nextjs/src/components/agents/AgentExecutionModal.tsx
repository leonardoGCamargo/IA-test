'use client';

import { useState, useEffect } from 'react';
import { X, Send, Loader2 } from 'lucide-react';
import { api } from '@/lib/api';
import { useWebSocket } from '@/hooks/useWebSocket';

interface AgentExecutionModalProps {
  agentId: string;
  onClose: () => void;
  messages: any[];
}

export function AgentExecutionModal({
  agentId,
  onClose,
  messages: propMessages,
}: AgentExecutionModalProps) {
  const [goal, setGoal] = useState('');
  const [isExecuting, setIsExecuting] = useState(false);
  const [result, setResult] = useState<any>(null);
  const { messages, subscribeToAgent } = useWebSocket();

  useEffect(() => {
    subscribeToAgent(agentId);
  }, [agentId, subscribeToAgent]);

  const agentMessages = messages.filter((m) => m.agent_id === agentId);

  const handleExecute = async () => {
    if (!goal.trim()) return;

    setIsExecuting(true);
    setResult(null);

    try {
      const response = await api.executeAgent(agentId, goal);
      setResult(response);
    } catch (error: any) {
      setResult({ error: error.message || 'Erro ao executar agente' });
    } finally {
      setIsExecuting(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-slate-800 rounded-lg w-full max-w-4xl max-h-[90vh] flex flex-col border border-slate-700">
        <div className="flex items-center justify-between p-6 border-b border-slate-700">
          <h2 className="text-2xl font-bold text-white">Executar Agente</h2>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-white transition-colors"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">
              Objetivo / Tarefa
            </label>
            <textarea
              value={goal}
              onChange={(e) => setGoal(e.target.value)}
              placeholder="Descreva o que você quer que o agente faça..."
              className="w-full bg-slate-900 text-white rounded-lg p-4 border border-slate-700 focus:border-purple-500 focus:outline-none resize-none"
              rows={4}
            />
          </div>

          {result && (
            <div className="bg-slate-900 rounded-lg p-4 border border-slate-700">
              <h3 className="text-lg font-semibold text-white mb-2">Resultado</h3>
              <pre className="text-sm text-slate-300 whitespace-pre-wrap">
                {JSON.stringify(result, null, 2)}
              </pre>
            </div>
          )}

          {agentMessages.length > 0 && (
            <div className="bg-slate-900 rounded-lg p-4 border border-slate-700">
              <h3 className="text-lg font-semibold text-white mb-2">
                Mensagens em Tempo Real
              </h3>
              <div className="space-y-2 max-h-64 overflow-y-auto">
                {agentMessages.map((msg, idx) => (
                  <div
                    key={idx}
                    className="text-sm text-slate-300 bg-slate-800 rounded p-2"
                  >
                    <div className="text-xs text-slate-500 mb-1">
                      {msg.timestamp ? new Date(msg.timestamp).toLocaleTimeString() : 'Agora'}
                    </div>
                    <div>{msg.message || JSON.stringify(msg.data || msg)}</div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        <div className="p-6 border-t border-slate-700 flex items-center justify-end gap-4">
          <button
            onClick={onClose}
            className="px-4 py-2 text-slate-300 hover:text-white transition-colors"
          >
            Fechar
          </button>
          <button
            onClick={handleExecute}
            disabled={!goal.trim() || isExecuting}
            className="px-6 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
          >
            {isExecuting ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                Executando...
              </>
            ) : (
              <>
                <Send className="w-4 h-4" />
                Executar
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}

