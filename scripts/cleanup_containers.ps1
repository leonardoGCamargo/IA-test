# Script PowerShell para limpar containers inúteis

Write-Host "=== Limpando containers do n8n ===" -ForegroundColor Yellow
docker stop 8n8-n8n_webhook-1 8n8-n8n_worker-1 8n8-n8n_editor-1 2>$null
docker rm 8n8-n8n_webhook-1 8n8-n8n_worker-1 8n8-n8n_editor-1 2>$null
Write-Host "Containers do n8n removidos" -ForegroundColor Green

Write-Host "=== Limpando containers parados do Dokploy ===" -ForegroundColor Yellow
$dokployStopped = docker ps -a --filter "name=dokploy" --filter "status=exited" -q
if ($dokployStopped) {
    docker rm $dokployStopped 2>$null
    Write-Host "Containers parados do Dokploy removidos" -ForegroundColor Green
} else {
    Write-Host "Nenhum container parado do Dokploy encontrado" -ForegroundColor Gray
}

Write-Host "=== Limpando containers parados diversos ===" -ForegroundColor Yellow
docker rm cloudflared-cloudflared-1 cranky_proskuriakova wizardly_spence frosty_euler open-webui 2>$null
Write-Host "Containers parados removidos" -ForegroundColor Green

Write-Host "=== Limpando containers com nomes aleatórios do projeto ===" -ForegroundColor Yellow
$randomContainers = @(
    "strange_roentgen", "keen_volhard", "elastic_sinoussi", "nifty_jemison",
    "sweet_khorana", "gallant_mahavira", "dazzling_perlman", "quizzical_blackwell"
)

foreach ($container in $randomContainers) {
    $exists = docker ps -a --filter "name=$container" -q
    if ($exists) {
        Write-Host "Parando e removendo $container..." -ForegroundColor Yellow
        docker stop $container 2>$null
        docker rm $container 2>$null
    }
}

Write-Host "=== Limpando containers parados ===" -ForegroundColor Yellow
docker container prune -f
Write-Host "Limpeza concluída" -ForegroundColor Green

Write-Host "`n=== Containers restantes ===" -ForegroundColor Cyan
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}"

