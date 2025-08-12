# Script PowerShell para testar conexões com GitHub, Vercel, Render e Firebase
# Gabarita AI - Teste de Conexões

Write-Host "`n" -ForegroundColor Cyan
Write-Host "  ____       _                _ _          _    ___ " -ForegroundColor Magenta
Write-Host " / ___| __ _| |__   __ _ _ __(_) |_ __ _  / \  |_ _|" -ForegroundColor Magenta
Write-Host " | |  _ / _` | '_ \ / _` | '__| | __/ _` |/ _ \  | | " -ForegroundColor Magenta
Write-Host " | |_| | (_| | |_) | (_| | |  | | || (_| / ___ \ | | " -ForegroundColor Magenta
Write-Host "  \____|\_,_|_.__/ \__,_|_|  |_|\__\__,_/_/   \_|___|" -ForegroundColor Magenta
Write-Host "`nTeste de Conexoes - Versao 1.0" -ForegroundColor White
Write-Host "Data: $(Get-Date -Format 'dd/MM/yyyy HH:mm:ss')" -ForegroundColor Gray

$results = @{}

# ============================================================================
# TESTE DE ESTRUTURA DO PROJETO
# ============================================================================
Write-Host "`n$('='*60)" -ForegroundColor Cyan
Write-Host "TESTE DE ESTRUTURA DO PROJETO".PadLeft(30).PadRight(60) -ForegroundColor Cyan
Write-Host "$('='*60)`n" -ForegroundColor Cyan

$requiredDirs = @(
    "gabarita-ai-frontend",
    "gabarita-ai-backend",
    "gabarita-ai-backend-deploy",
    "src"
)

$structureOk = $true

foreach ($dirName in $requiredDirs) {
    if (Test-Path $dirName -PathType Container) {
        Write-Host "✅ Diretorio encontrado: $dirName" -ForegroundColor Green
    }
    else {
        Write-Host "❌ Diretorio nao encontrado: $dirName" -ForegroundColor Red
        $structureOk = $false
    }
}

$mainFiles = @(
    "src\main.py",
    "gabarita-ai-frontend\package.json",
    "requirements.txt"
)

foreach ($filePath in $mainFiles) {
    if (Test-Path $filePath) {
        Write-Host "✅ Arquivo principal encontrado: $filePath" -ForegroundColor Green
    }
    else {
        Write-Host "❌ Arquivo principal nao encontrado: $filePath" -ForegroundColor Red
        $structureOk = $false
    }
}

$results['Estrutura do Projeto'] = $structureOk

# ============================================================================
# TESTE DE CONEXÃO COM GITHUB
# ============================================================================
Write-Host "`n$('='*60)" -ForegroundColor Cyan
Write-Host "TESTE DE CONEXAO - GITHUB".PadLeft(30).PadRight(60) -ForegroundColor Cyan
Write-Host "$('='*60)`n" -ForegroundColor Cyan

$githubOk = $false
try {
    $repoUrl = "https://api.github.com/repos/techiaemp-netizen/gabarita-ai-backend"
    $response = Invoke-RestMethod -Uri $repoUrl -Method Get -TimeoutSec 10
    
    if ($response) {
        Write-Host "✅ Repositorio encontrado: $($response.full_name)" -ForegroundColor Green
        Write-Host "ℹ️  Ultima atualizacao: $($response.updated_at)" -ForegroundColor Blue
        Write-Host "ℹ️  Branch padrao: $($response.default_branch)" -ForegroundColor Blue
        Write-Host "ℹ️  Linguagem principal: $($response.language)" -ForegroundColor Blue
        $githubOk = $true
    }
}
catch {
    Write-Host "❌ Erro na conexao com GitHub: $($_.Exception.Message)" -ForegroundColor Red
    $githubOk = $false
}

$results['GitHub'] = $githubOk

# ============================================================================
# TESTE DE CONFIGURAÇÃO DO VERCEL
# ============================================================================
Write-Host "`n$('='*60)" -ForegroundColor Cyan
Write-Host "TESTE DE CONFIGURACAO - VERCEL".PadLeft(30).PadRight(60) -ForegroundColor Cyan
Write-Host "$('='*60)`n" -ForegroundColor Cyan

$vercelFiles = @(
    "gabarita-ai-frontend\vercel.json",
    ".vercel\project.json"
)

$vercelOk = $true

