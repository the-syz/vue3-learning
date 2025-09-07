import request from './request';

export default {
    getTableData(){
        return request({
            url: '/home/getTableData', 
            method:'get',
            mock:false,
        })
    },
    getCountData(){
    return request({
        url: '/home/getCountData', 
        method:'get',
        mock:false,
    })
    },
    // 获取支付订单数据表格
    getPaymentData(){
    return request({
        url: '/home/getPaymentData', 
        method:'get',
        mock:false,
    })
    },
    // 获取收藏订单数据表格
    getCollectionData(){
    return request({
        url: '/home/getCollectionData', 
        method:'get',
        mock:false,
    })
    },
    // 获取未支付订单数据表格
    getUnpaidData(){
    return request({
        url: '/home/getUnpaidData', 
        method:'get',
        mock:false,
    })
    },
    getChartData(){
    return request({
        url: '/home/getChartData', 
        method:'get',
        mock:false,
    })
    },
    getUserData(data){
    return request({
        url: '/user/getUserData', 
        method:'get',
        mock:false,
        data:data,
    })
    },
    deleteUser(data){
        return request({
            url: '/user/deleteUser', 
            method:'delete',
            mock:false,
            data:data,
        })
    },
    addUser(data){
        return request({
            url: '/user/addUser', 
            method:'post',
            mock:false,
            data:data,
        })
    },
    editUser(data){
        // 确保id存在于data对象中
        if (!data.id) {
            console.error('编辑用户时缺少id参数');
            return Promise.reject('缺少id参数');
        }
        
        // 创建一个新对象，移除id属性
        const userData = { ...data };
        const userId = userData.id;
        delete userData.id;
        
        return request({
            url: `/user/editUser?id=${userId}`, 
            method:'put',
            mock:false,
            data:userData,
        })
    },
    getMenu(data) {
    return request({
      url: '/permission/getMenu',
      method: 'post',
      data: data,
      mock: false
    })
    },
    getSalespeople() {
    return request({
      url: '/user/getSalespeople',
      method: 'get',
      mock: false
    })
    },
};
