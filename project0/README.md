# Vue 3 电商管理系统 - 前端

这是电商管理系统的前端部分，基于 Vue 3 和 Vite 构建，提供数据可视化、商品管理和用户管理等功能模块。

## 技术栈

- **框架**: Vue 3
- **UI组件库**: Element Plus
- **状态管理**: Pinia
- **路由**: Vue Router 4
- **构建工具**: Vite
- **图表库**: ECharts
- **样式预处理**: Less
- **模拟数据**: Mock.js
- **HTTP请求**: Axios

## 项目结构

```
project0/
├── src/            # 前端源码
│   ├── api/        # API接口定义
│   ├── assets/     # 静态资源
│   ├── components/ # 公共组件
│   ├── config/     # 配置文件
│   ├── router/     # 路由配置
│   ├── stores/     # Pinia状态管理
│   ├── views/      # 页面视图
│   ├── App.vue     # 根组件
│   └── main.js     # Vue应用入口
├── public/         # 静态资源目录
├── index.html      # HTML入口文件
├── package.json    # 项目依赖配置
└── vite.config.js  # Vite配置文件
```

## 开发命令

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build

# 预览生产构建
npm run preview
```

## 主要功能

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

## 路由配置

系统使用 Vue Router 4 进行路由管理，支持静态路由和动态路由两种方式。主要路由包括：
- `/login`: 登录页面
- `/main`: 主页面框架
  - `/home`: 首页数据看板
  - `/mall`: 商品管理页面
  - `/user`: 用户管理页面
- `/404`: 页面不存在

## 状态管理

系统使用 Pinia 进行状态管理，主要存储：
- 用户登录状态
- 菜单权限
- 全局配置

## 开发说明

1. 组件开发规范：遵循 Vue 3 Composition API 风格
2. 样式规范：使用 Less 预处理，统一主题色彩
3. API 调用：统一封装在 `src/api/api.js` 中
4. Mock 数据：开发环境下使用 Mock.js 模拟接口数据

## 注意事项

1. 开发环境下默认端口为 5173
2. 前端请求默认指向 `http://localhost:8000`（后端服务）
3. 登录状态和路由信息会保存在 localStorage 中，刷新页面会尝试恢复

详细项目说明请参考根目录的 README.md 文件。