foreach ($filePath in $vercelFiles) {
    if (Test-Path $filePath) {
        Write-Host "✅ Arquivo encontrado: $filePath" -ForegroundColor Green
        try {
            $config = Get-Content $filePath | ConvertFrom-Json
            if ($config.projectName) {
                Write-Host "ℹ️  Projeto Vercel: $($config.projectName)" -ForegroundColor Blue
            }
            if ($config.buildCommand) {
                Write-Host "ℹ️  Comando de build: $($config.buildCommand)" -ForegroundColor Blue
            }
        }
        catch {
            Write-Host "⚠️  Erro ao ler $filePath" -ForegroundColor Yellow
        }
    }
    else {
        Write-Host "❌ Arquivo nao encontrado: $filePath" -ForegroundColor Red
        $vercelOk = $false
    }
}

$envExample = "gabarita-ai-frontend\.env.example"
if (Test-Path $envExample) {
    Write-Host "✅ Arquivo .env.example encontrado no frontend" -ForegroundColor Green
    Write-Host "ℹ️  Variaveis de ambiente configuradas para Vercel" -ForegroundColor Blue
}
else {
    Write-Host "❌ Arquivo .env.example nao encontrado no frontend" -ForegroundColor Red
    $vercelOk = $false
}

$results['Vercel'] = $vercelOk

# ============================================================================
# TESTE DE CONFIGURAÇÃO DO RENDER
# ============================================================================
Write-Host "`n$('='*60)" -ForegroundColor Cyan
Write-Host "TESTE DE CONFIGURACAO - RENDER".PadLeft(30).PadRight(60) -ForegroundColor Cyan
Write-Host "$('='*60)`n" -ForegroundColor Cyan

$renderFiles = @(
    "render.yaml",
    "gabarita-ai-backend-deploy\render.yaml",
    "requirements.txt"
)

$renderOk = $true

foreach ($filePath in $renderFiles) {
    if (Test-Path $filePath) {
        Write-Host "✅ Arquivo encontrado: $filePath" -ForegroundColor Green
        if ($filePath.EndsWith('.yaml')) {
            try {
                $content = Get-Content $filePath -Raw
                if ($content -match 'gabarita-ai-backend') {
                    Write-Host "ℹ️  Configuracao do servico encontrada" -ForegroundColor Blue
                }
                if ($content -match 'python') {
                    Write-Host "ℹ️  Runtime Python configurado" -ForegroundColor Blue
                }
            }
            catch {
                Write-Host "⚠️  Erro ao ler $filePath" -ForegroundColor Yellow
            }
        }
    }
    else {
        Write-Host "⚠️  Arquivo nao encontrado: $filePath" -ForegroundColor Yellow
        if ($filePath -eq "requirements.txt") {
            $renderOk = $false
        }
    }
}

$envExample = ".env.example"
if (Test-Path $envExample) {
    try {
        $content = Get-Content $envExample -Raw
        if ($content -match 'onrender.com') {
            Write-Host "ℹ️  URL do Render configurada no .env.example" -ForegroundColor Blue
        }
        else {
            Write-Host "⚠️  URL do Render nao encontrada no .env.example" -ForegroundColor Yellow
        }
    }
    catch {
        Write-Host "⚠️  Erro ao ler .env.example" -ForegroundColor Yellow
    }
}

$results['Render'] = $renderOk

# ============================================================================
# TESTE DE CONFIGURAÇÃO DO FIREBASE
# ============================================================================
Write-Host "`n$('='*60)" -ForegroundColor Cyan
Write-Host "TESTE DE CONFIGURACAO - FIREBASE".PadLeft(30).PadRight(60) -ForegroundColor Cyan
Write-Host "$('='*60)`n" -ForegroundColor Cyan

$firebaseFiles = @(
    "gabarita-ai-frontend\firebase.json",
    "gabarita-ai-frontend\firestore.rules",
    "gabarita-ai-frontend\src\config\firebase.js"
)

$firebaseOk = $true

foreach ($filePath in $firebaseFiles) {
    if (Test-Path $filePath) {
        Write-Host "✅ Arquivo encontrado: $filePath" -ForegroundColor Green
        if ($filePath.EndsWith('firebase.js')) {
            try {
                $content = Get-Content $filePath -Raw
                if ($content -match 'initializeApp') {
                    Write-Host "ℹ️  Inicializacao do Firebase configurada" -ForegroundColor Blue
                }
                if ($content -match 'getAuth') {
                    Write-Host "ℹ️  Autenticacao Firebase configurada" -ForegroundColor Blue
                }
                if ($content -match 'getFirestore') {
                    Write-Host "ℹ️  Firestore configurado" -ForegroundColor Blue
                }
            }
            catch {
                Write-Host "⚠️  Erro ao ler $filePath" -ForegroundColor Yellow
            }
        }
    }
    else {
        Write-Host "❌ Arquivo nao encontrado: $filePath" -ForegroundColor Red
        $firebaseOk = $false
    }
}

