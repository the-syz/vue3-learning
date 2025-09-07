export default {
  getTableData: () => {
    return {
      code: 200,
      data: {
        tableData: [
          {
            name: "oppo",
            todayBuy: 500,
            monthBuy: 3500,
            totalBuy: 22000
          },
          {
            name: "vivo",
            todayBuy: 300,
            monthBuy: 2200,
            totalBuy: 24000
          },
          {
            name: "苹果",
            todayBuy: 800,
            monthBuy: 4500,
            totalBuy: 65000
          },
          {
            name: "小米",
            todayBuy: 1200,
            monthBuy: 6500,
            totalBuy: 45000
          },
          {
            name: "三星",
            todayBuy: 300,
            monthBuy: 2000,
            totalBuy: 34000
          },
          {
            name: "魅族",
            todayBuy: 350,
            monthBuy: 3000,
            totalBuy: 22000
          }
        ]
      }
    };
  },
  // 支付订单数据表格
  getPaymentData: () => {
    return {
      code: 200,
      data: [
        {
          name: "今日支付订单",
          value: 1234,
          icon: "SuccessFilled",
          color: "#2ec7c9",
        },
        {
          name: "本月支付订单",
          value: 1234,
          icon: "SuccessFilled",
          color: "#2ec7c9",
        },
      ],
    };
  },
  
  // 收藏订单数据表格
  getCollectionData: () => {
    return {
      code: 200,
      data: [
        {
          name: "今日收藏订单",
          value: 210,
          icon: "StarFilled",
          color: "#ffb980",
        },
        {
          name: "本月收藏订单",
          value: 210,
          icon: "StarFilled",
          color: "#ffb980",
        },
      ],
    };
  },
  
  // 未支付订单数据表格
  getUnpaidData: () => {
    return {
      code: 200,
      data: [
        {
          name: "今日未支付订单",
          value: 1234,
          icon: "GoodsFilled",
          color: "#5ab1ef",
        },
        {
          name: "本月未支付订单",
          value: 1234,
          icon: "GoodsFilled",
          color: "#5ab1ef",
        },
      ],
    };
  },
  
  // 保留原有的getCountData用于向后兼容
  getCountData: () => {
    // 从三个独立表格获取数据并整合
    const paymentData = this.getPaymentData().data;
    const collectionData = this.getCollectionData().data;
    const unpaidData = this.getUnpaidData().data;
    
    return {
      code: 200,
      data: [
        ...paymentData,
        ...collectionData,
        ...unpaidData
      ],
    };
  },
   getChartData: () => {
    // 从三个独立表格获取数据
    const paymentData = this.getPaymentData().data;
    const collectionData = this.getCollectionData().data;
    const unpaidData = this.getUnpaidData().data;
    
    // 整合这三个表格的数据
    const countData = [
      ...paymentData,
      ...collectionData,
      ...unpaidData
    ];
    
    return {
      code: 200,
      data: {
        // 添加整合后的countData到返回结果中
        countData: countData,
        
        orderData: {
          date: [
            "2019-10-01",
            "2019-10-02",
            "2019-10-03",
            "2019-10-04",
            "2019-10-05",
            "2019-10-06",
            "2019-10-07",
          ],
          data: [
            {
              苹果: 3839,
              小米: 1423,
              华为: 4965,
              oppo: 3334,
              vivo: 2820,
              一加: 4751,
            },
            {
              苹果: 3560,
              小米: 2099,
              华为: 3192,
              oppo: 4210,
              vivo: 1283,
              一加: 1613,
            },
            {
              苹果: 1864,
              小米: 4598,
              华为: 4202,
              oppo: 4377,
              vivo: 4123,
              一加: 4750,
            },
            {
              苹果: 2634,
              小米: 1458,
              华为: 4155,
              oppo: 2847,
              vivo: 2551,
              一加: 1733,
            },
            {
              苹果: 3622,
              小米: 3990,
              华为: 2860,
              oppo: 3870,
              vivo: 1852,
              一加: 1712,
            },
            {
              苹果: 2004,
              小米: 1864,
              华为: 1395,
              oppo: 1315,
              vivo: 4051,
              一加: 2293,
            },
            {
              苹果: 3797,
              小米: 3936,
              华为: 3642,
              oppo: 4408,
              vivo: 3374,
              一加: 3874,
            },
          ],
        },
        videoData: [
          { name: "小米", value: 2999 },
          { name: "苹果", value: 5999 },
          { name: "vivo", value: 1500 },
          { name: "oppo", value: 1999 },
          { name: "魅族", value: 2200 },
          { name: "三星", value: 4500 },
        ],
        userData: [
          { date: "周一", new: 5, active: 200 },
          { date: "周二", new: 10, active: 500 },
          { date: "周三", new: 12, active: 550 },
          { date: "周四", new: 60, active: 800 },
          { date: "周五", new: 65, active: 550 },
          { date: "周六", new: 53, active: 770 },
          { date: "周日", new: 33, active: 170 },
        ],
      },
    };
  },
};
