from fastapi import APIRouter, Query, HTTPException, Depends
from typing import Optional, Dict, Any
from pydantic import BaseModel
from database import User, Product, Menu, Account, CountData, ChartData
import json

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
    # 从ChartData表查询数据
    chart_items = await ChartData.all()
    
    # 构建图表数据字典
    chart_data = {}
    for item in chart_items:
        chart_data[item.data_type] = json.loads(item.content)
    
    # 确保返回的格式符合前端要求
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