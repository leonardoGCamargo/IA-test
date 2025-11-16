# Script PowerShell para limpar containers Docker desnecessários

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  LIMPEZA DE CONTAINERS DOCKER" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Conta containers
$total = (docker ps -a -q | Measure-Object).Count
$running = (docker ps -q | Measure-Object).Count
$stopped = (docker ps -a --filter "status=exited" -q | Measure-Object).Count

Write-Host "ESTATISTICAS:" -ForegroundColor Yellow
Write-Host "  Total de containers: $total" -ForegroundColor White
Write-Host "  Rodando: $running" -ForegroundColor Green
Write-Host "  Parados: $stopped" -ForegroundColor Red
Write-Host ""

# Lista containers do projeto
Write-Host "CONTAINERS DO PROJETO IA-TEST:" -ForegroundColor Yellow
docker ps -a --format "{{.Names}}\t{{.Status}}" | Select-String -Pattern "ia-test|kestra|neo4j" | ForEach-Object {
    Write-Host "  $_" -ForegroundColor White
}
Write-Host ""

# Pergunta se deve limpar
$resposta = Read-Host "Deseja remover containers parados? (S/N)"

if ($resposta -eq "S" -or $resposta -eq "s") {
    Write-Host ""
    Write-Host "Removendo containers parados..." -ForegroundColor Yellow
    
    # Remove containers parados
    docker ps -a --filter "status=exited" -q | ForEach-Object {
        $nome = docker ps -a --filter "id=$_" --format "{{.Names}}"
        Write-Host "  Removendo: $nome" -ForegroundColor White
        docker rm $_ 2>&1 | Out-Null
    }
    
    Write-Host ""
    Write-Host "Containers parados removidos!" -ForegroundColor Green
}

# Limpa imagens não utilizadas
$resposta2 = Read-Host "Deseja limpar imagens nao utilizadas? (S/N)"

if ($resposta2 -eq "S" -or $resposta2 -eq "s") {
    Write-Host ""
    Write-Host "Limpando imagens nao utilizadas..." -ForegroundColor Yellow
    docker image prune -a -f
    Write-Host "Imagens limpas!" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  LIMPEZA CONCLUIDA!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan

