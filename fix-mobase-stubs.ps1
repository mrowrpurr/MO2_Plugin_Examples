# Check for admin rights
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()
).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")

if (-not $isAdmin) {
    Write-Host "🛑 Hey! You're not running this in an Administrator PowerShell window!" -ForegroundColor Red
    Write-Host "🔧 Right-click PowerShell and choose 'Run as administrator' before running this script."
    exit 1
}

$target = ".venv\Lib\site-packages\mobase-stubs"
$link = ".venv\Lib\site-packages\mobase"

if (-not (Test-Path $target)) {
    Write-Host "❌ Target stub folder not found: $target" -ForegroundColor Yellow
    exit 1
}

if (Test-Path $link) {
    Write-Host "✅ Symlink already exists: $link"
    exit 0
}

Write-Host "🔗 Creating symlink: $link -> $target"
cmd /c "mklink /D `"$link`" `"$target`""
