'use client';

import { useEffect, useState, useRef } from 'react';
import { io, Socket } from 'socket.io-client';

const WS_URL = process.env.NEXT_PUBLIC_WS_URL || 'http://localhost:8504';

export interface WebSocketMessage {
  type: string;
  agent_id?: string;
  task_id?: string;
  status?: string;
  message?: string;
  data?: any;
  timestamp: string;
}

export function useWebSocket() {
  const [messages, setMessages] = useState<WebSocketMessage[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const socketRef = useRef<Socket | null>(null);

  useEffect(() => {
    // Conectar ao Socket.IO
    const socket = io(WS_URL, {
      transports: ['websocket', 'polling'],
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionAttempts: 5,
      path: '/socket.io',
    });

    socketRef.current = socket;

    socket.on('connect', () => {
      console.log('Socket.IO conectado');
      setIsConnected(true);
    });

    socket.on('disconnect', () => {
      console.log('Socket.IO desconectado');
      setIsConnected(false);
    });

    socket.on('agent_status', (message: WebSocketMessage) => {
      setMessages((prev) => [...prev, message]);
    });

    socket.on('task_update', (message: WebSocketMessage) => {
      setMessages((prev) => [...prev, message]);
    });

    socket.on('system_event', (message: WebSocketMessage) => {
      setMessages((prev) => [...prev, message]);
    });

    socket.on('subscribed', (data: { agent_id: string }) => {
      console.log(`Inscrito no agente: ${data.agent_id}`);
    });

    return () => {
      socket.disconnect();
    };
  }, []);

  const sendMessage = (event: string, data: any) => {
    if (socketRef.current?.connected) {
      socketRef.current.emit(event, data);
    }
  };

  const subscribeToAgent = (agentId: string) => {
    if (socketRef.current?.connected) {
      socketRef.current.emit('subscribe_agent', { agent_id: agentId });
    }
  };

  return {
    messages,
    isConnected,
    sendMessage,
    subscribeToAgent,
  };
}

