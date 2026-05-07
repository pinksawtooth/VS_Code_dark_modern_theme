param(
    [string]$GhidraUserDir = (Join-Path $env:APPDATA 'ghidra\ghidra_12.0.4_PUBLIC')
)

$ErrorActionPreference = 'Stop'

$RepoDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ThemeSource = Join-Path $RepoDir 'themes\vscode-dark-modern.theme'
$IconSource = Join-Path $RepoDir 'images\vscode\codicons'
$ThemeTarget = Join-Path $GhidraUserDir 'themes'
$IconTarget = Join-Path $GhidraUserDir 'images\vscode\codicons'

New-Item -ItemType Directory -Force -Path $ThemeTarget | Out-Null
New-Item -ItemType Directory -Force -Path $IconTarget | Out-Null

Copy-Item -LiteralPath $ThemeSource -Destination $ThemeTarget -Force
Copy-Item -Path (Join-Path $IconSource '*') -Destination $IconTarget -Recurse -Force

Write-Host "Installed VS Code Dark Modern theme to $GhidraUserDir"
