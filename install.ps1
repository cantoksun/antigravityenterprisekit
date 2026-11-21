<#
.SYNOPSIS
    Antigravity AI-OS v1.0 - One-Click Project Installer & Scaffolder (PowerShell)

.DESCRIPTION
    Installs and injects the Antigravity Enterprise Kit (.agent/, rules, skills, neural-os)
    into any existing or new project workspace safely with zero friction.

.EXAMPLE
    .\install.ps1 -TargetDir "C:\Projects\MyNewApp" -Mode enterprise
#>
[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [string]$TargetDir = ".",

    [Parameter()]
    [ValidateSet("enterprise", "solo")]
    [string]$Mode = "enterprise",

    [Parameter()]
    [switch]$Force,

    [Parameter()]
    [switch]$SkipVerify
)

$ErrorActionPreference = "Stop"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "     ANTIGRAVITY AI-OS: AUTONOMOUS PROJECT INSTALLER        " -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

# 1. Resolve Paths
$SourceRoot = $PSScriptRoot
$ResolvedTarget = (Resolve-Path $TargetDir -ErrorAction SilentlyContinue)
if (-not $ResolvedTarget) {
    New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null
    $ResolvedTarget = (Resolve-Path $TargetDir)
}
$TargetAgentDir = Join-Path $ResolvedTarget ".agent"

Write-Host "[*] Kaynak Dizin : $SourceRoot"
Write-Host "[*] Hedef Dizin  : $ResolvedTarget"
Write-Host "[*] Kurulum Modu : $Mode"

# 2. Check Python Version
Write-Host "`n[*] Python sürümü kontrol ediliyor..." -ForegroundColor Yellow
try {
    $PyVersion = python --version 2>&1
    Write-Host "  [+] $PyVersion algılandı." -ForegroundColor Green
} catch {
    Write-Warning "Python bulunamadı! Lütfen Python 3.10+ kurulu olduğundan emin olun."
}

# 3. Check existing .agent directory
if (Test-Path $TargetAgentDir) {
    if (-not $Force -and ($SourceRoot -ne $ResolvedTarget.Path)) {
        Write-Warning "Hedef dizinde zaten bir '.agent/' klasörü mevcut! Üzerine yazmak için -Force parametresini kullanın."
        Write-Host "Kurulum güvenli biçimde durduruldu." -ForegroundColor Yellow
        exit 0
    }
}

# 4. Copy .agent folder if target is different from source
if ($SourceRoot -ne $ResolvedTarget.Path) {
    Write-Host "`n[*] .agent/ bileşenleri kopyalanıyor..." -ForegroundColor Yellow
    Copy-Item -Path (Join-Path $SourceRoot ".agent") -Destination $ResolvedTarget -Recurse -Force
    Write-Host "  [+] Ajanlar, beceriler, kurallar ve nöral zihin kasası aktarıldı." -ForegroundColor Green

    # Copy .github if exists
    $SourceGithub = Join-Path $SourceRoot ".github"
    if (Test-Path $SourceGithub) {
        Copy-Item -Path $SourceGithub -Destination $ResolvedTarget -Recurse -Force
        Write-Host "  [+] GitHub Actions CI/CD iş akışı (.github/) aktarıldı." -ForegroundColor Green
    }
} else {
    Write-Host "`n[*] Kaynak ve hedef aynı dizin, dosya kopyalama atlandı." -ForegroundColor Cyan
}

# 5. Merge .gitignore safely
$TargetGitignore = Join-Path $ResolvedTarget ".gitignore"
$RulesToAppend = @(
    "",
    "# Antigravity AI-OS Runtime Ignores",
    "__pycache__/",
    "*.py[cod]",
    ".pytest_cache/",
    ".env",
    ".env.*",
    "!.env.example"
)

if (Test-Path $TargetGitignore) {
    $ExistingContent = Get-Content $TargetGitignore -Raw
    $ToAppend = @()
    foreach ($line in $RulesToAppend) {
        if ($line -and -not ($ExistingContent -match [regex]::Escape($line))) {
            $ToAppend += $line
        }
    }
    if ($ToAppend.Count -gt 0) {
        Add-Content -Path $TargetGitignore -Value ($ToAppend -join "`n")
        Write-Host "  [+] .gitignore dosyasına Antigravity kuralları eklendi." -ForegroundColor Green
    }
} else {
    Set-Content -Path $TargetGitignore -Value ($RulesToAppend -join "`n")
    Write-Host "  [+] Yeni .gitignore oluşturuldu." -ForegroundColor Green
}

# 6. Verification
if (-not $SkipVerify) {
    Write-Host "`n[*] Kurulum doğrulaması çalıştırılıyor..." -ForegroundColor Yellow
    Push-Location $ResolvedTarget
    try {
        python .agent/scripts/validate_kit.py
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  [+] Kit bütünlük ve kilit doğrulaması BAŞARILI!" -ForegroundColor Green
        } else {
            Write-Warning "Doğrulama bazı uyarılar verdi."
        }
    } finally {
        Pop-Location
    }
}

Write-Host "`n============================================================" -ForegroundColor Green
Write-Host " [BAŞARILI] Antigravity AI-OS kurulumu tamamlandı!" -ForegroundColor Green
Write-Host " Çalıştırma Rehberi:" -ForegroundColor White
Write-Host "   - Kalite Kapıları: python .agent/scripts/quality_gates.py . --gate session-start"
Write-Host "   - Ana Doğrulayıcı: python .agent/scripts/verify_kit.py"
Write-Host "   - Zihin Grafiği  : .agent/neural_os/ui/graph-preview.html"
Write-Host "============================================================" -ForegroundColor Green
