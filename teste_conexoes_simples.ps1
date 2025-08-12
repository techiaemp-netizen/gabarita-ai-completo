# Script PowerShell para testar conexões - Versão Simplificada
# Gabarita AI - Teste de Conexões

Write-Host "`n" -ForegroundColor Cyan
Write-Host "  ____       _                _ _          _    ___ " -ForegroundColor Magenta
Write-Host " / ___| __ _| |__   __ _ _ __(_) |_ __ _  / \  |_ _|" -ForegroundColor Magenta
Write-Host " | |  _ / _` | '_ \ / _` | '__| | __/ _` |/ _ \  | | " -ForegroundColor Magenta
Write-Host " | |_| | (_| | |_) | (_| | |  | | || (_| / ___ \ | | " -ForegroundColor Magenta
Write-Host "  \____|\_,_|_.__/ \__,_|_|  |_|\__\__,_/_/   \_|___|" -ForegroundColor Magenta
Write-Host "`nTeste de Conexoes - Versao Simplificada" -ForegroundColor White
Write-Host "Data: $(Get-Date -Format 'dd/MM/yyyy HH:mm:ss')" -ForegroundColor Gray

$results = @{}

# ============================================================================
# TESTE DE ESTRUTURA DO PROJETO
# ============================================================================
Write-Host "`n$('='*60)" -ForegroundColor Cyan
Write-Host "TESTE DE ESTRUTURA DO PROJETO" -ForegroundColor Cyan
Write-Host "$('='*60)" -ForegroundColor Cyan

$structureOk = $true

# Verificar diretórios
$dirs = @("gabarita-ai-frontend", "gabarita-ai-backend", "gabarita-ai-backend-deploy", "src")
foreach ($dir in $dirs) {
    if (Test-Path $dir -PathType Container) {
        Write-Host "✅ Diretorio encontrado: $dir" -ForegroundColor Green
    } else {
        Write-Host "❌ Diretorio nao encontrado: $dir" -ForegroundColor Red
        $structureOk = $false
    }
}

# Verificar arquivos principais
$files = @("src\main.py", "gabarita-ai-frontend\package.json", "requirements.txt")
foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host "✅ Arquivo encontrado: $file" -ForegroundColor Green
    } else {
        Write-Host "❌ Arquivo nao encontrado: $file" -ForegroundColor Red
        $structureOk = $false
    }
}

$results['Estrutura'] = $structureOk

# ============================================================================
# TESTE DE CONEXÃO COM GITHUB
# ============================================================================
Write-Host "`n$('='*60)" -ForegroundColor Cyan
Write-Host "TESTE DE CONEXAO - GITHUB" -ForegroundColor Cyan
Write-Host "$('='*60)" -ForegroundColor Cyan

$githubOk = $false
$ErrorActionPreference = 'SilentlyContinue'
$response = Invoke-RestMethod -Uri "https://api.github.com/repos/techiaemp-netizen/gabarita-ai-backend" -Method Get -TimeoutSec 10
$ErrorActionPreference = 'Continue'

if ($response) {
    Write-Host "✅ Repositorio GitHub encontrado: $($response.full_name)" -ForegroundColor Green
    Write-Host "ℹ️  Ultima atualizacao: $($response.updated_at)" -ForegroundColor Blue
    Write-Host "ℹ️  Branch padrao: $($response.default_branch)" -ForegroundColor Blue
    $githubOk = $true
} else {
    Write-Host "❌ Erro na conexao com GitHub" -ForegroundColor Red
}

$results['GitHub'] = $githubOk

# ============================================================================
# TESTE DE CONFIGURAÇÃO DO VERCEL
# ============================================================================
Write-Host "`n$('='*60)" -ForegroundColor Cyan
Write-Host "TESTE DE CONFIGURACAO - VERCEL" -ForegroundColor Cyan
Write-Host "$('='*60)" -ForegroundColor Cyan

$vercelOk = $true

# Verificar arquivos do Vercel
$vercelFiles = @("gabarita-ai-frontend\vercel.json", ".vercel\project.json")
foreach ($file in $vercelFiles) {
    if (Test-Path $file) {
        Write-Host "✅ Arquivo Vercel encontrado: $file" -ForegroundColor Green
    } else {
        Write-Host "❌ Arquivo Vercel nao encontrado: $file" -ForegroundColor Red
        $vercelOk = $false
    }
}

# Verificar .env.example do frontend
if (Test-Path "gabarita-ai-frontend\.env.example") {
    Write-Host "✅ Arquivo .env.example do frontend encontrado" -ForegroundColor Green
} else {
    Write-Host "❌ Arquivo .env.example do frontend nao encontrado" -ForegroundColor Red
    $vercelOk = $false
}

$results['Vercel'] = $vercelOk

# ============================================================================
# TESTE DE CONFIGURAÇÃO DO RENDER
# ============================================================================
Write-Host "`n$('='*60)" -ForegroundColor Cyan
Write-Host "TESTE DE CONFIGURACAO - RENDER" -ForegroundColor Cyan
Write-Host "$('='*60)" -ForegroundColor Cyan

$renderOk = $true

# Verificar arquivos do Render
$renderFiles = @("render.yaml", "gabarita-ai-backend-deploy\render.yaml", "requirements.txt")
foreach ($file in $renderFiles) {
    if (Test-Path $file) {
        Write-Host "✅ Arquivo Render encontrado: $file" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Arquivo Render nao encontrado: $file" -ForegroundColor Yellow
        if ($file -eq "requirements.txt") {
            $renderOk = $false
        }
    }
}

