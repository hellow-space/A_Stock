@echo off
chcp 65001 >nul
cd /d "%~dp0\.."

echo ==========================================
echo   A_Stock Git 自动提交工具
echo ==========================================
echo.

REM 检查是否有修改
git diff --quiet
git diff --cached --quiet

if %errorlevel% == 0 (
    echo [INFO] 没有检测到文件修改
    echo.
    pause
    exit /b 0
)

echo [INFO] 检测到文件修改，开始提交...
echo.

REM 显示修改的文件
echo [INFO] 修改的文件列表：
git status --short
echo.

REM 添加所有修改
git add .

REM 提交
git commit -m "update: %date% %time%"

REM 推送到GitHub
git push origin main

if %errorlevel% == 0 (
    echo.
    echo [SUCCESS] 已成功推送到GitHub！
) else (
    echo.
    echo [ERROR] 推送失败，请检查网络或分支设置
)

echo.
pause
