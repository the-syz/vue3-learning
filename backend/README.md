# Vue 3 电商管理系统 - 后端

这是电商管理系统的后端部分，基于 FastAPI 和 Tortoise ORM 构建，为 Vue 3 前端项目提供 API 服务和数据支持。

## 技术栈

- **Web框架**: FastAPI
- **ASGI服务器**: Uvicorn
- **ORM**: Tortoise ORM
- **数据验证**: Pydantic
- **数据库**: MySQL (asyncmy驱动)
- **环境管理**: python-dotenv
- **数据生成**: Faker

## 项目结构

```
backend/
├── .env            # 环境变量配置
├── .gitignore      # Git忽略文件
├── main.py         # 主程序文件（应用初始化和配置）
├── database.py     # 数据库相关代码（模型定义和配置）
├── api.py          # API端点实现
├── requirements.txt # 项目依赖
└── README.md       # 项目说明
```

### 文件说明
- **main.py**: 主程序文件，负责应用初始化、CORS配置和整合其他模块
- **database.py**: 数据库相关代码，包含数据库模型定义、连接配置和初始化数据逻辑
- **api.py**: API端点实现，包含所有业务逻辑和API路由
- **.env**: 环境变量配置文件，包含数据库连接信息和服务器配置
- **requirements.txt**: 项目依赖清单

## 功能特性

- 完整的 RESTful API 实现
- 基于 Tortoise ORM 的数据库操作
- MySQL 数据库支持
- CORS 跨域支持
- 自动生成 API 文档
- 独立的数据库初始化脚本

## 安装依赖

在项目根目录执行以下命令安装依赖：

```bash
pip install -r requirements.txt
```

## 启动服务器

方法一：直接运行 main.py

```bash
python main.py
```

方法二：使用 uvicorn 命令

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

## API 文档

启动服务器后，可以通过以下地址访问自动生成的 API 文档：

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## 已实现的 API 端点

### Home 相关
- `GET /api/home/getTableData` - 获取产品表格数据
- `GET /api/home/getCountData` - 获取模拟的统计数据
- `GET /api/home/getChartData` - 获取图表数据（从ChartData表读取）

### User 相关
- `GET /api/user/getUserData` - 获取用户列表（支持分页和搜索）
- `DELETE /api/user/deleteUser` - 删除用户
- `POST /api/user/addUser` - 添加用户
- `PUT /api/user/editUser` - 编辑用户

### Permission 相关
- `POST /api/permission/getMenu` - 登录认证并获取菜单权限

## 数据存储和初始化

### 数据库表结构
- **users**: 存储用户信息，每个用户随机分配给一个员工账户
- **products**: 存储产品销售数据
- **chart_data**: 存储图表数据（orderData、videoData、userData）
- **accounts**: 存储登录账户信息
- **menus**: 存储菜单信息，与账户通过多对多关系关联

### 数据初始化改进
1. **用户数据优化**:
   - 初始化顺序调整：先创建员工账户，再创建用户数据
   - 用户地址格式优化：仅包含省市信息
   - 所有用户（包括随机生成的200个用户）都会随机分配给现有员工账户
2. **图表数据持久化**：数据库初始化时会自动生成并存储三种图表数据
3. **账户系统**：包含1个管理员账户和3个普通员工账户（xiaoxiao、zhangsan、lisi），权限分配通过多对多关系实现

## 默认账号

- Admin 账号：username=admin, password=admin
- 普通用户账号：username=xiaoxiao, password=xiaoxiao

## 数据库

项目使用 MySQL 数据库，通过独立的初始化脚本创建表结构和初始化数据：

### 1. 准备工作

1. 登录MySQL：
   ```bash
   mysql -u root -p
   ```

2. 创建数据库：
   ```sql
   CREATE DATABASE vue3_project CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

3. 修改 `.env` 文件中的数据库配置：
   ```
   DB_USERNAME=root
   DB_PASSWORD=password
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=vue3_project
   ```

### 2. 运行数据库初始化脚本

在首次运行项目前，需要先运行独立的数据库初始化脚本，该脚本只需运行一次：

```bash
python init_database.py
```

这个脚本会：
- 连接到MySQL数据库
- 创建所有必要的表结构
- 初始化示例数据（用户、产品、菜单等）

### 3. 注意事项

- 数据库初始化只需执行一次
- 后续启动FastAPI应用时，将不再自动创建表结构和初始化数据
- 如果需要重新初始化数据库，可以再次运行该脚本（会保留现有数据）

## 注意事项

1. 本项目仅用于开发和学习目的
2. 生产环境中请修改默认账号密码
3. 生产环境建议使用 PostgreSQL 或 MySQL 数据库