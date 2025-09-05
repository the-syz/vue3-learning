import asyncio
from tortoise import Tortoise
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 从database模块导入所需的模型
from database import Account, Menu

async def test_get_menu():
    # 获取数据库配置
    DB_USERNAME = os.getenv('DB_USERNAME', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '3306')
    DB_NAME = os.getenv('DB_NAME', 'vue3_project')
    
    # 构建数据库连接URL
    db_url = f"mysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    try:
        # 初始化Tortoise ORM
        await Tortoise.init(
            db_url=db_url,
            modules={"models": ["database"]}
        )
        
        print("数据库连接成功，开始测试get_menu功能...")
        
        # 模拟login_data
        username = "admin"
        password = "admin"
        
        # 用户认证部分
        try:
            account = await Account.get(username=username)
            print(f"找到用户: {username}, 类型: {account.account_type}")
            
            if account.password != password:
                print("密码错误")
            else:
                print("密码正确")
                role = account.account_type
                
                # 获取菜单数据
                menus = await account.menus.all()
                print(f"用户拥有的菜单项数量: {len(menus)}")
                
                # 打印每个菜单项的信息
                for menu in menus:
                    print(f"菜单ID: {menu.id}, 名称: {menu.name}, 路径: {menu.path}, 父ID: {menu.parent_id}")
                
                # 构建菜单树结构（复制get_menu函数中的逻辑）
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
                
                # 构建菜单树
                menu_tree = []
                for menu in menu_dict.values():
                    if menu["parent_id"] is None:
                        menu_tree.append(menu)
                    else:
                        if menu["parent_id"] in menu_dict:
                            menu_dict[menu["parent_id"]]["children"].append(menu)
                
                # 移除空的children字段
                for menu in menu_tree:
                    if not menu["children"]:
                        menu.pop("children", None)
                
                # 对于有子菜单的项，将路径设置为#
                for menu in menu_tree:
                    if "children" in menu and menu["children"]:
                        menu["path"] = "#"
                
                print("\n构建的菜单树:")
                import json
                print(json.dumps(menu_tree, ensure_ascii=False, indent=2))
                
        except Account.DoesNotExist:
            print("用户不存在")
        except Exception as e:
            print(f"测试过程中发生错误: {e}")
            import traceback
            traceback.print_exc()
    except Exception as e:
        print(f"数据库连接失败: {e}")
    finally:
        # 关闭数据库连接
        await Tortoise.close_connections()
        print("\n数据库连接已关闭")

# 运行测试
if __name__ == "__main__":
    asyncio.run(test_get_menu())