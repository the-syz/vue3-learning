from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.fastapi import register_tortoise
from typing import Dict, Any, List, Optional
import os
import json
import asyncio
import random
import time
from datetime import datetime

# 数据库模型定义

def get_db_url() -> str:
    # 从环境变量获取数据库配置参数
    DB_USERNAME = os.getenv('DB_USERNAME', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '123456')  # 使用.env中的密码作为默认值
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '3306')
    DB_NAME = os.getenv('DB_NAME', 'vue3_project')
    
    # 构建数据库连接字符串
    DATABASE_URL = f"mysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return DATABASE_URL


# 订单数据模型 - 对应order_data表
class OrderData(Model):
    id = fields.IntField(pk=True, generated=True)
    date = fields.CharField(max_length=20)  # 日期
    name = fields.CharField(max_length=100)  # 产品名称
    value = fields.IntField()  # 订单数量
    
    class Meta:
        table = "order_data"


# 视频数据模型 - 对应video_data表
class VideoData(Model):
    id = fields.IntField(pk=True, generated=True)
    name = fields.CharField(max_length=100)  # 品牌名称
    value = fields.IntField()  # 视频数量
    
    class Meta:
        table = "video_data"


# 周用户数据模型 - 对应week_user_data表
class WeekUserData(Model):
    id = fields.IntField(pk=True, generated=True)
    date = fields.CharField(max_length=20)  # 星期几
    new = fields.IntField()  # 新用户数
    active = fields.IntField()  # 活跃用户数
    
    class Meta:
        table = "week_user_data"

# 实时价格数据模型 - 对应real_time_price表
class RealTimePrice(Model):
    id = fields.IntField(pk=True, generated=True)
    name = fields.CharField(max_length=100)  # 品牌名称
    time = fields.DatetimeField(auto_now_add=True)  # 时间戳
    value = fields.FloatField()  # 价格值
    
    class Meta:
        table = "real_time_price"
        indexes = [
            ("name", "time"),  # 在name和time字段上创建索引，提高查询效率
        ]

# 存储各品牌的基础价格，用于生成浮动价格
_BASE_PRICES = {
    "苹果": 5000.0,
    "小米": 3000.0,
    "华为": 4000.0,
    "oppo": 2500.0,
    "vivo": 2600.0,
    "一加": 3500.0
}

# 价格浮动范围百分比
_PRICE_FLUCTUATION_RANGE = 0.05  # 5%

# 最大记录数
MAX_RECORDS_PER_BRAND = 1000

# 全局变量，用于存储当前价格
_current_prices = _BASE_PRICES.copy()

# 数据生成任务标志
_data_generation_task: Optional[asyncio.Task] = None

async def generate_real_time_price():
    """持续生成实时价格数据"""
    global _current_prices, _data_generation_task
    
    # 创建初始数据（每个品牌生成一些历史数据）
    await init_initial_price_data()
    
    try:
        while True:
            # 为每个品牌生成新的价格数据
            for brand, base_price in _BASE_PRICES.items():
                # 生成随机浮动值（在基础价格的±5%范围内）
                fluctuation = random.uniform(-_PRICE_FLUCTUATION_RANGE, _PRICE_FLUCTUATION_RANGE)
                new_price = _current_prices[brand] * (1 + fluctuation)
                
                # 确保价格不会波动太大
                max_price = base_price * (1 + _PRICE_FLUCTUATION_RANGE * 2)
                min_price = base_price * (1 - _PRICE_FLUCTUATION_RANGE * 2)
                new_price = max(min(new_price, max_price), min_price)
                
                # 更新当前价格
                _current_prices[brand] = new_price
                
                # 创建新的价格记录
                await RealTimePrice.create(
                    name=brand,
                    value=round(new_price, 2)
                )
                
                # 清理旧数据，确保每个品牌不超过1000条记录
                await cleanup_old_records(brand)
            
            # 等待一段时间后再次生成数据（每2-5秒生成一次）
            await asyncio.sleep(random.uniform(2, 5))
    except asyncio.CancelledError:
        print("实时价格数据生成任务已取消")
    except Exception as e:
        print(f"实时价格数据生成任务出错: {e}")

