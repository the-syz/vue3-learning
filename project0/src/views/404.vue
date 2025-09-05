<template>
    <div class="exception">
      <img :src="getImageUrl(404)" />
      <div class="button-container">
        <el-button v-if="hasToken" type="primary" @click="reloadRoutes">重新加载路由</el-button>
        <el-button v-if="hasToken" @click="logout">退出登录</el-button>
        <el-button v-else type="success" @click="goLogin">去登录页面</el-button>
        <el-button @click="goBack">返回上一页</el-button>
      </div>
    </div>
</template>
  
<script setup>
import {useRouter} from 'vue-router'
import {useAllStore} from '@/stores/index.js'
import {ref, onMounted} from 'vue'
import { ElMessage } from 'element-plus'

const router = useRouter()
const store = useAllStore()
const hasToken = ref(false)

// 检查是否有token
onMounted(() => {
  checkTokenStatus()
})

const checkTokenStatus = () => {
  hasToken.value = !!store.state.token
}

const getImageUrl = (img) => {
  return new URL(`../assets/images/${img}.png`, import.meta.url).href;
}

// 返回上一页
const goBack = () => {
  if (window.history.length > 1) {
    router.go(-1)
  } else if (hasToken.value) {
    // 如果没有历史记录但有token，尝试去首页
    tryLoadHome()
  } else {
    // 如果没有历史记录且没有token，去登录页
    router.push('/login')
  }
}

// 尝试加载首页
const tryLoadHome = () => {
  const homeRouteExists = router.getRoutes().some(route => route.path === '/home');
  if (homeRouteExists) {
    router.push('/home');
  } else {
    // 尝试创建临时首页路由
    try {
      router.addRoute('main', {
        path: '/home',
        name: 'home',
        component: () => import('@/views/home.vue')
      });
      router.push('/home');
    } catch (error) {
      console.error('创建临时首页路由失败:', error);
      ElMessage.error('无法加载首页，请尝试其他操作');
    }
  }
}

// 重新加载路由
const reloadRoutes = () => {
  try {
    // 尝试从localStorage恢复菜单数据
    const savedMenuList = localStorage.getItem('menuList');
    if (savedMenuList) {
      store.updateMenuList(JSON.parse(savedMenuList));
      // 清除旧路由并添加新路由
      store.addMenu(router);
      
      ElMessage.success('路由重新加载成功，正在跳转到首页');
      
      // 延迟后检查并跳转
      setTimeout(() => {
        tryLoadHome()
      }, 500);
    } else {
      ElMessage.warning('没有找到菜单数据，无法重新加载路由');
    }
  } catch (error) {
    console.error('重新加载路由失败:', error);
    ElMessage.error('重新加载路由失败，请尝试退出登录后重新登录');
  }
}

// 退出登录
const logout = () => {
  try {
    // 清空store和localStorage
    store.clearn()
    // 跳转到登录页
    router.push('/login')
    ElMessage.success('已退出登录');
  } catch (error) {
    console.error('退出登录失败:', error);
    ElMessage.error('退出登录失败，请刷新页面重试');
  }
}

// 去登录页面
const goLogin = () => {
  router.push('/login')
}
</script>

<style lang="less" scoped>
.exception {
  position: relative;
  img {
    width: 100%;
    height: 100vh;
  }
  .button-container {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    display: flex;
    flex-direction: column;
    gap: 12px;
    background-color: rgba(255, 255, 255, 0.9);
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  }
  :deep(.button-container .el-button) {
    margin: 0;
  }
}
</style>