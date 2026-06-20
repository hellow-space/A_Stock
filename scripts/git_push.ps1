# A_Stock Git 自动提交脚本 (PowerShell)
# 使用方法: 右键点击 -> 使用 PowerShell 运行

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "   A_Stock Git 自动提交工具" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# 检查是否有修改
git diff --quiet 2>$null
git diff --cached --quiet 2>$null

if ($LASTEXITCODE -eq 0) {
    Write-Host "[INFO] 没有检测到文件修改" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "按回车键退出"
    exit 0
}

Write-Host "[INFO] 检测到文件修改，开始提交..." -ForegroundColor Green
Write-Host ""

# 显示修改的文件
Write-Host "[INFO] 修改的文件列表：" -ForegroundColor Cyan
git status --short
Write-Host ""

# 添加所有修改
git add .

# 提交，使用时间戳作为提交信息
$commitMsg = "update: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
git commit -m "$commitMsg"

# 推送到GitHub
Write-Host ""
Write-Host "[INFO] 正在推送到GitHub..." -ForegroundColor Cyan
git push origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "[SUCCESS] 已成功推送到GitHub！" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "[ERROR] 推送失败，请检查网络或分支设置" -ForegroundColor Red
}

Write-Host ""
Read-Host "按回车键退出"
