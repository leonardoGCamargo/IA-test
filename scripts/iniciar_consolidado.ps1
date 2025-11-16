# Script PowerShell para iniciar configuração consolidada
# Remove serviços do Swarm e inicia docker-compose

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  INICIANDO CONFIGURACAO CONSOLIDADA" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verifica se há serviços do Swarm
Write-Host "Verificando servicos do Swarm..." -ForegroundColor Yellow
$services = docker service ls --format "{{.Name}}" 2>$null | Where-Object { $_ -match "dokploy" }

if ($services) {
    Write-Host "Servicos do Swarm encontrados:" -ForegroundColor Yellow
    $services | ForEach-Object { Write-Host "  - $_" -ForegroundColor White }
    Write-Host ""
    Write-Host "Removendo servicos do Swarm..." -ForegroundColor Yellow
    
    $services | ForEach-Object {
        Write-Host "  [REMOVENDO] $_" -ForegroundColor White
        docker service rm $_ 2>&1 | Out-Null
    }
    
    Write-Host "  [OK] Servicos removidos" -ForegroundColor Green
    Write-Host ""
    Start-Sleep -Seconds 3
}

# Inicia configuração consolidada
Write-Host "Iniciando configuracao consolidada..." -ForegroundColor Yellow
Write-Host ""

docker compose -f config/docker-compose-consolidado.yml up -d

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "  [OK] CONFIGURACAO INICIADA!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "SERVICOS:" -ForegroundColor Yellow
    Write-Host "  - N8N: http://localhost:5678" -ForegroundColor White
    Write-Host "  - Dokploy: http://localhost:3000" -ForegroundColor White
    Write-Host ""
    Write-Host "Ver status:" -ForegroundColor Yellow
    Write-Host "  docker compose -f config/docker-compose-consolidado.yml ps" -ForegroundColor Cyan
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "[ERRO] Falha ao iniciar configuracao" -ForegroundColor Red
}


