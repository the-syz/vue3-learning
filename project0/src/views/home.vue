<script setup>
import { ref, getCurrentInstance, onMounted, onUnmounted, reactive, nextTick } from 'vue'
import * as echarts from 'echarts'

const { proxy } = getCurrentInstance()

function getImageUrl(user) { 
  return new URL(`../assets/images/${user}.png`, import.meta.url).href
}
const tableData = ref([]) 
const countData = ref([])
const echartsRef = ref(null) // 创建专门的 ref 引用图表 DOM 元素
const userEchartRef = ref(null) // 用户图表引用
const videoEchartRef = ref(null) // 视频图表引用

const tableLabel = ref({
    name: "课程",
    todayBuy: "今日购买",
    monthBuy: "本月购买",
    totalBuy: "总购买",
})

// 柱状图配置
const xOptions = reactive({
      // 图例文字颜色
      textStyle: {
        color: "#333",
      },
      legend: {},
      grid: {
        left: "20%",
      },
      // 提示框
      tooltip: {
        trigger: "axis",
      },
      xAxis: {
        type: "category", // 类目轴
        data: [],
        axisLine: {
          lineStyle: {
            color: "#17b3a3",
          },
        },
        axisLabel: {
          interval: 0,
          color: "#333",
        },
      },
      yAxis: [
        {
          type: "value",
          axisLine: {
            lineStyle: {
              color: "#17b3a3",
            },
          },
        },
      ],
      color: ["#2ec7c9", "#b6a2de", "#5ab1ef", "#ffb980", "#d87a80", "#8d98b3"],
      series: [],
})
// 饼图配置
const pieOptions = reactive({
  tooltip: {
    trigger: "item",
  },
  legend: {},
  color: [
    "#0f78f4",
    "#dd536b",
    "#9462e5",
    "#a6a6a6",
    "#e1bb22",
    "#39c362",
    "#3ed1cf",
  ],
  series: []
})

const getTableData = async ()=>{
  try {
    const data = await proxy.$api.getTableData()
    tableData.value = data.tableData
  } catch (error) {
    console.error('获取表格数据失败:', error)
  }
}
const getCountData = async ()=>{
  try {
    const data = await proxy.$api.getCountData()
    console.log('获取到的数据:', data)
    // 修复数据格式问题：mockData返回的是整个数组，不需要再访问countData属性
    countData.value = data
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
}
const getChartData = async ()=>{
    try {
      const {orderData,userData,videoData,countData: chartCountData} = await proxy.$api.getChartData()
      //确保DOM渲染完成后再初始化图表
      await nextTick()
      
      // 使用从getChartData中获取的countData
      if (chartCountData) {
        countData.value = chartCountData;
      }
    
    // 第一个图表 - 订单数据折线图
    if (echartsRef.value) {
      // 设置第一个图表数据
      const orderChartOptions = {
        ...xOptions,
        xAxis: {
          ...xOptions.xAxis,
          data: orderData.date
        },
        series: Object.keys(orderData.data[0]).map(val => ({
          name: val,
          type: 'line',
          data: orderData.data.map(item => item[val])
        }))
      }
      
      const oneEchart = echarts.init(echartsRef.value)
      oneEchart.setOption(orderChartOptions)
      
      // 添加窗口大小改变时重绘图表
      const handleResize = () => {
        oneEchart.resize()
      }
      
      window.addEventListener('resize', handleResize)
      
      // 在组件卸载时清理事件监听器
      onUnmounted(() => {
        window.removeEventListener('resize', handleResize)
        oneEchart.dispose()
      })
    }
    
    // 第二个图表 - 用户数据柱状图
    if (userEchartRef.value) {
      // 设置第二个图表数据
      const userChartOptions = {
        ...xOptions,
        xAxis: {
          ...xOptions.xAxis,
          data: userData.map(item => item.date)
        },
        series: [
          {
            name: '新增用户',
            type: 'bar',
            data: userData.map(item => item.new)
          },
          {
            name: '活跃用户',
            type: 'bar',
            data: userData.map(item => item.active)
          }
        ]
      }
      
      const userEchart = echarts.init(userEchartRef.value)
      userEchart.setOption(userChartOptions)
      
      // 添加窗口大小改变时重绘图表
      const handleUserResize = () => {
        userEchart.resize()
      }
      
      window.addEventListener('resize', handleUserResize)
      
      // 在组件卸载时清理事件监听器
      onUnmounted(() => {
        window.removeEventListener('resize', handleUserResize)
        userEchart.dispose()
      })
    }
    
    // 第三个图表 - 视频数据饼图
    if (videoEchartRef.value) {
      // 设置饼图数据
      const videoChartOptions = {
        ...pieOptions,
        series: [{
          name: '视频分类',
          type: 'pie',
          radius: '60%',
          data: videoData,
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          }
        }]
      }
      
      const videoEchart = echarts.init(videoEchartRef.value)
      videoEchart.setOption(videoChartOptions)
      
      // 添加窗口大小改变时重绘图表
      const handleVideoResize = () => {
        videoEchart.resize()
      }
      
      window.addEventListener('resize', handleVideoResize)
      
      // 在组件卸载时清理事件监听器
      onUnmounted(() => {
        window.removeEventListener('resize', handleVideoResize)
        videoEchart.dispose()
      })
    }
    
  } catch (error) {
    console.error('获取图表数据失败:', error)
  }
}

