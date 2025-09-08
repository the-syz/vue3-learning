<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue';
import * as echarts from 'echarts';
import { ElMessage } from 'element-plus';
import api from '../api/api';

// 品牌列表
const brands = ['苹果', '小米', '华为', 'oppo', 'vivo', '一加'];

// 实时价格数据
const realTimePrices = ref({});

// 历史价格数据
const priceHistories = ref({});

// echarts实例
const chartInstances = ref({});

// 数据更新定时器
let updateTimer = null;

// 初始化图表
const initCharts = async () => {
  await nextTick();
  
  brands.forEach(brand => {
    const chartDom = document.getElementById(`chart-${brand}`);
    if (chartDom) {
      chartInstances.value[brand] = echarts.init(chartDom);
      // 设置图表配置
      setChartOption(brand);
    }
  });
};

// 设置图表配置
const setChartOption = (brand) => {
  const chartInstance = chartInstances.value[brand];
  if (!chartInstance) return;
  
  const history = priceHistories.value[brand] || [];
  const times = history.map(item => item.time);
  const values = history.map(item => item.value);
  
  // 计算价格范围，确保最低价格不碰到横轴
  let minValue = Infinity;
  let maxValue = -Infinity;
  values.forEach(value => {
    if (value < minValue) minValue = value;
    if (value > maxValue) maxValue = value;
  });
  
  // 设置合理的范围，添加10%的边距
  const range = maxValue - minValue;
  const padding = range * 0.1;
  const yMin = minValue - padding;
  const yMax = maxValue + padding;
  
  const option = {
    grid: {
      left: '3%',
      right: '3%', // 让图表占满整个容器
      top: '10%',
      bottom: '15%',
      containLabel: true
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        show: false // 隐藏鼠标悬停的虚线
      },
      formatter: function(params) {
        const date = new Date(params[0].axisValue);
        const timeStr = `${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}:${date.getSeconds().toString().padStart(2, '0')}`;
        return `
          <div>时间: ${timeStr}</div>
          <div>${brand}价格: ${Math.round(params[0].value)}元</div>
        `;
      },
      showContent: true,
      alwaysShowContent: false,
      triggerOn: 'mousemove',
      hideDelay: 100
    },
    xAxis: {
      type: 'category',
      data: times,
      axisLabel: {
        rotate: 45,
        formatter: function(value) {
          const date = new Date(value);
          // 显示秒级时间，与后端数据更新频率匹配
          return `${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}:${date.getSeconds().toString().padStart(2, '0')}`;
        }
      },
      boundaryGap: false // 确保数据点不会在曲线上滑动
    },
    yAxis: {
      type: 'value',
      name: '价格 (元)', // 添加纵轴名称
      nameLocation: 'middle',
      nameGap: 60, // 增加间距避免标题被遮挡
      min: yMin > 0 ? yMin : 0, // 确保最小值不小于0
      max: yMax,
      axisLabel: {
        formatter: function(value) {
          return Math.round(value) + ' 元';
        }
      },
      splitLine: {
        show: true
      }
    },
    series: [
      {
        name: brand,
        type: 'line',
        data: values,
        smooth: true,
        lineStyle: {
          width: 2,
          color: getBrandColor(brand)
        },
        itemStyle: {
          color: getBrandColor(brand)
        },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [
              {
                offset: 0,
                color: `${getBrandColor(brand)}80` // 80表示透明度
              },
              {
                offset: 1,
                color: `${getBrandColor(brand)}10` // 10表示透明度
              }
            ]
          }
        },
        markPoint: {
          data: [],
          symbolSize: 60,
          label: {
            formatter: function(params) {
              return `${Math.round(params.value)}元`;
            },
            show: false
          }
        },
        emphasis: {
          focus: 'series',
          itemStyle: {
            borderWidth: 3,
            borderColor: '#fff'
          },
          label: {
            show: true,
            position: 'top',
            formatter: function(params) {
              return `${Math.round(params.value)}元`;
            },
            backgroundColor: getBrandColor(brand),
            color: '#fff',
            padding: [5, 10],
            borderRadius: 4
          }
        }
      }
    ]
  };
  
  chartInstance.setOption(option);
};

// 获取品牌对应的颜色
const getBrandColor = (brand) => {
  const colorMap = {
    '苹果': '#FF6384',
    '小米': '#36A2EB',
    '华为': '#FFCE56',
    'oppo': '#4BC0C0',
    'vivo': '#9966FF',
    '一加': '#FF9F40'
  };
  return colorMap[brand] || '#333333';
};

// 获取历史价格数据
const fetchPriceHistories = async () => {
  for (const brand of brands) {
    try {
      const data = await api.getPriceHistory({ name: brand, limit: 100 });
      priceHistories.value[brand] = data.history;
      setChartOption(brand);
    } catch (error) {
      ElMessage.error(`获取${brand}历史数据失败`);
      console.error(`获取${brand}历史数据失败:`, error);
    }
  }
};

