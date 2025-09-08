import asyncio
from tortoise import Tortoise
from database import get_db_url, RealTimePrice, _BASE_PRICES

async def test_insert_price():
    """测试插入价格数据到数据库"""
    try:
        # 连接数据库
        await Tortoise.init(
            db_url=get_db_url(),
            modules={"models": ["database"]}
        )
        
        print(f"数据库连接成功: {get_db_url()}")
        
        # 尝试插入一条测试数据
        brand = list(_BASE_PRICES.keys())[0]  # 获取第一个品牌
        price = _BASE_PRICES[brand]
        
        print(f"尝试插入测试数据: 品牌={brand}, 价格={price}")
        record = await RealTimePrice.create(
            name=brand,
            value=price
        )
        
        print(f"数据插入成功，记录ID: {record.id}")
        
        # 尝试查询数据
        count = await RealTimePrice.all().count()
        print(f"当前数据库中real_time_price表的记录总数: {count}")
        
        # 查询最新的记录
        latest_record = await RealTimePrice.filter(name=brand).order_by('-time').first()
        if latest_record:
            print(f"最新记录: 品牌={latest_record.name}, 时间={latest_record.time}, 价格={latest_record.value}")
        
    except Exception as e:
        print(f"测试过程中发生错误: {e}")
    finally:
        # 关闭数据库连接
        await Tortoise.close_connections()
        print("数据库连接已关闭")

if __name__ == "__main__":
    asyncio.run(test_insert_price())