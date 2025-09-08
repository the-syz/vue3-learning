from fastapi import APIRouter, Query, HTTPException, Depends
from typing import Optional, Dict, Any, List
from pydantic import BaseModel
from database import User, Product, Menu, Account, CountData, ChartData, OrderData, VideoData, WeekUserData, RealTimePrice
import json
from datetime import datetime, timedelta

# 创建API路由器
router = APIRouter()

# Pydantic模型定义
class UserCreate(BaseModel):
    name: str
    addr: str
    age: int
    birth: str
    sex: int
    salesperson_id: Optional[int] = None


class UserUpdate(BaseModel):
    name: Optional[str] = None
    addr: Optional[str] = None
    age: Optional[int] = None
    birth: Optional[str] = None
    sex: Optional[int] = None
    salesperson_id: Optional[int] = None


class LoginData(BaseModel):
    username: str
    password: str


# Home相关API
@router.get("/home/getTableData", response_model=Dict[str, Any])
async def get_table_data():
    # 从Product表查询数据
    products = await Product.all()
    
    # 将数据库数据格式化为前端所需格式
    table_data = []
    for product in products:
        table_data.append({
            "name": product.name,
            "todayBuy": product.today_buy,
            "monthBuy": product.month_buy,
            "totalBuy": product.total_buy
        })
    
    return {
        "code": 200,
        "data": {
            "tableData": table_data
        }
    }


@router.get("/home/getOrderData", response_model=Dict[str, Any])
async def get_order_data():
    # 从OrderData表查询数据
    order_items = await OrderData.all()
    
    # 构建日期列表
    dates = sorted(list(set([item.date for item in order_items])))
    
    # 构建产品名称列表
    names = sorted(list(set([item.name for item in order_items])))
    
    # 构建数据结构
    data = []
    for date in dates:
        day_data = {}
        for name in names:
            # 查找该日期和产品的订单数据
            item = next((x for x in order_items if x.date == date and x.name == name), None)
            day_data[name] = item.value if item else 0
        data.append(day_data)
    
    # 构建返回结果
    order_data = {
        "date": dates,
        "data": data
    }
    
    return {
        "code": 200,
        "data": order_data
    }


@router.get("/home/getVideoData", response_model=Dict[str, Any])
async def get_video_data():
    # 从VideoData表查询数据
    video_items = await VideoData.all()
    
    # 将数据库数据格式化为前端所需格式
    video_data = []
    for item in video_items:
        video_data.append({
            "name": item.name,
            "value": item.value
        })
    
    return {
        "code": 200,
        "data": video_data
    }


@router.get("/home/getWeekuserData", response_model=Dict[str, Any])
async def get_weekuser_data():
    # 从WeekUserData表查询数据
    weekuser_items = await WeekUserData.all()
    
    # 将数据库数据格式化为前端所需格式
    weekuser_data = []
    for item in weekuser_items:
        weekuser_data.append({
            "date": item.date,
            "new": item.new,
            "active": item.active
        })
    
    return {
        "code": 200,
        "data": weekuser_data
    }


@router.get("/home/getCountData", response_model=Dict[str, Any])
async def get_count_data():
    # 从CountData表查询数据
    count_items = await CountData.all()
    
    # 将数据库数据格式化为前端所需格式
    count_data = []
    for item in count_items:
        count_data.append({
            "name": item.name,
            "value": item.value,
            "icon": item.icon,
            "color": item.color
        })
    
    return {
        "code": 200,
        "data": count_data
    }


@router.get("/home/getChartData", response_model=Dict[str, Any])
async def get_chart_data():
    # 构建图表数据字典
    chart_data = {}
    
    # 获取并格式化订单数据
    order_items = await OrderData.all()
    dates = sorted(list(set([item.date for item in order_items])))
    names = sorted(list(set([item.name for item in order_items])))
    
    data = []
    for date in dates:
        day_data = {}
        for name in names:
            item = next((x for x in order_items if x.date == date and x.name == name), None)
            day_data[name] = item.value if item else 0
        data.append(day_data)
    
    chart_data["orderData"] = {
        "date": dates,
        "data": data
    }
    
    # 获取并格式化视频数据
    video_items = await VideoData.all()
    video_data = []
    for item in video_items:
        video_data.append({
            "name": item.name,
            "value": item.value
        })
    
    chart_data["videoData"] = video_data
    
    # 获取并格式化周用户数据
    weekuser_items = await WeekUserData.all()
    weekuser_data = []
    for item in weekuser_items:
        weekuser_data.append({
            "date": item.date,
            "new": item.new,
            "active": item.active
        })
    
    chart_data["userData"] = weekuser_data
    
    # 从CountData表获取统计卡片数据
    count_items = await CountData.all()
    count_data = []
    for item in count_items:
        count_data.append({
            "name": item.name,
            "value": item.value,
            "icon": item.icon,
            "color": item.color
        })
    
    chart_data["countData"] = count_data
    
    return {
        "code": 200,
        "data": chart_data
    }


