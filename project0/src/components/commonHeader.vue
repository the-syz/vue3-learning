<template>
  <div class="header">
    <div class="l-content">
      <el-button size="small" @click="handleCollapse">
        <component class="icons" is="menu"></component>
      </el-button>
      <el-breadcrumb separator="/" class="bread">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <div class="r-content">
      <el-dropdown>
        <span class="el-dropdown-link">
           <img :src="getImgUrl('user')"class="user"/>
        </span>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item>个人中心</el-dropdown-item>
            <el-dropdown-item @click="handleLogout">退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </div>
</template>

<script setup>
import {ref, computed} from 'vue'
import {useAllStore} from '@/stores'
import {useRouter} from 'vue-router'
const router = useRouter()
const getImgUrl = (user) => {
  // 修复拼写错误并统一路径格式
  return new URL(`../assets/images/${user}.png`, import.meta.url).href
} 
const store = useAllStore()
const handleCollapse = () => {
  // 调用store中的toggleCollapse函数来切换折叠状态
  store.toggleCollapse()
}

// 退出登录函数
const handleLogout = () => {
  
  // 执行重置方法，清除所有状态
  store.clearn()
  
  // 跳转到登录页
  router.push('/login')
}
</script>

<style scoped lang="less">
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  height: 100%;
  background-color: #333;
}
.icons {
  width: 20px;
  height: 20px;
}
.l-content {
  display: flex;
  align-items: center;
  .el-button {
    margin-right: 20px;
  }
}
.r-content {
  .user {
  width: 30px;
  height: 30px;
  border-radius: 50%;
}}
:deep(.bread) {
  color: #fff!important;
  cursor: pointer!important;
}
</style>
