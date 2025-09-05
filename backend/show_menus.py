#!/usr/bin/env python3
"""
显示菜单数据脚本
用于查看数据库中菜单项的数据
"""
import asyncio
from tortoise import Tortoise, run_async
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

# 从database模块导入所需的组件
from database import Menu

async def show_menus():
    """显示菜单数据"""
    try:
        # 获取数据库配置参数
        DB_USERNAME = os.getenv('DB_USERNAME', 'root')
        DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
        DB_HOST = os.getenv('DB_HOST', 'localhost')
        DB_PORT = os.getenv('DB_PORT', '3306')
        DB_NAME = os.getenv('DB_NAME', 'vue3_project')
        
        # 构建数据库连接URL
        db_url = f"mysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        print(f"正在连接到数据库: {DB_USERNAME}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
        
        # 初始化Tortoise ORM（不依赖FastAPI应用）
        await Tortoise.init(
            db_url=db_url,
            modules={"models": ["database"]}
        )
        
        # 获取所有菜单项
        menus = await Menu.all()
        print(f"找到 {len(menus)} 个菜单项")
        
        # 显示每个菜单项的数据
        for menu in menus:
            print(f"ID: {menu.id}, Name: {menu.name}, URL: {menu.url}, Parent ID: {menu.parent_id}")
        
    except Exception as e:
        print(f"显示菜单数据过程中发生错误: {e}")
        raise
    finally:
        # 关闭数据库连接
        await Tortoise.close_connections()
        print("数据库连接已关闭")

def main():
    """主函数，运行菜单显示流程"""
    print("=== 菜单数据显示脚本开始执行 ===")
    
    # 运行异步显示函数
    run_async(show_menus())
    
    print("\n=== 菜单数据显示脚本执行完成 ===")

if __name__ == "__main__":
    main()