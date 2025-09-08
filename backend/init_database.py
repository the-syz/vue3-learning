#!/usr/bin/env python3
"""
数据库初始化脚本
用于一次性创建数据库表结构和初始化数据，无需在每次程序运行时重复执行
"""
import asyncio
from tortoise import Tortoise, run_async
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

# 从database模块导入所需的组件
from database import User, Product, ChartData, CountData, Menu, Account, OrderData, VideoData, WeekUserData, RealTimePrice, init_db

async def initialize_database():
    """初始化数据库：创建连接、创建表结构、初始化数据"""
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
        print(f"连接URL: mysql://{DB_USERNAME}:******@{DB_HOST}:{DB_PORT}/{DB_NAME}")
        
        # 初始化Tortoise ORM（不依赖FastAPI应用）
        await Tortoise.init(
            db_url=db_url,
            modules={"models": ["database"]}
        )
        
        # 创建数据库表结构
        print("开始创建数据库表结构...")
        await Tortoise.generate_schemas(safe=True)
        print("数据库表结构创建完成")
        
        # 初始化数据
        print("开始初始化数据...")
        await init_db()
        print("数据初始化完成")
        
    except Exception as e:
        print(f"数据库初始化过程中发生错误: {e}")
        raise
    finally:
        # 关闭数据库连接
        await Tortoise.close_connections()
        print("数据库连接已关闭")

def main():
    """主函数，运行数据库初始化流程"""
    print("=== 数据库初始化脚本开始执行 ===")
    print("此脚本用于一次性创建数据库表结构和初始化数据")
    
    # 运行异步初始化函数
    run_async(initialize_database())
    
    print("\n=== 数据库初始化脚本执行完成 ===")
    print("后续启动FastAPI应用时，将不再自动创建表结构和初始化数据")

if __name__ == "__main__":
    main()