$envFiles = @(".env.example", "gabarita-ai-frontend\.env.example")

foreach ($envFile in $envFiles) {
    if (Test-Path $envFile) {
        try {
            $content = Get-Content $envFile -Raw
            $firebaseVars = @('FIREBASE_PROJECT_ID', 'FIREBASE_PRIVATE_KEY', 'FIREBASE_CLIENT_EMAIL')
            
            $foundVars = $firebaseVars | Where-Object { $content -match $_ }
            if ($foundVars.Count -gt 0) {
                Write-Host "ℹ️  Variaveis Firebase em $envFile encontradas" -ForegroundColor Blue
            }
            else {
                Write-Host "⚠️  Nenhuma variavel Firebase encontrada em $envFile" -ForegroundColor Yellow
            }
        }
        catch {
            Write-Host "⚠️  Erro ao ler $envFile" -ForegroundColor Yellow
        }
    }
}

$results['Firebase'] = $firebaseOk

# ============================================================================
# RELATÓRIO FINAL
# ============================================================================
Write-Host "`n$('='*60)" -ForegroundColor Cyan
Write-Host "RELATORIO FINAL".PadLeft(30).PadRight(60) -ForegroundColor Cyan
Write-Host "$('='*60)`n" -ForegroundColor Cyan

$totalTests = $results.Count
$passedTests = ($results.Values | Where-Object { $_ -eq $true }).Count

Write-Host "📊 Testes executados: $totalTests" -ForegroundColor White
Write-Host "✅ Testes aprovados: $passedTests" -ForegroundColor Green
Write-Host "❌ Testes falharam: $($totalTests - $passedTests)" -ForegroundColor Red
$successRate = [math]::Round(($passedTests/$totalTests)*100, 1)
Write-Host "📈 Taxa de sucesso: $successRate%" -ForegroundColor White

Write-Host "`n📋 Detalhes por servico:" -ForegroundColor White
foreach ($service in $results.Keys) {
    $statusIcon = if ($results[$service]) { "✅" } else { "❌" }
    Write-Host "   $statusIcon $service" -ForegroundColor White
}

if ($passedTests -eq $totalTests) {
    Write-Host "`n🎉 Todas as conexoes estao configuradas corretamente!" -ForegroundColor Green
    Write-Host "Voce pode prosseguir com o deploy dos servicos." -ForegroundColor Blue
}
else {
    Write-Host "`n⚠️  Algumas configuracoes precisam de atencao." -ForegroundColor Yellow
    Write-Host "Verifique os erros acima e configure os servicos necessarios." -ForegroundColor Blue
}

Write-Host "`n🚀 Proximos passos recomendados:" -ForegroundColor White
if (-not $results['GitHub']) {
    Write-Host "   1. Verificar acesso ao repositorio GitHub" -ForegroundColor Yellow
}
if (-not $results['Vercel']) {
    Write-Host "   2. Configurar variaveis de ambiente no Vercel" -ForegroundColor Yellow
}
if (-not $results['Render']) {
    Write-Host "   3. Configurar deploy no Render" -ForegroundColor Yellow
}
if (-not $results['Firebase']) {
    Write-Host "   4. Configurar credenciais do Firebase" -ForegroundColor Yellow
}

Write-Host "`n📚 Documentacao disponivel:" -ForegroundColor White
Write-Host "   - DEPLOY_RENDER_MANUAL.md" -ForegroundColor Gray
Write-Host "   - gabarita-ai-frontend/DEPLOY_VERCEL.md" -ForegroundColor Gray
Write-Host "   - GUIA_CONFIGURACAO_RAPIDA.md" -ForegroundColor Gray

# Retornar status geral
$allPassed = ($results.Values | Where-Object { $_ -eq $false }).Count -eq 0
if ($allPassed) {
    Write-Host "`n🎉 Todos os testes passaram com sucesso!" -ForegroundColor Green
    exit 0
}
else {
    Write-Host "`n⚠️  Alguns testes falharam. Verifique as configuracoes." -ForegroundColor Yellow
    exit 1
}