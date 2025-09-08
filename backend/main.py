from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

# 创建FastAPI应用实例
app = FastAPI(title="Vue3 Project Backend", description="基于FastAPI的后端API服务")

# 配置CORS
origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://localhost:5174",
    "http://127.0.0.1",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 导入数据库配置和API路由器
from database import register_db, init_db, start_price_generation, stop_price_generation
from api import router as api_router

# 注册数据库（关闭自动创建表结构）
register_db(app)

# 注册API路由器，添加/api前缀
app.include_router(api_router, prefix="/api")

# 添加应用启动和关闭事件处理器
@app.on_event("startup")
async def startup_event():
    print("启动实时价格数据生成任务...")
    await start_price_generation()

@app.on_event("shutdown")
async def shutdown_event():
    print("停止实时价格数据生成任务...")
    await stop_price_generation()

# 注意：数据库表结构和初始化数据已通过独立脚本init_database.py处理
# 不再在应用启动时执行这些操作，以提高性能

# 主程序启动代码（整合了run.py的功能）
if __name__ == "__main__":
    print("FastAPI服务器启动中...")
    print("访问地址: http://127.0.0.1:8000")
    print("API文档: http://127.0.0.1:8000/docs")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)