onMounted(async ()=>{
  getTableData()
  // 不再单独调用getCountData，而是通过getChartData获取整合后的数据
  // 延迟调用图表初始化，确保DOM已渲染
  setTimeout(() => {
    getChartData()
  }, 100)
})

</script>

<template>
  <div >
    <el-row class="home" :gutter="20">
      <el-col :span="8" style="margin-top: 20px">
        <el-card shadow="hover">
          <div class="user">
            <img :src="getImageUrl('user')" class="user"/>
            <div class="user-info">
              <p class="user-info-admin">admin</p>
              <p class="user-info-p">管理员</p>
            </div>
          </div>
          <div class="login-info">
            <p>上次登录时间:<span>2021-09-22 15:32:00</span></p>
            <p>上次登录地点:<span>北京</span></p>
          </div>
        </el-card>
        
        <el-card shadow="hover" class="user-table">
         <el-table :data="tableData">
          <el-table-column 
            v-for="(val, key) in tableLabel"
            :key="key"
            :prop="key"
            :label="val"
            >
            </el-table-column>
         </el-table>
        </el-card>
      
      </el-col>
      <el-col :span="16" style="margin-top: 20px"> 
        <div class="num">
          <el-card 
            :body-style="{display: 'flex', padding:0}"
            v-for="item in countData"
            :key="item.name"
          >
          <component :is="item.icon" class="icon" :style="{background:item.color,color}"></component>
          <div class="detail">
            <p class="num">￥{{item.value}}</p>
            <p class="txt">￥{{item.name}}</p>
          </div>
          </el-card>
        </div>
        <el-card class="top-chart" shadow="hover"> 
          <div ref="echartsRef" style="height: 280px"></div>
        </el-card>
        <div class="graph">
          <el-card shadow="hover"> 
            <div ref="userEchartRef" style="height: 240px"></div>
          </el-card>
          <el-card shadow="hover"> 
            <div ref="videoEchartRef" style="height: 240px"></div>
          </el-card>
        </div>
      </el-col>

    </el-row>
  </div>
</template>

<style scoped lang = "less">
  .home{
    height: 100%;
    overflow: hidden;
    .user{
      display: flex; 
      align-items: center;
      border-bottom: 1px solid #ccc;
      margin-bottom: 20px;
      img{
        width:150px;
        height: 150px;
        border-radius: 50%;
        margin-right: 20px;
      }
      .user-info{
        p{
          line-height: 20px;
          font-size:16px;
        }
        .user-info-p{
          color: #999;
          margin-top: 10px;
        }
        .user-info-admin{
          font-size: 35px;
        }
      }
    }
    .login-info{
        p{
          line-height: 30px;
          font-size:14px;
          color:#999;
          span{
            color: #666;
            margin-left: 10px;
          }
        }
      }
      .user-table{
        margin-top: 20px;
      }
      .num{
        display:flex;
        flex-wrap: wrap;
        justify-content: space-between;
        .el-card{
          width:32%;
          margin-bottom: 20px;
        }
        .icon{
          width: 80px;
          height: 80px;
          font-size: 30px;
          line-height: 80px;
          text-align: center;
          color: #fff;
        }
        .detail{
          margin-left: 15px;
          display: flex;
          flex-direction: column;
          justify-content: center;
          .num{
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 10px;
          }
          .txt{
            font-size: 12px;
            text-align: center;
            color: #999;
          }
        }
      }
      .graph{ 
        margin-top: 20px;
        display: flex;
        justify-content: space-between;
        .el-card{
          width: 48%;
          height: 300px;
        }
      }
}
</style>