# User相关API
@router.get("/user/getUserData", response_model=Dict[str, Any])
async def get_user_data(name: Optional[str] = None, page: int = 1, limit: int = 10):
    # 使用select_related加载关联的salesperson数据
    query = User.all().select_related("salesperson")
    if name:
        query = query.filter(name__contains=name)
    
    total_count = await query.count()
    users = await query.offset((page - 1) * limit).limit(limit)
    
    user_list = [{
        "id": str(u.id),
        "name": u.name,
        "addr": u.addr,
        "age": u.age,
        "birth": str(u.birth),
        "sex": u.sex,
        "salesperson_id": u.salesperson.id if u.salesperson else None,
        "salesperson_name": u.salesperson.username if u.salesperson else ""
    } for u in users]
    
    return {"code": 200, "data": {"list": user_list, "count": total_count}}


@router.delete("/user/deleteUser", response_model=Dict[str, Any])
async def delete_user(id: str):
    try:
        user = await User.get(id=id)
        await user.delete()
        return {"code": 200, "message": "删除成功"}
    except Exception:
        raise HTTPException(status_code=400, detail={"code": -999, "message": "参数不正确"})


@router.post("/user/addUser", response_model=Dict[str, Any])
async def add_user(user_data: UserCreate):
    # 准备创建用户的数据
    create_data = {
        "name": user_data.name,
        "addr": user_data.addr,
        "age": user_data.age,
        "birth": user_data.birth,
        "sex": user_data.sex
    }
    
    # 如果提供了salesperson_id，查找对应的Account对象
    if user_data.salesperson_id is not None:
        try:
            salesperson = await Account.get(id=user_data.salesperson_id)
            create_data["salesperson"] = salesperson
        except Account.DoesNotExist:
            raise HTTPException(status_code=400, detail={"code": -999, "message": "指定的负责人不存在"})
    
    user = await User.create(**create_data)
    return {"code": 200, "message": "添加成功"}


@router.put("/user/editUser", response_model=Dict[str, Any])
async def edit_user(id: str, user_data: UserUpdate):
    try:
        user = await User.get(id=id)
        
        # 处理普通字段更新
        update_data = user_data.dict(exclude_unset=True, exclude={"salesperson_id"})
        for key, value in update_data.items():
            setattr(user, key, value)
        
        # 特殊处理salesperson_id字段
        if user_data.salesperson_id is not None:
            try:
                salesperson = await Account.get(id=user_data.salesperson_id)
                user.salesperson = salesperson
            except Account.DoesNotExist:
                raise HTTPException(status_code=400, detail={"code": -999, "message": "指定的负责人不存在"})
        elif "salesperson_id" in user_data.dict(exclude_unset=True):
            # 如果明确设置salesperson_id为None，则移除关联
            user.salesperson = None
        
        await user.save()
        return {"code": 200, "message": "编辑成功"}
    except Exception:
        raise HTTPException(status_code=400, detail={"code": -999, "message": "参数不正确"})


@router.get("/user/getSalespeople", response_model=Dict[str, Any])
async def get_salespeople():
    # 获取所有account_type为"user"的账户
    salespeople = await Account.filter(account_type="user")
    
    # 格式化数据，返回id和username
    salespeople_list = [
        {"id": sp.id, "username": sp.username}
        for sp in salespeople
    ]
    
    return {"code": 200, "data": salespeople_list}