async def init_initial_price_data():
    """初始化初始价格数据"""
    # 检查是否已有数据
    count = await RealTimePrice.all().count()
    if count > 0:
        # 如果已有数据，更新当前价格为最新价格
        for brand in _BASE_PRICES.keys():
            latest_price = await RealTimePrice.filter(name=brand).order_by('-time').first()
            if latest_price:
                _current_prices[brand] = latest_price.value
        return
    
    # 为每个品牌生成一些历史数据
    now = datetime.now()
    for brand, base_price in _BASE_PRICES.items():
        print(f"初始化{brand}的价格数据...")
        # 生成50条历史数据，时间间隔为5秒
        for i in range(50):
            # 生成基于基础价格的随机价格
            price = base_price * (1 + random.uniform(-0.1, 0.1))
            # 计算历史时间戳
            historical_time = now - datetime.timedelta(seconds=5*(50-i))
            # 创建历史价格记录
            await RealTimePrice.create(
                name=brand,
                value=round(price, 2),
                time=historical_time
            )
        # 更新当前价格
        _current_prices[brand] = base_price

async def cleanup_old_records(brand: str):
    """清理指定品牌的旧记录，确保不超过1000条"""
    # 计算需要删除的记录数量
    count = await RealTimePrice.filter(name=brand).count()
    if count > MAX_RECORDS_PER_BRAND:
        # 查询需要删除的记录
        records_to_delete = await RealTimePrice.filter(name=brand).order_by('time').limit(count - MAX_RECORDS_PER_BRAND)
        # 批量删除
        for record in records_to_delete:
            await record.delete()

async def start_price_generation():
    """启动价格生成任务"""
    global _data_generation_task
    
    if _data_generation_task and not _data_generation_task.done():
        print("价格生成任务已经在运行")
        return
    
    _data_generation_task = asyncio.create_task(generate_real_time_price())
    print("实时价格数据生成任务已启动")

async def stop_price_generation():
    """停止价格生成任务"""
    global _data_generation_task
    
    if _data_generation_task and not _data_generation_task.done():
        _data_generation_task.cancel()
        try:
            await _data_generation_task
        except asyncio.CancelledError:
            pass
        print("实时价格数据生成任务已停止")
    
    _data_generation_task = None


class User(Model):
    id = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=100)
    addr = fields.CharField(max_length=200)
    age = fields.IntField()
    birth = fields.DateField()
    sex = fields.IntField()  # 0: 女, 1: 男
    create_time = fields.DatetimeField(auto_now_add=True)
    # 外键关联到Account表，表示这个客户由哪个员工负责
    salesperson = fields.ForeignKeyField('models.Account', related_name='customers', null=True)

    class Meta:
        table = "users"


class Product(Model):
    id = fields.IntField(pk=True, generated=True)
    name = fields.CharField(max_length=100)
    today_buy = fields.IntField()
    month_buy = fields.IntField()
    total_buy = fields.IntField()

    class Meta:
        table = "products"


class ChartData(Model):
    id = fields.IntField(pk=True, generated=True)
    data_type = fields.CharField(max_length=50)  # orderData, videoData, userData
    content = fields.TextField()  # 存储JSON格式的数据

    class Meta:
        table = "chart_data"


class CountData(Model):
    id = fields.IntField(pk=True, generated=True)
    name = fields.CharField(max_length=100)  # 统计项名称
    value = fields.IntField()  # 统计值
    icon = fields.CharField(max_length=100)  # 图标名称
    color = fields.CharField(max_length=20)  # 颜色值

    class Meta:
        table = "count_data"


# 登录账户表
class Account(Model):
    id = fields.IntField(pk=True, generated=True)
    username = fields.CharField(max_length=50, unique=True)  # 用户名，唯一
    password = fields.CharField(max_length=100)  # 密码
    account_type = fields.CharField(max_length=20)  # 账户类型：admin或user
    create_time = fields.DatetimeField(auto_now_add=True)  # 创建时间

    class Meta:
        table = "accounts"

