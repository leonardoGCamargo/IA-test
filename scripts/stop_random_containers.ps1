# Script para parar e remover containers com nomes aleatórios do projeto

Write-Host "=== Parando e removendo containers com nomes aleatórios ===" -ForegroundColor Yellow

# Containers com nomes aleatórios que são do projeto (MCP Desktop)
$randomContainers = @(
    "strange_roentgen",
    "keen_volhard",
    "elastic_sinoussi",
    "nifty_jemison",
    "sweet_khorana",
    "gallant_mahavira",
    "dazzling_perlman",
    "quizzical_blackwell"
)

$stopped = 0
$removed = 0

foreach ($container in $randomContainers) {
    $exists = docker ps -a --filter "name=$container" -q
    if ($exists) {
        Write-Host "Parando $container..." -ForegroundColor Yellow
        docker stop $container 2>$null
        if ($LASTEXITCODE -eq 0) {
            $stopped++
        }
        
        Write-Host "Removendo $container..." -ForegroundColor Yellow
        docker rm $container 2>$null
        if ($LASTEXITCODE -eq 0) {
            $removed++
        }
    }
}

Write-Host "`n=== Resultado ===" -ForegroundColor Green
Write-Host "Containers parados: $stopped" -ForegroundColor Green
Write-Host "Containers removidos: $removed" -ForegroundColor Green

Write-Host "`n=== Containers restantes do projeto ===" -ForegroundColor Cyan
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}" | findstr /V "NAMES"