# Permission相关API
@router.post("/permission/getMenu", response_model=Dict[str, Any])
async def get_menu(login_data: LoginData):
    username = login_data.username
    password = login_data.password
    
    # 用户认证
    try:
        account = await Account.get(username=username)
        if account.password != password:
            raise HTTPException(status_code=401, detail={"code": -999, "data": {"message": "密码错误"}})
        role = account.account_type
    except Account.DoesNotExist:
        raise HTTPException(status_code=401, detail={"code": -999, "data": {"message": "用户不存在"}})
    
    # 从数据库获取菜单数据
    # 获取当前用户有权限访问的所有菜单项
    menus = await account.menus.all()
    
    # 将菜单项转换为字典，便于处理
    menu_dict = {}
    for menu in menus:
        menu_dict[menu.id] = {
            "id": menu.id,
            "path": menu.path,
            "name": menu.name,
            "label": menu.label,
            "icon": menu.icon,
            "url": menu.url,
            "parent_id": menu.parent_id,
            "children": []
        }
    
    # 构建菜单树结构
    menu_tree = []
    for menu in menu_dict.values():
        if menu["parent_id"] is None:
            # 顶级菜单项
            menu_tree.append(menu)
        else:
            # 子菜单项，添加到父菜单的children中
            if menu["parent_id"] in menu_dict:
                menu_dict[menu["parent_id"]]["children"].append(menu)
    
    # 移除空的children字段
    for menu in menu_tree:
        if not menu["children"]:
            menu.pop("children", None)
    
    # 对于有子菜单的项，如果需要特殊处理（如路径设置为#），可以在这里处理
    for menu in menu_tree:
        if "children" in menu and menu["children"]:
            menu["path"] = "#"
    
    return {"code": 200, "data": {"menuList": menu_tree, "token": "fake-token-" + role, "message": "获取成功"}}

# 商品页相关API - 实时价格数据接口
@router.get("/mall/getRealTimePrice", response_model=Dict[str, Any])
async def get_real_time_price(name: Optional[str] = None):
    """获取实时价格数据"""
    query = RealTimePrice.all()
    
    # 如果指定了品牌名称，只返回该品牌的数据
    if name:
        # 检查品牌是否存在
        if name not in ["苹果", "小米", "华为", "oppo", "vivo", "一加"]:
            raise HTTPException(status_code=400, detail={"code": -999, "message": "无效的品牌名称"})
        
        # 获取该品牌的最新价格
        latest_price = await RealTimePrice.filter(name=name).order_by("-time").first()
        
        if not latest_price:
            return {"code": 200, "data": {"name": name, "value": 0, "time": str(datetime.now())}}
        
        return {
            "code": 200,
            "data": {
                "name": latest_price.name,
                "value": latest_price.value,
                "time": str(latest_price.time)
            }
        }
    else:
        # 返回所有品牌的最新价格
        all_prices = []
        for brand in ["苹果", "小米", "华为", "oppo", "vivo", "一加"]:
            latest_price = await RealTimePrice.filter(name=brand).order_by("-time").first()
            if latest_price:
                all_prices.append({
                    "name": latest_price.name,
                    "value": latest_price.value,
                    "time": str(latest_price.time)
                })
            else:
                all_prices.append({
                    "name": brand,
                    "value": 0,
                    "time": str(datetime.now())
                })
        
        return {
            "code": 200,
            "data": all_prices
        }

@router.get("/mall/getPriceHistory", response_model=Dict[str, Any])
async def get_price_history(
    name: str,
    limit: int = 100,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None
):
    """获取指定品牌的价格历史数据"""
    # 检查品牌是否存在
    if name not in ["苹果", "小米", "华为", "oppo", "vivo", "一加"]:
        raise HTTPException(status_code=400, detail={"code": -999, "message": "无效的品牌名称"})
    
    # 构建查询
    query = RealTimePrice.filter(name=name).order_by("time")
    
    # 添加时间范围过滤（如果提供）
    if start_time:
        try:
            start_datetime = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            query = query.filter(time__gte=start_datetime)
        except ValueError:
            raise HTTPException(status_code=400, detail={"code": -999, "message": "无效的开始时间格式，应为YYYY-MM-DD HH:MM:SS"})
    
    if end_time:
        try:
            end_datetime = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
            query = query.filter(time__lte=end_datetime)
        except ValueError:
            raise HTTPException(status_code=400, detail={"code": -999, "message": "无效的结束时间格式，应为YYYY-MM-DD HH:MM:SS"})
    
    # 限制返回的记录数量
    if limit > 1000:
        limit = 1000  # 最多返回1000条记录
    
    # 执行查询
    history_data = await query.limit(limit)
    
    # 格式化结果
    formatted_data = []
    for item in history_data:
        formatted_data.append({
            "time": str(item.time),
            "value": item.value
        })
    
    return {
        "code": 200,
        "data": {
            "name": name,
            "history": formatted_data
        }
    }