# Verificar .env.example
if (Test-Path ".env.example") {
    Write-Host "✅ Arquivo .env.example encontrado" -ForegroundColor Green
    $content = Get-Content ".env.example" -Raw -ErrorAction SilentlyContinue
    if ($content -and $content -match 'onrender.com') {
        Write-Host "ℹ️  URL do Render configurada" -ForegroundColor Blue
    }
} else {
    Write-Host "❌ Arquivo .env.example nao encontrado" -ForegroundColor Red
}

$results['Render'] = $renderOk

# ============================================================================
# TESTE DE CONFIGURAÇÃO DO FIREBASE
# ============================================================================
Write-Host "`n$('='*60)" -ForegroundColor Cyan
Write-Host "TESTE DE CONFIGURACAO - FIREBASE" -ForegroundColor Cyan
Write-Host "$('='*60)" -ForegroundColor Cyan

$firebaseOk = $true

# Verificar arquivos do Firebase
$firebaseFiles = @(
    "gabarita-ai-frontend\firebase.json",
    "gabarita-ai-frontend\firestore.rules",
    "gabarita-ai-frontend\src\config\firebase.js"
)

foreach ($file in $firebaseFiles) {
    if (Test-Path $file) {
        Write-Host "✅ Arquivo Firebase encontrado: $file" -ForegroundColor Green
    } else {
        Write-Host "❌ Arquivo Firebase nao encontrado: $file" -ForegroundColor Red
        $firebaseOk = $false
    }
}

# Verificar variáveis Firebase nos arquivos .env.example
$envFiles = @(".env.example", "gabarita-ai-frontend\.env.example")
foreach ($envFile in $envFiles) {
    if (Test-Path $envFile) {
        $content = Get-Content $envFile -Raw -ErrorAction SilentlyContinue
        if ($content) {
            $firebaseVars = @('FIREBASE_PROJECT_ID', 'FIREBASE_PRIVATE_KEY', 'FIREBASE_CLIENT_EMAIL')
            $foundVars = 0
            foreach ($var in $firebaseVars) {
                if ($content -match $var) {
                    $foundVars++
                }
            }
            if ($foundVars -gt 0) {
                Write-Host "ℹ️  Variaveis Firebase encontradas em $envFile ($foundVars/3)" -ForegroundColor Blue
            } else {
                Write-Host "⚠️  Nenhuma variavel Firebase em $envFile" -ForegroundColor Yellow
            }
        }
    }
}

$results['Firebase'] = $firebaseOk

# ============================================================================
# RELATÓRIO FINAL
# ============================================================================
Write-Host "`n$('='*60)" -ForegroundColor Cyan
Write-Host "RELATORIO FINAL" -ForegroundColor Cyan
Write-Host "$('='*60)" -ForegroundColor Cyan

$totalTests = $results.Count
$passedTests = 0
foreach ($result in $results.Values) {
    if ($result -eq $true) {
        $passedTests++
    }
}

Write-Host "`n📊 Resumo dos Testes:" -ForegroundColor White
Write-Host "   Total de testes: $totalTests" -ForegroundColor White
Write-Host "   Testes aprovados: $passedTests" -ForegroundColor Green
Write-Host "   Testes falharam: $($totalTests - $passedTests)" -ForegroundColor Red

if ($totalTests -gt 0) {
    $successRate = [math]::Round(($passedTests / $totalTests) * 100, 1)
    Write-Host "   Taxa de sucesso: $successRate%" -ForegroundColor White
}

Write-Host "`n📋 Status por Servico:" -ForegroundColor White
foreach ($service in $results.Keys) {
    $status = if ($results[$service]) { "✅ APROVADO" } else { "❌ FALHOU" }
    $color = if ($results[$service]) { "Green" } else { "Red" }
    Write-Host "   $service`: $status" -ForegroundColor $color
}

if ($passedTests -eq $totalTests) {
    Write-Host "`n🎉 SUCESSO: Todas as conexoes estao configuradas!" -ForegroundColor Green
    Write-Host "Voce pode prosseguir com o deploy dos servicos." -ForegroundColor Blue
    exit 0
} else {
    Write-Host "`n⚠️  ATENCAO: Algumas configuracoes precisam ser ajustadas." -ForegroundColor Yellow
    Write-Host "Verifique os erros acima antes de fazer o deploy." -ForegroundColor Blue
    
    Write-Host "`n🔧 Proximos Passos:" -ForegroundColor White
    if (-not $results['GitHub']) {
        Write-Host "   1. Verificar acesso ao repositorio GitHub" -ForegroundColor Yellow
    }
    if (-not $results['Vercel']) {
        Write-Host "   2. Configurar arquivos do Vercel" -ForegroundColor Yellow
    }
    if (-not $results['Render']) {
        Write-Host "   3. Configurar arquivos do Render" -ForegroundColor Yellow
    }
    if (-not $results['Firebase']) {
        Write-Host "   4. Configurar arquivos do Firebase" -ForegroundColor Yellow
    }
    
    Write-Host "`n📚 Documentacao:" -ForegroundColor White
    Write-Host "   - DEPLOY_RENDER_MANUAL.md" -ForegroundColor Gray
    Write-Host "   - gabarita-ai-frontend/DEPLOY_VERCEL.md" -ForegroundColor Gray
    Write-Host "   - GUIA_CONFIGURACAO_RAPIDA.md" -ForegroundColor Gray
    
    exit 1
}