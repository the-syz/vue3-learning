<template>
  <el-aside :width="width"> 
  <el-menu
    background-color="#545c64"
    text-color="#fff"
    :collapse="isCollapse"
    :collapse-transition="false"
    :default-active="activeMenu"
  >
    <h3 v-show="!isCollapse">通用后台管理</h3>
    <h3 v-show="isCollapse">后台</h3>
    <el-menu-item
      v-for="item in noChildren"
      :index="item.path"
      :key="item.path"
      @click="handleMenu(item)"
    >
      <component class="icons" :is="item.icon"></component>
      <span>{{item.label}}</span>
    </el-menu-item>
    <el-sub-menu
      v-for="item in hasChildren"
      :index="item.path"
      :key="item.path"
    >
      <template #title>
        <component class="icons" :is="item.icon"></component>
        <span>{{item.label}}</span>
      </template>
      <el-menu-item-group>
        <el-menu-item
          v-for="(subItem, subIndex) in item.children"
          :index="subItem.path"
          :key="subItem.path"
          @click="handleMenu(subItem)"
        >
          <component class="icons" :is="subItem.icon"></component>
          <span>{{subItem.label}}</span>
        </el-menu-item>
      </el-menu-item-group>
    </el-sub-menu>
  </el-menu>
  </el-aside>
</template>

<script setup>
import { ref, computed } from 'vue'
import {useAllStore} from '@/stores'
import { useRoute, useRouter } from 'vue-router'
const Store = useAllStore()
// 使用store中的menuList或默认列表
const menuList = computed(() => {
  // 优先使用store中的menuList，如果为空则使用默认列表
  if (Store.state.menuList && Store.state.menuList.length > 0) {
    return Store.state.menuList
  }
  return [
    {
      path: '/home',
      name: 'home',
      label: '首页',
      icon: 'House',
      url: 'Home'
    },
    {
      path: '/mall',
      name: 'mall',
      label: '商品管理',
      icon: 'VideoPlay',
      url: 'Mall'
    },
    {
      path: '/user',
      name: 'user',
      label: '用户管理',
      icon: 'User',
      url: 'User'
    },
    {
      path: 'other',
      label: '其他',
      icon: 'Location',
      children: [
        {
          path: '/page1',
          name: 'page1',
          label: '页面1',
          icon: 'Setting',
          url: 'Page1'
        },
        {
          path: '/page2',
          name: 'page2',
          label: '页面2',
          icon: 'Setting',
          url: 'Page2'
        }
      ]
    }
  ]
})

const noChildren = computed(() => menuList.value.filter(item => !item.children))
const hasChildren = computed(() => menuList.value.filter(item => item.children))
const isCollapse = computed(()=>Store.state.isCollapse)
const width = computed(()=>Store.state.isCollapse ? '60px' : '180px')

const router = useRouter()
const route = useRoute()

const handleMenu = (item) => { 
    router.push(item.path)
    Store.selectMenu(item)
}
const activeMenu = computed(()=>route.path)
</script>

<style scoped lang="less">
.el-aside {
  height: 100%;
  background-color: #545c64;
}

.el-menu {
  border-right: none;
  background-color: #545c64;
  height: 100%;
  min-height: 100vh;
  
  h3 {
    line-height: 40px;
    text-align: center;
    color: #ffffff;
    font-size: 14px;
    margin: 0;
    padding: 0;
  }
  
  .el-menu-item, .el-sub-menu {
    font-size: 13px;
    height: 36px;
    line-height: 36px;
  }
  
  .el-menu-item {
    span {
      font-size: 13px;
    }
  }
  
  .el-sub-menu {
    .el-sub-menu__title {
      height: 36px;
      line-height: 36px;
      
      span {
        font-size: 13px;
      }
    }
  }
}

.icons {
  width: 14px;
  height: 14px;
  margin-right: 5px;
}
</style>
