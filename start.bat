@echo off
chcp 65001 >nul
title 前后端开发服务器启动器
echo.
echo ================================================
echo      前后端开发服务器自动启动工具
echo ================================================
echo 后端服务: FastAPI (端口 8000)
echo 前端服务: Vite + Vue3 (端口 5173)
echo ================================================
echo.

:: 检查Python环境
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未检测到Python环境，请先安装Python
    pause
    exit /b 1
)

:: 启动前后端服务器
echo 🚀 正在启动前后端服务器...
python start_servers.py

pause