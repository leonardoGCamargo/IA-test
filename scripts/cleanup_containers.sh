#!/bin/bash
# Script para limpar containers inúteis

echo "=== Limpando containers do n8n ==="
docker stop 8n8-n8n_webhook-1 8n8-n8n_worker-1 8n8-n8n_editor-1 2>/dev/null
docker rm 8n8-n8n_webhook-1 8n8-n8n_worker-1 8n8-n8n_editor-1 2>/dev/null
echo "Containers do n8n removidos"

echo "=== Limpando containers parados do Dokploy ==="
docker rm $(docker ps -a --filter "name=dokploy" --filter "status=exited" -q) 2>/dev/null
echo "Containers parados do Dokploy removidos"

echo "=== Limpando containers parados diversos ==="
docker rm cloudflared-cloudflared-1 cranky_proskuriakova wizardly_spence frosty_euler open-webui 2>/dev/null
echo "Containers parados removidos"

echo "=== Limpando containers parados ==="
docker container prune -f
echo "Limpeza concluída"

echo "=== Containers restantes ==="
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}"

