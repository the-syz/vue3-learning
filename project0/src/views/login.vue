<script setup>
import { reactive, getCurrentInstance } from 'vue'
import { useRouter } from 'vue-router'
import { useAllStore } from '@/stores'
import { ElMessage } from 'element-plus'
const loginForm = reactive({
  username: '',
  password: ''
})
const {proxy} = getCurrentInstance()
const store = useAllStore()
const router = useRouter()
const handleLogin = async () => { 
  try {
    // 先清除所有可能残留的localStorage数据
    localStorage.removeItem('token');
    localStorage.removeItem('menuList');
    localStorage.removeItem('userInfo');
    
    // 清除路由缓存
    if (store.state.routerList && store.state.routerList.length > 0) {
      store.state.routerList.forEach(item => {
        if (item && typeof item === 'function') {
          try {
            item();
          } catch (error) {
            console.warn('清除路由失败:', error);
          }
        }
      });
      store.state.routerList = [];
    }
    
    // 重置store状态
    store.updateMenuList([]);
    store.state.token = '';
    
    const res = await proxy.$api.getMenu(loginForm)
    console.log('登录请求返回数据:', res)
    
    // 注意：由于request.js的响应拦截器处理，当code===200时，会直接返回response.data.data
    // 所以res已经是response.data.data的数据结构
    if (res && res.menuList && Array.isArray(res.menuList) && res.menuList.length > 0 && res.token) {
      // 更新store状态
      store.updateMenuList(res.menuList);
      store.state.token = res.token;
      
      // 将token、菜单数据和用户信息保存到localStorage，解决刷新页面丢失问题
      localStorage.setItem('token', res.token);
      localStorage.setItem('menuList', JSON.stringify(res.menuList));
      localStorage.setItem('userInfo', JSON.stringify({username: loginForm.username}));
      
      // 动态添加路由
      console.log('开始添加动态路由');
      store.addMenu(router);
      
      // 确保路由已添加后再跳转，增加延迟时间确保路由完全加载
      setTimeout(() => {
        // 检查是否有默认首页路径
        const defaultRoute = res.menuList[0]?.path || '/home';
        console.log('使用默认路由:', defaultRoute);
        
        // 直接跳转，让路由守卫处理路由是否存在的问题
        router.push(defaultRoute);
      }, 100);
    } else {
      console.error('登录响应数据结构不正确或菜单列表为空:', res);
      ElMessage.error('登录失败，无法获取有效菜单数据');
    }
  } catch (error) {
    console.error('登录过程发生错误:', error);
    ElMessage.error('登录失败，请重试');
  }
}
</script>

<template>
  <div class="body-login">
    <el-form :model="loginForm" class="login-container">
      <h1>欢迎登录</h1>
      <el-form-item>
        <el-input type="input" v-model="loginForm.username" placeholder="请输入用户名"></el-input>
      </el-form-item>
      <el-form-item>
        <el-input type="password" v-model="loginForm.password" placeholder="请输入密码"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleLogin">登录</el-button>
      </el-form-item>
    </el-form>

  </div>
</template>

<style scoped lang = "less">
.body-login{
  width: 100%;
  height: 100%;
  background-image: url('../assets/images/background.png');
  background-size: 100% ;
  overflow: hidden;
}
.login-container {
  width: 400px;
  background-color: #fff;
  border:1px solid #eaeaea;
  border-radius: 10px;
  padding: 35px 35px 15px 35px;
  box-shadow: 0 0 25px #cacaca;
  margin:250px auto;
  h1{
    text-align: center;
    margin-bottom: 20px;
    color: #505450;
    font-size: 24px;
    font-weight: bold;
  }
  :deep(.el-form-item__content){
    justify-content: center;
  }
}
</style>