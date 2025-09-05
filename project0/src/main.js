import { createApp } from 'vue'
import App from './App.vue'
import "@/assets/less/index.less"
import router from './router'
//完整导入 element-plus
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import { createPinia } from 'pinia'
import "@/api/mock.js"
import api from "@/api/api.js"
import { useAllStore } from '@/stores/index.js'

const pinia = createPinia()
const app = createApp(App)
app.use(ElementPlus)

app.config.globalProperties.$api = api

// 初始化pinia
app.use(pinia)

// 这个动态路由的方法必须要在use(pinia)之后使用，因为这样才可以获取到pinia对象
// 必须在use(router)之前使用，因为如果是刷新，use(router)后执行完会直接跳转路由，所以需要在他之前执行动态路由方法
const store = useAllStore()

// 尝试从localStorage恢复路由和登录状态（如果有）
// 这将解决刷新页面需要重新登录的问题
store.addMenu(router, "refresh")

// 路由守卫已在router/index.js中定义，避免重复定义导致的冲突
// 保留isRoute函数用于其他地方可能的调用
function isRoute(to) {
  return router.getRoutes().filter(item => item.path === to.path).length > 0
}

app.use(router)
app.mount('#app')

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}