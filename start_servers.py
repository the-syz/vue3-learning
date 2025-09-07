#!/usr/bin/env python3
"""
前后端服务器自动启动脚本
可以同时启动FastAPI后端和Vite前端开发服务器
"""

import subprocess
import time
import os
import sys
import signal
import platform
from pathlib import Path

class ServerManager:
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        self.is_windows = platform.system() == "Windows"
        
    def print_banner(self):
        print("=" * 60)
        print("     前后端开发服务器自动启动工具")
        print("=" * 60)
        print("后端服务: FastAPI (端口 8000)")
        print("前端服务: Vite + Vue3 (端口 5173)")
        print("=" * 60)
        print()
        
    def start_backend(self):
        """启动后端FastAPI服务器"""
        backend_dir = Path("backend")
        if not backend_dir.exists():
            print(f"❌ 后端目录不存在: {backend_dir.absolute()}")
            return False
            
        print("🚀 正在启动后端服务器...")
        
        # 检查Python环境
        try:
            subprocess.run([sys.executable, "-c", "import fastapi"], 
                         cwd=backend_dir, capture_output=True, check=True)
        except subprocess.CalledProcessError:
            print("⚠️  检测到后端依赖未安装，正在安装...")
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                               cwd=backend_dir, check=True)
                print("✅ 后端依赖安装完成")
            except subprocess.CalledProcessError as e:
                print(f"❌ 依赖安装失败: {e}")
                return False
        
        # 启动后端服务器
        cmd = [sys.executable, "main.py"]
        
        if self.is_windows:
            self.backend_process = subprocess.Popen(
                cmd,
                cwd=backend_dir,
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        else:
            self.backend_process = subprocess.Popen(
                cmd,
                cwd=backend_dir,
                shell=True
            )
        
        print("⏳ 等待后端服务器启动...")
        time.sleep(3)
        
        if self.backend_process.poll() is None:
            print("✅ 后端服务器启动成功")
            print("📍 后端地址: http://127.0.0.1:8000")
            print("📍 API文档: http://127.0.0.1:8000/docs")
            return True
        else:
            print("❌ 后端服务器启动失败")
            return False
    
    def start_frontend(self):
        """启动前端Vite开发服务器"""
        frontend_dir = Path("project0")
        if not frontend_dir.exists():
            print(f"❌ 前端目录不存在: {frontend_dir.absolute()}")
            return False
            
        print("🚀 正在启动前端服务器...")
        
        # 检查Node.js环境
        try:
            subprocess.run(["node", "--version"], capture_output=True, check=True)
        except subprocess.CalledProcessError:
            print("❌ 未检测到Node.js环境，请先安装Node.js")
            return False
        
        # 检查依赖
        node_modules = frontend_dir / "node_modules"
        if not node_modules.exists():
            print("⚠️  检测到前端依赖未安装，正在安装...")
            try:
                subprocess.run(["npm", "install"], cwd=frontend_dir, check=True)
                print("✅ 前端依赖安装完成")
            except subprocess.CalledProcessError as e:
                print(f"❌ 前端依赖安装失败: {e}")
                return False
        
        # 启动前端服务器
        cmd = ["npm", "run", "dev"]
        
        if self.is_windows:
            self.frontend_process = subprocess.Popen(
                cmd,
                cwd=frontend_dir,
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        else:
            self.frontend_process = subprocess.Popen(
                cmd,
                cwd=frontend_dir,
                shell=True
            )
        
        print("⏳ 等待前端服务器启动...")
        time.sleep(3)
        
        if self.frontend_process.poll() is None:
            print("✅ 前端服务器启动成功")
            print("📍 前端地址: http://127.0.0.1:5173")
            return True
        else:
            print("❌ 前端服务器启动失败")
            return False
    
    def stop_servers(self):
        """停止所有服务器"""
        print("\n🛑 正在停止所有服务器...")
        
        if self.backend_process:
            try:
                self.backend_process.terminate()
                self.backend_process.wait(timeout=5)
                print("✅ 后端服务器已停止")
            except subprocess.TimeoutExpired:
                self.backend_process.kill()
                print("⚠️  强制停止后端服务器")
            except:
                print("⚠️  停止后端服务器时出错")
        
        if self.frontend_process:
            try:
                self.frontend_process.terminate()
                self.frontend_process.wait(timeout=5)
                print("✅ 前端服务器已停止")
            except subprocess.TimeoutExpired:
                self.frontend_process.kill()
                print("⚠️  强制停止前端服务器")
            except:
                print("⚠️  停止前端服务器时出错")
        
        print("👋 所有服务器已停止")
    
    def run(self):
        """运行启动流程"""
        try:
            self.print_banner()
            
            # 启动后端
            if not self.start_backend():
                return False
            
            print()
            
            # 启动前端
            if not self.start_frontend():
                self.stop_servers()
                return False
            
            print()
            print("=" * 60)
            print("🎉 所有服务器启动成功！")
            print("📍 访问地址:")
            print("   前端: http://127.0.0.1:5173")
            print("   后端: http://127.0.0.1:8000")
            print("   API文档: http://127.0.0.1:8000/docs")
            print("=" * 60)
            print()
            print("💡 提示: 按 Ctrl+C 停止所有服务器")
            
            # 等待用户中断
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n检测到中断信号...")
                
        except Exception as e:
            print(f"❌ 启动过程中发生错误: {e}")
            return False
        finally:
            self.stop_servers()
        
        return True

def main():
    """主函数"""
    # 检查是否在正确的目录
    current_dir = Path.cwd()
    backend_dir = current_dir / "backend"
    frontend_dir = current_dir / "project0"
    
    if not backend_dir.exists() or not frontend_dir.exists():
        print("❌ 请在包含 'backend' 和 'project0' 文件夹的目录中运行此脚本")
        print(f"当前目录: {current_dir}")
        print("请确保目录结构如下:")
        print("  vue3-learning/")
        print("  ├── backend/")
        print("  ├── project0/")
        print("  └── start_servers.py")
        return
    
    manager = ServerManager()
    manager.run()

if __name__ == "__main__":
    main()