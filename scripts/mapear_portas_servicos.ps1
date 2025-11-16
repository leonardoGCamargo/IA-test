# Script para mapear portas dos serviços N8N e Kestra
# Este script cria containers temporários para expor as portas

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  MAPEANDO PORTAS - N8N e KESTRA" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar se os containers estão rodando
$n8nContainer = "iaimplementation-n8nrunnerpostgresollama-ep0mt9-n8n-1"
$kestraContainer = "iaimplementation-kestra-hxsb9f-kestra-1"

Write-Host "Verificando containers..." -ForegroundColor Yellow

$n8nRunning = docker ps --filter "name=$n8nContainer" --format "{{.Names}}" | Select-String -Pattern $n8nContainer
$kestraRunning = docker ps --filter "name=$kestraContainer" --format "{{.Names}}" | Select-String -Pattern $kestraContainer

if ($n8nRunning) {
    Write-Host "✓ N8N está rodando" -ForegroundColor Green
    
    # Verificar se já existe proxy para N8N
    $n8nProxy = docker ps --filter "name=n8n-port-proxy" --format "{{.Names}}"
    if (-not $n8nProxy) {
        Write-Host "Criando proxy de porta para N8N..." -ForegroundColor Yellow
        $n8nNetwork = docker inspect $n8nContainer --format='{{range $k, $v := .NetworkSettings.Networks}}{{$k}}{{end}}' | Select-Object -First 1
        
        # Usar socat se disponível, senão criar um container nginx simples
        docker run -d --name n8n-port-proxy --network $n8nNetwork -p 5678:5678 alpine/socat tcp-listen:5678,fork,reuseaddr tcp-connect:$n8nContainer`:5678 2>&1 | Out-Null
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Proxy N8N criado na porta 5678" -ForegroundColor Green
        } else {
            Write-Host "✗ Erro ao criar proxy N8N" -ForegroundColor Red
        }
    } else {
        Write-Host "✓ Proxy N8N já existe" -ForegroundColor Green
    }
} else {
    Write-Host "✗ N8N não está rodando" -ForegroundColor Red
}

if ($kestraRunning) {
    Write-Host "✓ Kestra está rodando na porta 64149" -ForegroundColor Green
} else {
    Write-Host "✗ Kestra não está rodando" -ForegroundColor Red
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ACESSO:" -ForegroundColor Yellow
Write-Host "  N8N: http://localhost:5678" -ForegroundColor Cyan
Write-Host "  Kestra: http://localhost:64149" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

