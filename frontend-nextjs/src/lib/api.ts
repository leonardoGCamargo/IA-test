import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8504';

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const api = {
  // Agents
  getAgents: async () => {
    const { data } = await apiClient.get('/api/v1/agents');
    return data;
  },

  getAgent: async (agentId: string) => {
    const { data } = await apiClient.get(`/api/v1/agents/${agentId}`);
    return data;
  },

  executeAgent: async (agentId: string, goal: string, parameters?: Record<string, any>) => {
    const { data } = await apiClient.post(`/api/v1/agents/${agentId}/execute`, {
      goal,
      parameters: parameters || {},
    });
    return data;
  },

  getAgentStatus: async (agentId: string) => {
    const { data } = await apiClient.get(`/api/v1/agents/${agentId}/status`);
    return data;
  },

  // System Status
  getSystemStatus: async () => {
    const { data } = await apiClient.get('/api/v1/system/status');
    return data;
  },

  // Tasks
  getTasks: async () => {
    const { data } = await apiClient.get('/api/v1/tasks');
    return data;
  },

  getTask: async (taskId: string) => {
    const { data } = await apiClient.get(`/api/v1/tasks/${taskId}`);
    return data;
  },

  // Workflows (Kestra)
  getWorkflows: async () => {
    const { data } = await apiClient.get('/api/v1/workflows');
    return data;
  },

  executeWorkflow: async (workflowId: string, inputs?: Record<string, any>) => {
    const { data } = await apiClient.post(`/api/v1/workflows/${workflowId}/execute`, {
      inputs: inputs || {},
    });
    return data;
  },

  // Neo4j Memory
  queryMemory: async (query: string, limit: number = 10) => {
    const { data } = await apiClient.post('/api/v1/memory/query', {
      query,
      limit,
    });
    return data;
  },

  // LangSmith Traces
  getTraces: async (limit: number = 50) => {
    const { data } = await apiClient.get(`/api/v1/traces?limit=${limit}`);
    return data;
  },
};

