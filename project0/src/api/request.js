import axios from 'axios';
import { ElMessage } from "element-plus";
import config from "@/config/index.js";

const service = axios.create({
  baseURL: config.baseApi,
});
const NETWORK_ERROR = "网络错误，请稍后重试";

// 添加请求拦截器
service.interceptors.request.use(function (config) {
    // 在发送请求之前做些什么
    return config;
  }, function (error) {
    // 对请求错误做些什么
    return Promise.reject(error);
  });

// 添加响应拦截器
service.interceptors.response.use(function (response) {
    // 确保response.data存在
    if (!response.data) {
      ElMessage.error(NETWORK_ERROR);
      return Promise.reject(NETWORK_ERROR);
    }
    
    const {code, data, msg} = response.data;
    if(code === 200){
        return data;
    }else{
        ElMessage.error(msg || NETWORK_ERROR);
        return Promise.reject(msg || NETWORK_ERROR); 
    }
  }, function (error) {
    ElMessage.error(NETWORK_ERROR);
    return Promise.reject(error);
  });

function request(options) {
    options.method = options.method || "get";
    // 关于参数的调整
    if(options.method.toLowerCase() === "get"){
      // 如果已经有params，就不要用data覆盖它
      if (!options.params && options.data) {
        options.params = options.data;
      }
      // GET请求不需要data参数
      options.data = undefined;
    } else if(options.method.toLowerCase() === "delete"){
      // DELETE请求特殊处理，将参数放在params中，因为有些后端只接受URL参数
      options.params = options.data;
    } else {
      // 其他请求方法使用data参数
      options.params = undefined;
    }
    
    // 检查是否使用mock
    const isMock = typeof options.mock !== 'undefined' ? options.mock : config.mock;
    
    // 检查是否使用后端API
    const useBackend = typeof options.useBackend !== 'undefined' ? options.useBackend : config.useBackend;
    
    // 确保使用已配置了拦截器的service实例
    // 设置withCredentials以解决跨域问题
    service.defaults.withCredentials = true;
    
    // 根据配置设置baseURL
    if (useBackend) {
      service.defaults.baseURL = config.backendApi;
      // 确保URL以/api开头
      if (!options.url.startsWith('/api')) {
        options.url = '/api' + (options.url.startsWith('/') ? '' : '/') + options.url;
      }
    } else if (isMock) {
      // 对于本地mock，确保URL格式正确
      if (!options.url.startsWith('/')) {
        options.url = '/' + options.url;
      }
      service.defaults.baseURL = '';
    } else {
      service.defaults.baseURL = config.baseApi;
    }
    
    // 使用带拦截器的service实例发送请求
    return service(options);
}

export default request;