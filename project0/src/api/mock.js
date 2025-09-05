import Mock from 'mockjs';
import homeApi from './mockData/home';
import userApi from './mockData/user';
import permissionApi from './mockData/permission';
import config from '../config/index.js';

// 只有在mock为true且不使用后端API时才启用mock拦截
if (config.mock && !config.useBackend) {
  Mock.mock('/api/home/getTableData', 'get', homeApi.getTableData);
  Mock.mock('/api/home/getCountData', 'get', homeApi.getCountData);
  Mock.mock('/api/home/getChartData', 'get', homeApi.getChartData);
  Mock.mock(/\/api\/user\/getUserData/, 'get', userApi.getUserList);
  Mock.mock(/\/api\/user\/deleteUser/, 'delete', (options) => {
    const params = options.data || {};
    const mockConfig = {
      url: options.url + (params.id ? `?id=${params.id}` : '')
    };
    return userApi.deleteUser(mockConfig);
  });
  Mock.mock('/api/user/addUser', 'post', userApi.createUser);
  Mock.mock('/api/user/editUser', 'put', userApi.editUser);
  Mock.mock('/api/permission/getMenu', 'post', permissionApi.getMenu);
}