// 获取实时价格数据
const fetchRealTimePrices = async () => {
  try {
    const prices = await api.getRealTimePrice();
    
    // 更新实时价格数据
    prices.forEach(item => {
      realTimePrices.value[item.name] = item;
      
      // 将新数据添加到历史数据中
      if (!priceHistories.value[item.name]) {
        priceHistories.value[item.name] = [];
      }
      
      // 检查是否已经存在相同时间点的数据
      const exists = priceHistories.value[item.name].some(historyItem => 
        historyItem.time === item.time
      );
      
      if (!exists) {
        // 只保留最新的100条数据
        if (priceHistories.value[item.name].length >= 100) {
          priceHistories.value[item.name].shift();
        }
        
        priceHistories.value[item.name].push({
          time: item.time,
          value: item.value
        });
        
        // 更新图表
        setChartOption(item.name);
      }
    });
  } catch (error) {
    ElMessage.error('获取实时价格数据失败');
    console.error('获取实时价格数据失败:', error);
  }
};

// 启动定时更新
const startAutoUpdate = () => {
  // 先立即获取一次数据
  fetchRealTimePrices();
  
  // 然后每3秒更新一次
  updateTimer = setInterval(fetchRealTimePrices, 3000);
};

// 停止定时更新
const stopAutoUpdate = () => {
  if (updateTimer) {
    clearInterval(updateTimer);
    updateTimer = null;
  }
};

// 监听窗口大小变化，调整图表尺寸
const handleResize = () => {
  brands.forEach(brand => {
    const chartInstance = chartInstances.value[brand];
    if (chartInstance) {
      chartInstance.resize();
    }
  });
};

// 组件挂载时初始化
onMounted(async () => {
  // 初始化图表
  await initCharts();
  
  // 获取历史数据
  await fetchPriceHistories();
  
  // 启动自动更新
  startAutoUpdate();
  
  // 监听窗口大小变化
  window.addEventListener('resize', handleResize);
});

// 组件卸载时清理
onUnmounted(() => {
  // 停止自动更新
  stopAutoUpdate();
  
  // 移除窗口大小变化监听
  window.removeEventListener('resize', handleResize);
  
  // 销毁图表实例
  brands.forEach(brand => {
    const chartInstance = chartInstances.value[brand];
    if (chartInstance) {
      chartInstance.dispose();
    }
  });
});
</script>

<template>
  <div class="mall-container">
    <div class="page-header">
      <h1>实时价格浮动监控</h1>
      <p>监控苹果、小米、华为、oppo、vivo、一加六大品牌的实时价格变化</p>
    </div>
    
    <div class="charts-wrapper">
      <div v-for="brand in brands" :key="brand" class="chart-container">
        <div class="chart-header">
          <h3>{{ brand }}</h3>
          <div class="real-time-info" v-if="realTimePrices[brand]">
            <span class="price" :style="{ color: getBrandColor(brand) }">
              ¥{{ Math.round(realTimePrices[brand].value) || '0' }}
            </span>
            <span class="update-time">
              {{ formatUpdateTime(realTimePrices[brand].time) }}
            </span>
          </div>
        </div>
        <div :id="`chart-${brand}`" class="chart-content"></div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="less">
.mall-container {
  padding: 20px;
  height: 100vh;
  background-color: #f5f7fa;
  overflow-y: auto;
}

.page-header {
  margin-bottom: 30px;
  text-align: center;
  
  h1 {
    font-size: 28px;
    color: #333;
    margin-bottom: 10px;
  }
  
  p {
    font-size: 16px;
    color: #666;
  }
}

.charts-wrapper {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(600px, 1fr));
  gap: 20px;
}

.chart-container {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  
  h3 {
    font-size: 18px;
    color: #333;
    margin: 0;
  }
  
  .real-time-info {
    display: flex;
    align-items: center;
    gap: 10px;
    
    .price {
      font-size: 18px;
      font-weight: bold;
    }
    
    .update-time {
      font-size: 12px;
      color: #999;
    }
  }
}

.chart-content {
  width: 100%;
  height: 300px;
}

// 格式化更新时间
.format-update-time {
  font-size: 12px;
  color: #999;
}
</style>

<script>
export default {
  methods: {
    // 格式化更新时间
    formatUpdateTime(timeStr) {
      if (!timeStr) return '';
      const date = new Date(timeStr);
      return `${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}:${date.getSeconds().toString().padStart(2, '0')}`;
    },
    
    // 获取品牌颜色（用于模板中）
    getBrandColor(brand) {
      const colorMap = {
        '苹果': '#FF6384',
        '小米': '#36A2EB',
        '华为': '#FFCE56',
        'oppo': '#4BC0C0',
        'vivo': '#9966FF',
        '一加': '#FF9F40'
      };
      return colorMap[brand] || '#333333';
    }
  }
};
</script>