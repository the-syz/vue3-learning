# Vue 3 电商管理系统

这是一个基于 Vue 3 和 FastAPI 的前后端分离电商管理系统，包含数据可视化、商品管理、用户管理等功能模块。

## 项目特点

- 前后端分离架构，前端基于 Vue 3，后端基于 FastAPI
- 响应式布局设计，适配不同设备屏幕
- 数据可视化展示，使用 ECharts 绘制各类图表
- 动态路由和权限管理
- 实时数据更新和模拟

## 技术栈

### 前端
- **框架**: Vue 3
- **UI组件库**: Element Plus
- **状态管理**: Pinia
- **路由**: Vue Router 4
- **构建工具**: Vite
- **图表库**: ECharts
- **样式预处理**: Less
- **模拟数据**: Mock.js
- **HTTP请求**: Axios

### 后端
- **框架**: FastAPI
- **ASGI服务器**: Uvicorn
- **ORM**: Tortoise ORM
- **数据验证**: Pydantic
- **数据库**: MySQL (asyncmy驱动)
- **环境管理**: python-dotenv
- **数据生成**: Faker

## 项目结构

```
vue3_learning/
├── backend/            # 后端项目目录
│   ├── main.py         # FastAPI主入口
│   ├── api.py          # API路由定义
│   ├── database.py     # 数据库配置
│   ├── requirements.txt # 后端依赖
│   └── ...
├── project0/           # 前端项目目录
│   ├── src/            # 前端源码
│   │   ├── api/        # API接口定义
│   │   ├── components/ # 公共组件
│   │   ├── views/      # 页面视图
│   │   ├── router/     # 路由配置
│   │   ├── stores/     # Pinia状态管理
│   │   └── main.js     # Vue应用入口
│   ├── package.json    # 前端依赖配置
│   └── vite.config.js  # Vite配置
├── start.bat           # 快速启动脚本
├── start_servers.py    # 服务器启动脚本
└── 启动说明.md         # 项目启动说明
```

## 快速开始

### 环境准备

1. 确保安装了 Node.js (v16+) 和 Python (v3.8+)
2. 安装前端依赖
   ```bash
   cd project0
   npm install
   ```
3. 安装后端依赖
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

### 启动项目

#### 方法一：使用批处理脚本（Windows）
```bash
start.bat
```

#### 方法二：手动启动

1. 启动后端服务器
   ```bash
   cd backend
   python main.py
   ```

2. 启动前端开发服务器
   ```bash
   cd project0
   npm run dev
   ```

3. 访问系统
   打开浏览器，访问 http://localhost:5173/

## 功能模块

### 1. 登录系统
- 用户认证和授权
- 路由守卫和权限控制

### 2. 首页数据看板
- 销售数据统计图表
- 课程购买数据表格
- 实时数据更新

### 3. 商品管理
- 商品列表展示
- 价格趋势图表
- 实时价格更新（2-5秒更新一次）

### 4. 用户管理
- 用户信息展示
- 用户行为分析

## 数据模拟

项目使用 Mock.js 进行前端数据模拟，主要模拟以下数据：
- 首页表格数据
- 图表统计数据
- 商品价格数据

## 特殊功能

### 实时价格更新

商品管理页面支持实时价格更新功能，系统会每2-5秒自动获取最新价格数据并更新图表显示。

### 数据可视化

系统使用 ECharts 实现了多种数据可视化图表：
- 柱状图：展示销售数据
- 折线图：展示价格趋势
- 饼图：展示用户分布

### 响应式布局

系统采用响应式设计，适配不同屏幕尺寸的设备，提供良好的用户体验。

## 开发说明

### 前端开发

1. 组件开发规范：遵循 Vue 3 Composition API 风格
2. 样式规范：使用 Less 预处理，统一主题色彩
3. 路由配置：支持静态路由和动态路由两种方式

### 后端开发

1. API 设计：遵循 RESTful 规范
2. 数据库操作：使用 Tortoise ORM 进行异步数据库操作
3. 数据验证：使用 Pydantic 进行请求和响应数据验证

## 注意事项

1. 项目使用模拟数据，实际部署时需要配置真实数据库
2. 开发环境下前端默认端口为 5173，后端默认端口为 8000
3. 项目中的路由权限需要在登录后获取，刷新页面会尝试从 localStorage 恢复状态
4. 商品价格图表支持鼠标悬停显示数据点详情

## License

MIT