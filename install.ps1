# 作者：阿洋
# Profound Cognition - Windows PowerShell 安装脚本
# 
# 用法: .\install.ps1
# 默认: .\install.ps1 -Scope user
# 可选: .\install.ps1 -Scope project

param(
    [ValidateSet("user", "project")]
    [string]$Scope = "user"
)

$REPO_URL = "https://github.com/llootupsl/profound-cognition.git"
$SKILL_NAME = "profound-cognition"

if ($Scope -eq "user") {
    $TARGET = Join-Path $env:USERPROFILE ".claude\skills\$SKILL_NAME"
} else {
    $TARGET = Join-Path (Get-Location) ".claude\skills\$SKILL_NAME"
}

Write-Host "正在安装 Profound Cognition 技能" -ForegroundColor Cyan
Write-Host "安装路径: $TARGET" -ForegroundColor Gray
Write-Host ""

if (Test-Path $TARGET) {
    Write-Host "已存在，正在更新..." -ForegroundColor Yellow
    Push-Location $TARGET
    git pull origin master 2>&1 | Out-Null
    Pop-Location
    Write-Host "更新完成！" -ForegroundColor Green
} else {
    Write-Host "正在下载..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Force -Path (Split-Path $TARGET -Parent) | Out-Null
    git clone $REPO_URL $TARGET 2>&1 | Out-Null
    Write-Host "安装完成！" -ForegroundColor Green
}

Write-Host ""
Write-Host "使用方式：" -ForegroundColor White
Write-Host "直接在对话中输入分析问题，框架自动激活。" -ForegroundColor Gray
Write-Host "示例: 分析《三体》中黑暗森林法则的哲学基础" -ForegroundColor Gray
