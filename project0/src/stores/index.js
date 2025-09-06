import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue'

function initState() {
  return {
    isCollapse: false,
    tags: [
      {
        path: '/home',
        name: 'home',
        label: '首页',
        icon: 'home'
      }
    ],
    currentMenu: null,
    menuList: [],
    token:"",
    routerList:[]
  }
}

export const useAllStore = defineStore('allData', () => {
  const state = ref(initState())
  
  // 使用watch监听state的变化，进行持久化存储
  watch(state, (newObj) => {
    // 持久化存储state，包括tags数据，无论token是否存在
    // 这样即使退出登录，页面刷新时tags数据也不会丢失
    localStorage.setItem('store', JSON.stringify(newObj))
    // 如果有token，也单独存储token和menuList，保持兼容性
    if (newObj.token) {
      localStorage.setItem('token', newObj.token)
      localStorage.setItem('menuList', JSON.stringify(newObj.menuList))
    }
  }, { deep: true }) // deep开启深度监听

  function selectMenu(val) {
    if (val.name === 'home') {
      state.value.currentMenu = null
    } else {
      let index = state.value.tags.findIndex(item => item.name === val.name)
      index === -1 ? state.value.tags.push(val) : ""
    }
  }
  function updateTags(tag){
    let index = state.value.tags.findIndex(item => item.name === tag.name)
    state.value.tags.splice(index, 1)
  }
  
  // 添加一个函数来切换折叠状态
  const toggleCollapse = () => {
    state.value.isCollapse = !state.value.isCollapse
  }
  function updateMenuList(val) {
    state.value.menuList = val
  }
  function addMenu(router, type){
  // 确保routerList始终是一个数组
  if (!state.value.routerList) {
    state.value.routerList = []
  }
  
  // 如果是刷新的时候执行的，则从localStorage中读取数据
  if(type === 'refresh'){
    // 优先从完整的store中读取数据，确保tags数据正确恢复
    if(localStorage.getItem('store')){
      try {
        const storedState = JSON.parse(localStorage.getItem('store'))
        // 确保storedState是一个对象
        if (typeof storedState === 'object' && storedState !== null) {
          // 深度合并，避免覆盖默认值
          Object.assign(state.value, storedState)
          // 单独处理routerList，因为它保存的是函数，存储时不能正确解析
          state.value.routerList = []
        }
      } catch (error) {
        console.error('解析localStorage中的store失败:', error);
        // 尝试恢复单个数据项
        try {
          const savedToken = localStorage.getItem('token');
          const savedMenuList = localStorage.getItem('menuList');
          
          if(savedToken) {
            state.value.token = savedToken;
          }
          if(savedMenuList) {
            const menuList = JSON.parse(savedMenuList);
            updateMenuList(menuList);
          }
        } catch (innerError) {
          console.error('解析localStorage中的单个数据失败:', innerError);
          localStorage.removeItem('store');
        }
      }
    }
  }
  
  // 确保menuList是有效的
  const menu = state.value.menuList
  if (!menu || !Array.isArray(menu) || menu.length === 0) {
    console.warn('菜单列表为空或无效，无法添加路由');
    return
  }
  
  const module = import.meta.glob('../views/**/*.vue')
  const routeArr =[]
  
  // 清除之前添加的路由
  try {
    state.value.routerList.forEach(item => {
      if (item && typeof item === 'function') {
        item();
      }
    })
  } catch (error) {
    console.error('清除旧路由失败，但继续执行:', error);
  }
  
  // 重置routerList
  state.value.routerList = []
  
  // 处理菜单数据
  menu.forEach(item => {
    if(item.children){
      item.children.forEach(val => {
        // 处理后端返回的url格式，可能包含目录路径
        let componentPath = val.url;
        // 如果url不以.vue结尾，添加.vue后缀
        if (!componentPath.endsWith('.vue')) {
          componentPath = `${componentPath}.vue`;
        }
        // 确保路径以../views/开头
        if (!componentPath.startsWith('../views/')) {
          componentPath = `../views/${componentPath}`;
        }
        
        // 尝试多种可能的路径格式以确保匹配成功
        const urlFormats = [
          componentPath,
          componentPath.toLowerCase(),
          `../views/${val.url}`,
          `../views/${val.url.toLowerCase()}`,
          `../views/${val.name}.vue`,
          `../views/${val.name.charAt(0).toUpperCase() + val.name.slice(1)}.vue`,
          // 特殊处理包含目录路径的URL，提取文件名部分
          `../views/${val.url.split('/').pop()}`,
          `../views/${val.url.split('/').pop().toLowerCase()}`
        ];
        
        // 找到第一个存在的模块路径
        let foundComponent = null;
        for (const url of urlFormats) {
          if (module[url]) {
            foundComponent = module[url];
            break;
          }
        }
        
        // 如果找到了组件，或者尝试使用默认路径
        if (foundComponent) {
          val.component = foundComponent;
        } else {
          console.warn(`未找到组件: ${val.url}，使用默认组件路径`);
          // 作为后备方案，使用动态导入
          val.component = () => {
            // 特殊映射处理：product相关路径应映射到mall.vue
            if (val.url.includes('product')) {
              return import('../views/mall.vue');
            }
            return import(`../views/${val.url}.vue`).catch(err => {
              console.error(`导入组件失败: ${val.url}`, err);
              // 尝试其他可能的路径
              return import(`../views/${val.name}.vue`).catch(err2 => {
                console.error(`导入组件失败: ${val.name}`, err2);
                // 导入失败时返回404组件
                return import('../views/404.vue');
              });
            });
          };
        }
        
        // 正确添加单个子路由
        routeArr.push(val)
      })
    }else{
      // 处理后端返回的url格式，可能包含目录路径
      let componentPath = item.url;
      // 如果url不以.vue结尾，添加.vue后缀
      if (!componentPath.endsWith('.vue')) {
        componentPath = `${componentPath}.vue`;
      }
      // 确保路径以../views/开头
      if (!componentPath.startsWith('../views/')) {
        componentPath = `../views/${componentPath}`;
      }
      
      // 尝试多种可能的路径格式以确保匹配成功
      const urlFormats = [
        componentPath,
        componentPath.toLowerCase(),
        `../views/${item.url}`,
        `../views/${item.url.toLowerCase()}`,
        `../views/${item.name}.vue`,
        `../views/${item.name.charAt(0).toUpperCase() + item.name.slice(1)}.vue`,
        // 特殊处理包含目录路径的URL，提取文件名部分
        `../views/${item.url.split('/').pop()}`,
        `../views/${item.url.split('/').pop().toLowerCase()}`
      ];
      
      // 找到第一个存在的模块路径
      let foundComponent = null;
      for (const url of urlFormats) {
        if (module[url]) {
          foundComponent = module[url];
          break;
        }
      }
      
      // 如果找到了组件，或者尝试使用默认路径
      if (foundComponent) {
        item.component = foundComponent;
      } else {
        console.warn(`未找到组件: ${item.url}，使用默认组件路径`);
        // 作为后备方案，使用动态导入
          item.component = () => {
            // 特殊映射处理：product相关路径应映射到mall.vue
            if (item.url.includes('product')) {
              return import('../views/mall.vue');
            }
            return import(`../views/${item.url}.vue`).catch(err => {
              console.error(`导入组件失败: ${item.url}`, err);
              // 尝试其他可能的路径
              return import(`../views/${item.name}.vue`).catch(err2 => {
                console.error(`导入组件失败: ${item.name}`, err2);
                // 导入失败时返回404组件
                return import('../views/404.vue');
              });
            });
          };
      }
      
      routeArr.push(item)
    }
  })

  // 添加路由记录
  routeArr.forEach(item => {
    // 确保name、path和component存在
    if (item.name && item.path && item.component) {
      try {
        // 检查路由是否已存在
        const existingRoute = router.getRoutes().find(route => route.path === item.path);
        if (existingRoute) {
          router.removeRoute(existingRoute.name);
        }
        
        const routeRecord = router.addRoute('main', item)
        state.value.routerList.push(routeRecord)
      } catch (error) {
        console.error(`添加路由 ${item.path} 失败:`, error);
      }
    }
  })
  }

  // 定义重置方法
  function clearn(){
    // 确保routerList是一个数组
    if (!state.value.routerList || !Array.isArray(state.value.routerList)) {
      state.value.routerList = []
    }
    
    // 把保存的删除路由方法都执行一遍
    state.value.routerList.forEach(item => {
      try {
        if(item && typeof item === 'function') {
          item()
        }
      } catch (error) {
        console.error('删除路由失败:', error)
      }
    })
    
    // 重置state的数据
    state.value = initState()
    
    // 删除本地缓存，因为这个clearn方法是用户退出执行的
    localStorage.removeItem('store')
    localStorage.removeItem('token')
    localStorage.removeItem('menuList')
  }
  
  return { 
    state, 
    toggleCollapse, 
    selectMenu,
    updateTags,
    updateMenuList,
    addMenu,
    clearn
  }  
})