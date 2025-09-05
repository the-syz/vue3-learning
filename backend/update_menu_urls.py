#!/usr/bin/env python3
"""
更新菜单URL脚本
用于更新数据库中菜单项的URL字段，使其与前端组件路径匹配
"""
import asyncio
from tortoise import Tortoise, run_async
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

# 从database模块导入所需的组件
from database import Menu

async def update_menu_urls():
    """更新菜单URL字段"""
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
        
        # 定义菜单URL映射
        menu_url_mapping = {
            "home": "home/index",
            "mall": "mall/index",
            "user": "user/index",
            "page1": "page1/index",
            "page2": "page2/index"
        }
        
        # 获取所有菜单项
        menus = await Menu.all()
        print(f"找到 {len(menus)} 个菜单项")
        
        # 更新每个菜单项的URL
        updated_count = 0
        for menu in menus:
            if menu.name in menu_url_mapping:
                old_url = menu.url
                new_url = menu_url_mapping[menu.name]
                
                # 只有当URL需要更新时才更新
                if old_url != new_url:
                    menu.url = new_url
                    await menu.save()
                    print(f"更新菜单 '{menu.name}': '{old_url}' -> '{new_url}'")
                    updated_count += 1
        
        print(f"成功更新 {updated_count} 个菜单项的URL")
        
    except Exception as e:
        print(f"更新菜单URL过程中发生错误: {e}")
        raise
    finally:
        # 关闭数据库连接
        await Tortoise.close_connections()
        print("数据库连接已关闭")

def main():
    """主函数，运行菜单URL更新流程"""
    print("=== 菜单URL更新脚本开始执行 ===")
    
    # 运行异步更新函数
    run_async(update_menu_urls())
    
    print("\n=== 菜单URL更新脚本执行完成 ===")

if __name__ == "__main__":
    main()