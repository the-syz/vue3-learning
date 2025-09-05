import { createRouter, createWebHashHistory } from 'vue-router';
import { useAllStore } from '@/stores/index.js';

// 基础路由配置
const routes = [
  {
    path: '/',
    name: 'main',
    component: () => import('@/views/main.vue'),
    redirect: '/home',
    children: []
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/login.vue')
  },
  // 404页面路由
  {
    path: '/404',
    name: '404',
    component: () => import('@/views/404.vue')
  },
  // 重定向所有未匹配的路由到404页面
  {
    path: '/:pathMatch(.*)*',
    redirect: '/404'
  }
]

// 创建路由
const router = createRouter({
  // 设置路由模式
  history: createWebHashHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const store = useAllStore();
  const token = store.state.token;
  const menuList = JSON.parse(localStorage.getItem('menuList') || '[]');
  
  // 确保token和menuList是有效的
  if (!token) {
    // 如果没有token，清除相关本地存储并跳转到登录页
    localStorage.removeItem('token');
    localStorage.removeItem('menuList');
    localStorage.removeItem('store');
    
    if (to.name !== 'login') {
      next({ name: 'login' });
    } else {
      next();
    }
    return;
  }
  
  // 如果有token且是登录页
  if (token && to.name === 'login') {
    // 跳转到首页
    next({ path: '/home' });
    return;
  }
  
  // 增强404页面的处理逻辑：如果在404页面且有token，提供退出或重试机制
  if (to.path === '/404' && token) {
    console.log('用户进入404页面，但仍有有效token');
    // 继续导航到404页面，但在组件中可以处理退出逻辑
    next();
    return;
  }
  
  // 如果有token，确保菜单数据正确加载
  if (token) {
    // 如果store中没有菜单数据，但localStorage中有，从localStorage恢复
    if (!store.state.menuList || store.state.menuList.length === 0) {
      if (menuList.length > 0) {
        store.updateMenuList(menuList);
      }
    }
    
    // 检查是否已经添加了动态路由
    const hasDynamicRoutes = router.getRoutes().some(route => 
      route.path === '/home' || route.path === '/mall' || route.path === '/user'
    );
    
    if (!hasDynamicRoutes) {
      // 动态添加路由
      try {
        store.addMenu(router);
        // 重新执行导航，确保新添加的路由能够被正确匹配
        next({ ...to, replace: true });
      } catch (error) {
        console.error('添加路由失败:', error);
        next('/404');
      }
      return;
    }
  }
  
  // 检查当前路由是否存在，更宽松的判断逻辑
  const isRouteExists = router.hasRoute(to.name) || 
                        router.getRoutes().some(route => route.path === to.path);
  
  if (!isRouteExists && to.path !== '/login' && token) {
    // 对于不存在的路由，记录日志并跳转到404
    console.warn(`路由不存在: ${to.path}`);
    next('/404');
  } else {
    // 正常情况，继续导航
    next();
  }
})

// 处理刷新页面时的路由匹配失败
router.onError(error => {
  if (error.name === 'NavigationDuplicated') {
    // 忽略重复导航错误
    return;
  }
  if (error.message.includes('Failed to resolve component')) {
    console.error('路由组件解析失败，可能是组件路径错误或组件不存在:', error);
    // 路由组件解析失败，清除token并重定向到登录页
    const store = useAllStore();
    store.state.token = '';
    store.updateMenuList([]);
    localStorage.removeItem('token');
    localStorage.removeItem('menuList');
    router.push('/login');
  }
})

export default router