# .env dosyasını oku ve PowerShell oturumuna yükle
if (-not (Test-Path ".env")) {
    Write-Host "[X] .env dosyasi yok. Once .env.example'dan kopyala." -ForegroundColor Red
    exit 1
}

Get-Content .env | ForEach-Object {
    if ($_ -match '^\s*([^#][^=]*?)\s*=\s*(.*)\s*$') {
        $name = $matches[1].Trim()
        $value = $matches[2].Trim()
        Set-Item -Path "env:$name" -Value $value
    }
}

Write-Host "[OK] .env yuklendi" -ForegroundColor Green

# GITHUB_PAT preview (ilk 15 karakter)
if ($env:GITHUB_PAT) {
    $preview = $env:GITHUB_PAT.Substring(0, [Math]::Min(15, $env:GITHUB_PAT.Length))
    Write-Host "  GITHUB_PAT preview: $preview" -ForegroundColor Cyan
} else {
    Write-Host "  [!] GITHUB_PAT yuklenmedi" -ForegroundColor Yellow
}

Write-Host ""

# Claude Code'u baslat
claude