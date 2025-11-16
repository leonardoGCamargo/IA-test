# Script PowerShell para iniciar o dashboard e abrir no navegador

Write-Host "🚀 Iniciando Dashboard de Agentes..." -ForegroundColor Green
Write-Host ""

# Muda para o diretório do projeto
$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

# Verifica se streamlit está instalado
try {
    $streamlitVersion = python -c "import streamlit; print(streamlit.__version__)" 2>&1
    Write-Host "✅ Streamlit encontrado: $streamlitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Streamlit não encontrado. Instalando..." -ForegroundColor Yellow
    pip install streamlit
}

# Inicia o dashboard em background
Write-Host "⏳ Iniciando dashboard na porta 8508..." -ForegroundColor Yellow
$dashboardProcess = Start-Process python -ArgumentList "-m", "streamlit", "run", "src/apps/agent_dashboard.py", "--server.port=8508", "--server.address=0.0.0.0" -PassThru -NoNewWindow

# Aguarda alguns segundos
Write-Host "⏳ Aguardando dashboard iniciar..." -ForegroundColor Yellow
Start-Sleep -Seconds 8

# Verifica se está rodando
$portCheck = netstat -ano | Select-String ":8508"
if ($portCheck) {
    Write-Host "✅ Dashboard iniciado com sucesso!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🌐 Abrindo no navegador..." -ForegroundColor Cyan
    Start-Process "http://localhost:8508"
    Write-Host ""
    Write-Host "📱 Dashboard disponível em: http://localhost:8508" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "💡 Pressione Ctrl+C para parar" -ForegroundColor Yellow
    Write-Host ""
    
    # Mantém o processo rodando
    $dashboardProcess.WaitForExit()
} else {
    Write-Host "⚠️ Dashboard pode estar iniciando ainda..." -ForegroundColor Yellow
    Write-Host "💡 Aguarde alguns segundos e abra manualmente: http://localhost:8508" -ForegroundColor Cyan
    Start-Process "http://localhost:8508"
}

