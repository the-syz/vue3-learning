#!/usr/bin/env python3
"""
简化版前后端启动脚本
快速启动前后端服务器
"""

import subprocess
import os
import sys
from pathlib import Path

def main():
    """简化版启动函数"""
    
    # 获取当前目录
    base_dir = Path.cwd()
    backend_dir = base_dir / "backend"
    frontend_dir = base_dir / "project0"
    
    if not backend_dir.exists():
        print(f"❌ 后端目录不存在: {backend_dir}")
        return
    
    if not frontend_dir.exists():
        print(f"❌ 前端目录不存在: {frontend_dir}")
        return
    
    print("🚀 启动前后端开发服务器...")
    print("📍 前端: http://localhost:5173")
    print("📍 后端: http://localhost:8000")
    print("💡 按 Ctrl+C 停止所有服务")
    print()
    
    # 启动后端
    print("🔄 启动后端服务...")
    backend_cmd = [sys.executable, "main.py"]
    
    # 启动前端
    print("🔄 启动前端服务...")
    frontend_cmd = ["npm", "run", "dev"]
    
    try:
        # 使用Windows的start命令在新窗口启动
        if os.name == 'nt':
            os.system(f'start "后端服务" cmd /k "cd /d {backend_dir} && {sys.executable} main.py"')
            os.system(f'start "前端服务" cmd /k "cd /d {frontend_dir} && npm run dev"')
        else:
            # Linux/Mac版本
            os.system(f'gnome-terminal -- bash -c "cd {backend_dir} && python3 main.py; exec bash" &')
            os.system(f'gnome-terminal -- bash -c "cd {frontend_dir} && npm run dev; exec bash" &')
        
        print("✅ 服务器启动完成！")
        print("📝 已在新窗口中启动前后端服务")
        
    except Exception as e:
        print(f"❌ 启动失败: {e}")

if __name__ == "__main__":
    main()