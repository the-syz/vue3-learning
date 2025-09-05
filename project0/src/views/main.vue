<script setup>
import CommonAside from '@/components/commonAside.vue'
import CommonHeader from '@/components/commonHeader.vue'
import CommonTab from '@/components/commonTab.vue'
</script>

<template>
  <div class="common-layout">
    <el-container class="lay-container">
      <!--左侧自定义组件-->
      <common-aside />
      <el-container>
        <el-header class ="el-header">
          <common-header />
        </el-header>
        <el-main class="main-right">
          <common-tab />
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<style scoped lang = "less">
  .common-layout,.lay-container {
    height: 100%;
  }
  .el-header{
    background-color: #333;
  }
</style>