# Script PowerShell para consolidar estrutura do projeto
# Move conteúdo de IA-test/IA-test/ para a raiz

Write-Host "="*70 -ForegroundColor Cyan
Write-Host "📁 CONSOLIDAÇÃO DA ESTRUTURA DO PROJETO" -ForegroundColor Cyan
Write-Host "="*70 -ForegroundColor Cyan

$root = Get-Location
$iaTestSub = Join-Path $root "IA-test\IA-test"

if (-not (Test-Path $iaTestSub)) {
    Write-Host "❌ Pasta IA-test\IA-test não encontrada!" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Pasta encontrada: $iaTestSub" -ForegroundColor Green
Write-Host ""

# Pastas para consolidar
$foldersToConsolidate = @(
    "docker",
    "config",
    "docs",
    "scripts",
    "examples",
    "src"
)

# Consolidar pastas
foreach ($folder in $foldersToConsolidate) {
    $source = Join-Path $iaTestSub $folder
    $dest = Join-Path $root "IA-test\$folder"
    
    if (Test-Path $source) {
        Write-Host "📦 Consolidando $folder/..." -ForegroundColor Yellow
        
        if (Test-Path $dest) {
            Write-Host "   ⚠️  $dest já existe, mesclando..." -ForegroundColor Yellow
            # Mescla conteúdo
            Get-ChildItem -Path $source -Recurse | ForEach-Object {
                $relativePath = $_.FullName.Substring($source.Length + 1)
                $destPath = Join-Path $dest $relativePath
                
                if ($_.PSIsContainer) {
                    if (-not (Test-Path $destPath)) {
                        New-Item -ItemType Directory -Path $destPath -Force | Out-Null
                    }
                } else {
                    $destDir = Split-Path $destPath -Parent
                    if (-not (Test-Path $destDir)) {
                        New-Item -ItemType Directory -Path $destDir -Force | Out-Null
                    }
                    Copy-Item -Path $_.FullName -Destination $destPath -Force
                }
            }
        } else {
            # Move pasta inteira
            Move-Item -Path $source -Destination $dest -Force
            Write-Host "   ✅ Movido: $folder/ -> IA-test/$folder/" -ForegroundColor Green
        }
    }
}

# Remover front-end e embedding_model duplicados
$duplicates = @("front-end", "embedding_model")
foreach ($dup in $duplicates) {
    $dupPath = Join-Path $iaTestSub $dup
    if (Test-Path $dupPath) {
        Write-Host "🗑️  Removendo $dup duplicado..." -ForegroundColor Yellow
        Remove-Item -Path $dupPath -Recurse -Force
        Write-Host "   ✅ Removido: $dup" -ForegroundColor Green
    }
}

# Mover arquivos soltos
Write-Host "📄 Movendo arquivos soltos..." -ForegroundColor Yellow
Get-ChildItem -Path $iaTestSub -File | ForEach-Object {
    $dest = Join-Path $root "IA-test\$($_.Name)"
    if (-not (Test-Path $dest)) {
        Move-Item -Path $_.FullName -Destination $dest -Force
        Write-Host "   ✅ Movido: $($_.Name)" -ForegroundColor Green
    } else {
        Write-Host "   ⏭️  Ignorado (já existe): $($_.Name)" -ForegroundColor Gray
    }
}

# Remover pasta IA-test/IA-test/ se estiver vazia
Write-Host ""
Write-Host "🗑️  Removendo pasta IA-test/IA-test/..." -ForegroundColor Yellow
try {
    Remove-Item -Path $iaTestSub -Recurse -Force
    Write-Host "✅ Pasta removida com sucesso!" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Erro ao remover pasta (pode não estar vazia): $_" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "="*70 -ForegroundColor Cyan
Write-Host "✅ CONSOLIDAÇÃO CONCLUÍDA!" -ForegroundColor Green
Write-Host "="*70 -ForegroundColor Cyan