# 菜单项表
class Menu(Model):
    id = fields.IntField(pk=True, generated=True)
    path = fields.CharField(max_length=100)
    name = fields.CharField(max_length=100)
    label = fields.CharField(max_length=100)
    icon = fields.CharField(max_length=100)
    url = fields.CharField(max_length=100)
    parent_id = fields.IntField(null=True)  # 父菜单ID，用于树形结构

    # 多对多关系：一个菜单项可以被多个账户访问
    accounts = fields.ManyToManyField('models.Account', related_name='menus', through='account_menu')

    class Meta:
        table = "menus"


# 注册数据库
def register_db(app):
    register_tortoise(
        app,
        db_url=get_db_url(),
        modules={"models": ["database"]},
        generate_schemas=False,  # 不再自动创建表结构，通过独立脚本处理
        add_exception_handlers=True,
    )


# 初始化数据
import random
import datetime
from faker import Faker

async def init_db():
    # 初始化Faker实例用于生成随机数据
    fake = Faker('zh_CN')  # 使用中文数据生成器
    
    # 首先检查并初始化账户数据（确保先有员工账户，再创建用户数据）
    account_count = await Account.all().count()
    if account_count == 0:
        # 创建管理员账户
        admin_account = await Account.create(
            username="admin",
            password="admin",  # 注意：实际项目中应该使用加密存储密码
            account_type="admin"
        )
        
        # 创建3个普通员工账户
        employee_accounts = []
        employee_info = [
            {"username": "xiaoxiao", "password": "xiaoxiao"},
            {"username": "zhangsan", "password": "zhangsan"},
            {"username": "lisi", "password": "lisi"}
        ]
        
        for emp in employee_info:
            employee = await Account.create(
                username=emp["username"],
                password=emp["password"],
                account_type="user"
            )
            employee_accounts.append(employee)
    else:
        # 如果账户已存在，获取所有普通员工账户
        employee_accounts = await Account.filter(account_type="user")
    
    # 检查并初始化菜单数据
    menu_count = await Menu.all().count()
    if menu_count == 0:
        # 创建所有菜单项（不包含角色信息，通过多对多关系分配）
        menus = [
            {"path": "/home", "name": "home", "label": "首页", "icon": "house", "url": "Home", "parent_id": None},
            {"path": "/mall", "name": "mall", "label": "商品管理", "icon": "video-play", "url": "Mall", "parent_id": None},
            {"path": "/user", "name": "user", "label": "用户管理", "icon": "user", "url": "User", "parent_id": None},
            {"path": "other", "name": "other", "label": "其他", "icon": "location", "url": "", "parent_id": None},
            {"path": "/page1", "name": "page1", "label": "页面1", "icon": "setting", "url": "Page1", "parent_id": 4},
            {"path": "/page2", "name": "page2", "label": "页面2", "icon": "setting", "url": "Page2", "parent_id": 4}
        ]
        
        # 保存所有菜单项并存储它们的引用
        created_menus = []
        for menu_data in menus:
            menu = await Menu.create(**menu_data)
            created_menus.append(menu)
            
        # 分配菜单权限：管理员拥有所有菜单权限
        admin_menu_ids = [1, 2, 3, 4, 5, 6]  # 所有菜单ID
        admin_menus = await Menu.filter(id__in=admin_menu_ids)
        admin_account = await Account.get(username="admin")
        await admin_account.menus.add(*admin_menus)
        
        # 分配菜单权限：所有普通员工只有首页和用户管理菜单权限
        user_menu_ids = [1, 3]  # 首页和用户管理菜单ID
        user_menus = await Menu.filter(id__in=user_menu_ids)
        for employee in employee_accounts:
            await employee.menus.add(*user_menus)
    else:
        # 如果菜单项已存在，获取所有菜单项
        created_menus = await Menu.all()
    
    # 检查并初始化用户数据
    user_count = await User.all().count()
    if user_count == 0:
        # 初始化客户数据（注意：这里是客户信息，不是登录账户）
        # 先创建3个示例用户
        mock_users = [
            {
                "name": "张三",
                "addr": "北京市海淀区",
                "age": 25,
                "birth": "1998-01-15",
                "sex": 1
            },
            {
                "name": "李四",
                "addr": "上海市浦东新区",
                "age": 30,
                "birth": "1993-05-20",
                "sex": 1
            },
            {
                "name": "王五",
                "addr": "广州市天河区",
                "age": 28,
                "birth": "1995-09-10",
                "sex": 0
            }
        ]
        
        # 先创建示例用户并分配给员工
        for user in mock_users:
            if employee_accounts:
                user["salesperson"] = random.choice(employee_accounts)  # 随机分配给一个员工
            await User.create(**user)
        
        # 生成200个随机用户数据
        print("开始生成200个随机用户数据...")
        batch_size = 50  # 分批创建以提高性能
        total_users = 200
        
        # 随机用户数据列表
        random_users = []
        
        # 中国省份和城市列表，用于生成简洁地址
        provinces = ['北京市', '上海市', '广东省', '江苏省', '浙江省', '山东省', '河南省', '四川省', '湖北省', '湖南省']
        cities = {
            '北京市': ['北京市'],
            '上海市': ['上海市'],
            '广东省': ['广州市', '深圳市', '东莞市', '佛山市', '珠海市'],
            '江苏省': ['南京市', '苏州市', '无锡市', '常州市', '南通市'],
            '浙江省': ['杭州市', '宁波市', '温州市', '嘉兴市', '湖州市'],
            '山东省': ['济南市', '青岛市', '烟台市', '潍坊市', '临沂市'],
            '河南省': ['郑州市', '洛阳市', '开封市', '安阳市', '新乡市'],
            '四川省': ['成都市', '绵阳市', '德阳市', '自贡市', '泸州市'],
            '湖北省': ['武汉市', '宜昌市', '襄阳市', '荆州市', '黄石市'],
            '湖南省': ['长沙市', '株洲市', '湘潭市', '衡阳市', '邵阳市']
        }
        
        for _ in range(total_users):
            # 随机生成性别
            sex = random.randint(0, 1)
            # 随机生成年龄（18-65岁）
            age = random.randint(18, 65)
            # 随机生成出生日期
            current_year = datetime.datetime.now().year
            birth_year = current_year - age
            birth_month = random.randint(1, 12)
            days_in_month = 31
            if birth_month in [4, 6, 9, 11]:
                days_in_month = 30
            elif birth_month == 2:
                # 简单判断闰年
                if (birth_year % 4 == 0 and birth_year % 100 != 0) or (birth_year % 400 == 0):
                    days_in_month = 29
                else:
                    days_in_month = 28
            birth_day = random.randint(1, days_in_month)
            birth_date = f"{birth_year}-{birth_month:02d}-{birth_day:02d}"
            
            # 随机生成简洁地址（仅包含省和市）
            province = random.choice(provinces)
            city = random.choice(cities[province])
            simple_address = f"{province}{city}"
            
            # 随机生成用户数据
            user_data = {
                "name": fake.name_male() if sex == 1 else fake.name_female(),
                "addr": simple_address,
                "age": age,
                "birth": birth_date,
                "sex": sex
            }
            
            # 随机分配一个员工
            if employee_accounts:
                user_data["salesperson"] = random.choice(employee_accounts)
            
            random_users.append(user_data)
        
        # 分批创建用户
        for i in range(0, len(random_users), batch_size):
            batch = random_users[i:i+batch_size]
            for user in batch:
                await User.create(**user)
            
        print(f"已生成{len(random_users)}个随机用户数据并随机分配给员工")
    
    # 检查并初始化产品数据
    product_count = await Product.all().count()
    if product_count == 0:
        mock_products = [
            {"name": "oppo", "today_buy": 500, "month_buy": 3500, "total_buy": 22000},
            {"name": "vivo", "today_buy": 300, "month_buy": 2200, "total_buy": 24000},
            {"name": "苹果", "today_buy": 800, "month_buy": 4500, "total_buy": 65000},
            {"name": "小米", "today_buy": 1200, "month_buy": 6500, "total_buy": 45000},
            {"name": "三星", "today_buy": 300, "month_buy": 2000, "total_buy": 34000},
            {"name": "魅族", "today_buy": 350, "month_buy": 3000, "total_buy": 22000}
        ]
        for product in mock_products:
            await Product.create(**product)
    
    # 检查并初始化统计数据
    count_data_count = await CountData.all().count()
    if count_data_count == 0:
        mock_count_data = [
            {"name": "今日支付订单", "value": 1234, "icon": "SuccessFilled", "color": "#2ec7c9"},
            {"name": "今日收藏订单", "value": 210, "icon": "StarFilled", "color": "#ffb980"},
            {"name": "今日未支付订单", "value": 1234, "icon": "GoodsFilled", "color": "#5ab1ef"},
            {"name": "本月支付订单", "value": 1234, "icon": "SuccessFilled", "color": "#2ec7c9"},
            {"name": "本月收藏订单", "value": 210, "icon": "StarFilled", "color": "#ffb980"},
            {"name": "本月未支付订单", "value": 1234, "icon": "GoodsFilled", "color": "#5ab1ef"}
        ]
        for item in mock_count_data:
            await CountData.create(**item)
        
        print("已初始化统计数据")
    
    # 初始化订单数据
    order_data_count = await OrderData.all().count()
    if order_data_count == 0:
        # 从指定的数据创建订单数据
        dates = [
            "2019-10-01", "2019-10-02", "2019-10-03", "2019-10-04",
            "2019-10-05", "2019-10-06", "2019-10-07"
        ]
        data = [
            {"苹果": 3839, "小米": 1423, "华为": 4965, "oppo": 3334, "vivo": 2820, "一加": 4751},
            {"苹果": 3560, "小米": 2099, "华为": 3192, "oppo": 4210, "vivo": 1283, "一加": 1613},
            {"苹果": 1864, "小米": 4598, "华为": 4202, "oppo": 4377, "vivo": 4123, "一加": 4750},
            {"苹果": 2634, "小米": 1458, "华为": 4155, "oppo": 2847, "vivo": 2551, "一加": 1733},
            {"苹果": 3622, "小米": 3990, "华为": 2860, "oppo": 3870, "vivo": 1852, "一加": 1712},
            {"苹果": 2004, "小米": 1864, "华为": 1395, "oppo": 1315, "vivo": 4051, "一加": 2293},
            {"苹果": 3797, "小米": 3936, "华为": 3642, "oppo": 4408, "vivo": 3374, "一加": 3874}
        ]
        
        # 拆分数据并存储
        for i, date in enumerate(dates):
            day_data = data[i]
            for name, value in day_data.items():
                await OrderData.create(date=date, name=name, value=value)
        
        print("已初始化订单数据")
    
    # 初始化视频数据
    video_data_count = await VideoData.all().count()
    if video_data_count == 0:
        # 创建视频数据
        video_data = [
            {"name": "小米", "value": 2999},
            {"name": "苹果", "value": 5999},
            {"name": "vivo", "value": 1500},
            {"name": "oppo", "value": 1999},
            {"name": "魅族", "value": 2200},
            {"name": "三星", "value": 4500}
        ]
        
        for item in video_data:
            await VideoData.create(**item)
        
        print("已初始化视频数据")
    
    # 初始化周用户数据
    week_user_data_count = await WeekUserData.all().count()
    if week_user_data_count == 0:
        # 创建周用户数据
        week_user_data = [
            {"date": "周一", "new": 5, "active": 200},
            {"date": "周二", "new": 10, "active": 500},
            {"date": "周三", "new": 12, "active": 550},
            {"date": "周四", "new": 60, "active": 800},
            {"date": "周五", "new": 65, "active": 550},
            {"date": "周六", "new": 53, "active": 770},
            {"date": "周日", "new": 33, "active": 170}
        ]
        
        for item in week_user_data:
            await WeekUserData.create(**item)
        
        print("已初始化周用户数据")
    
    # 如果chart_data表存在，删除它
    chart_data_count = await ChartData.all().count()
    if chart_data_count > 0:
        await ChartData.all().delete()
        print("已删除chart_data表中的所有数据")