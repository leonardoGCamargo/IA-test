# Script PowerShell para limpeza automática de containers órfãos
# Execute periodicamente para manter o sistema limpo

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  LIMPEZA AUTOMATICA DE CONTAINERS" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Executa o script Python
python "scripts/remover_containers_orfos.py"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ESTATISTICAS FINAIS" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$total = docker ps --format "{{.Names}}" | Measure-Object -Line | Select-Object -ExpandProperty Lines
$ia_test = docker ps --format "{{.Names}}" | Where-Object { $_ -match "ia-test" } | Measure-Object -Line | Select-Object -ExpandProperty Lines
$n8n = docker ps --format "{{.Names}}" | Where-Object { $_ -match "n8n" } | Measure-Object -Line | Select-Object -ExpandProperty Lines
$outros = docker ps --format "{{.Names}}" | Where-Object { $_ -notmatch "ia-test|n8n|dokploy|postgres|redis|ollama|kestra|neo4j|traefik" } | Measure-Object -Line | Select-Object -ExpandProperty Lines

Write-Host "Total de containers rodando: $total" -ForegroundColor White
Write-Host "  - IA-test: $ia_test" -ForegroundColor Yellow
Write-Host "  - N8N: $n8n" -ForegroundColor Yellow
Write-Host "  - Outros (dokploy, redis, etc): $($total - $ia_test - $n8n - $outros)" -ForegroundColor Yellow
Write-Host "  - Orfaos restantes: $outros" -ForegroundColor $(if ($outros -gt 0) { "Red" } else { "Green" })
Write-Host ""

if ($outros -gt 0) {
    Write-Host "AVISO: Ainda ha containers orfaos rodando!" -ForegroundColor Red
    Write-Host "Execute novamente o script se necessario." -ForegroundColor Yellow
}

Write-Host "========================================" -ForegroundColor Cyan

