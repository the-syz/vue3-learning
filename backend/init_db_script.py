import asyncio
from fastapi import FastAPI
from database import register_db, init_db

# 创建一个临时的FastAPI应用来注册数据库
def create_app():
    app = FastAPI()
    register_db(app)
    return app

async def main():
    # 创建应用并注册数据库
    app = create_app()
    
    # 初始化数据库（创建表并插入初始数据）
    print("开始初始化数据库...")
    await init_db()
    print("数据库初始化完成！")

if __name__ == "__main__":
    asyncio.run(main())