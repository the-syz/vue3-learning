// 环境配置
export const EnvConfig = {
  development: {
    baseApi: '/api',
    mockApi: '/api', // 修改为本地路径，与mock.js中定义的接口路径匹配
    backendApi: 'http://127.0.0.1:8000' // FastAPI后端API地址，不需要添加/api前缀
  },
  test: {
    baseApi: '//test/api',
    mockApi: '/api', // 测试环境也可以使用本地mock
    backendApi: 'http://test-server:8000' // 不需要添加/api前缀
  },
  production: {
    baseApi: 'https://api.example.com',
    mockApi: '', // 生产环境通常不使用mock
    backendApi: 'https://api.example.com' // 生产环境API地址
  }
}

// 定义当前环境
const env = import.meta.env.MODE || "development"; // 使用Vite的环境变量，默认开发环境

// 导出默认配置
export default {
  env,
  ...EnvConfig[env], // 只扩展当前环境的配置
  useBackend: true, // 设置为true，使用后端实际API地址
  mock: false, // 设置为false，关闭mock数据拦截功能
};