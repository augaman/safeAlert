# SafeAlert Backup Script
# This script creates timestamped backups of the project

$date = Get-Date -Format "yyyy-MM-dd_HH-mm"
$projectRoot = Split-Path -Parent $PSScriptRoot
$backupDir = Join-Path $projectRoot "backups"
$backupName = "safeAlert_backup_$date.zip"
$backupPath = Join-Path $backupDir $backupName

# Create backup directory if it doesn't exist
if (-not (Test-Path $backupDir)) {
    New-Item -ItemType Directory -Path $backupDir
}

# Create backup excluding unnecessary files/folders
$excludeList = @(
    "node_modules",
    "venv",
    "__pycache__",
    "*.pyc",
    "backups",
    ".git"
)

# Create backup
Compress-Archive -Path "$projectRoot\*" -DestinationPath $backupPath -Force
foreach ($exclude in $excludeList) {
    Get-ChildItem -Path $projectRoot -Recurse -Filter $exclude | Remove-Item -Force -Recurse
}

Write-Host "Backup created at: $backupPath"

# Clean old backups (keep last 5)
$oldBackups = Get-ChildItem -Path $backupDir | Sort-Object CreationTime -Descending | Select-Object -Skip 5
if ($oldBackups) {
    $oldBackups | Remove-Item -Force
    Write-Host "Cleaned up old backups"
} 