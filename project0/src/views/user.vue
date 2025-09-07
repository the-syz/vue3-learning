<script setup>
import { ref, onMounted,getCurrentInstance, reactive,nextTick } from 'vue'
import {ElMessage,ElMessageBox} from 'element-plus'
const handleClick = () => {
  console.log('click')
}

const tableData = ref([])

const config = reactive({
    name: '',
    page: 1,  // 添加分页参数
    limit: 10, // 每页显示条数，与后端API保持一致
})

// 单独存储总条数，不传递给API
const totalCount = ref(0)

const { proxy } = getCurrentInstance()
const getUserData = async() => { 
    // 调用API，直接使用config对象作为参数
    let data = await proxy.$api.getUserData(config)
    
    // 直接使用后端返回的分页和过滤后的数据
    let userList = data.list || []
    console.log('API返回数据:', userList)
    
    // 处理性别显示并赋值
    tableData.value = userList.map(item => ({
        ...item,
        sexLabel: String(item.sex) === '1' ? '男' : '女',
    }))
    
    // 更新总条数
    totalCount.value = data.count
    console.log('配置信息:', config)
    console.log('总条数:', totalCount.value)
}

const tableLabel =reactive([
    {
        prop:'name',
        label:'姓名'
    },
    {
        prop:'age',
        label:'年龄'
    },
    {
        prop:'sexLabel',
        label:'性别'
    },
    {
        prop:'birth',
        label:'出生日期',
        width:200
    },
    {
        prop:'addr',
        label:'地址',
        width:200
    },
    {
        prop:'salesperson_name',
        label:'负责人',
        width:150
    },
])
const formInline = reactive({
    keyWord: '',
})

const handleSearch = () => {
    config.name = formInline.keyWord
    getUserData()
}

const handleChange = (page) => {
    config.page = page
    getUserData()
}

const handleDelete = async (row) => {
    console.log(row)
    ElMessageBox.confirm('是否确认删除').then(async() => {
        await proxy.$api.deleteUser({id:row.id})
        ElMessage({
          showClose: true,
          message: '删除成功',
          type: 'success',
        })
        getUserData()
    })

}
const action = ref('add')
const dialogVisible = ref(false)
const salespeopleList = ref([]) // 存储销售人员列表
const formUser = reactive({
  id: '',
  name: '',
  addr: '',
  age: '',
  birth: '',
  sex: '',
  salesperson_id: '',
})
//表单校验规则
const rules = reactive({
  name: [{ required: true, message: "姓名是必填项", trigger: "blur" }],
  age: [
    { required: true, message: "年龄是必填项", trigger: "blur" },
    { type: "number", message: "年龄必须是数字" },
  ],
  sex: [{ required: true, message: "性别是必选项", trigger: "change" }],
  birth: [{ required: true, message: "出生日期是必选项" }],
  addr:[{ required: true, message: '地址是必填项' }],
  salesperson_id: [{ required: false, message: '请选择负责人', trigger: 'change' }]
})
const handleClose = () => {
  //获取并重置表单
  dialogVisible.value = false
  proxy.$refs.userForm.resetFields()
}
const handleCancel = () => {
  //获取并重置表单
  dialogVisible.value = false
  proxy.$refs.userForm.resetFields()
}
const handleAdd = () => { 
  dialogVisible.value = true
  action.value = 'add'
}
const timeFormat = (time) => {
  // 确保time是有效的日期
  const date = new Date(time)
  if (isNaN(date.getTime())) {
    return ''
  }
  var year = date.getFullYear()
  var month = date.getMonth() + 1
  var day = date.getDate()
  function add(m){
    return m < 10 ? '0' + m : m
  }
  return year + '-' + add(month) + '-' + add(day)
}
const onSubmit = async () => { 
  //校验表单
  try {
    await proxy.$refs.userForm.validate()
    
    // 确保birth始终是YYYY-MM-DD格式的字符串
    if (formUser.birth instanceof Date) {
      formUser.birth = timeFormat(formUser.birth)
    } else if (!/^\d{4}-\d{2}-\d{2}$/.test(formUser.birth)) {
      formUser.birth = timeFormat(formUser.birth)
    }
    
    if(action.value == 'add'){
      await proxy.$api.addUser(formUser)
      ElMessage({
        showClose: true,
        message: '新增成功',
        type: 'success',
      })
    }else{
      await proxy.$api.editUser(formUser)
      ElMessage({
        showClose: true,
        message: '编辑成功',
        type: 'success',
      })
    }
    
    // 无论API调用结果如何，都关闭对话框并重置表单
    dialogVisible.value = false
    proxy.$refs.userForm.resetFields()
    // 重新获取用户数据以显示最新状态
    getUserData()
  } catch (error) {
    // 处理表单校验失败的情况
    if (error === false) {
      ElMessage({
        showClose: true,
        message: '请填写正确的信息',
        type: 'error',
      })
    } else {
      // 处理其他错误
      console.error('提交失败:', error)
      ElMessage({
        showClose: true,
        message: '操作失败，请重试',
        type: 'error',
      })
      // 即使失败也关闭对话框并重置表单，避免用户卡在错误状态
      dialogVisible.value = false
      proxy.$refs.userForm.resetFields()
    }
  }
}
const handleEdit = (row) => { 
  action.value = 'edit'
  dialogVisible.value = true
  nextTick(() => { 
    Object.assign(formUser, {...row,sex:''+row.sex, salesperson_id: row.salesperson_id || ''})
  })
}

// 获取销售人员列表
const getSalespeople = async() => {
  try {
    const data = await proxy.$api.getSalespeople()
    salespeopleList.value = data || []
  } catch (error) {
    console.error('获取销售人员列表失败:', error)
    ElMessage({ 
      type: 'error', 
      message: '获取销售人员列表失败' 
    })
  }
}

onMounted(() => {
  getUserData()
  getSalespeople() // 加载销售人员列表
})

</script>

<template>
  <div class = "user-header">
    <el-button type = "primary" @click="handleAdd">新增</el-button>
    <el-form :inline="true" :model="formInline"> 
    <el-form-item label = "请输入">
        <el-input placeholder = "请输入用户名" v-model="formInline.keyWord"></el-input>
    </el-form-item>
    <el-form-item >
        <el-button type = "primary" @click="handleSearch">查询</el-button>
    </el-form-item>
    </el-form>
  </div>
  <div class = "user-table">
    <el-table :data="tableData" style="width: 100%">
    <el-table-column 
        v-for="item in tableLabel"
        :key="item.prop"
        :width="item.width ? item.width : 125"
        :prop="item.prop"
        :label="item.label"
    ></el-table-column>
    <el-table-column fixed="right" label="Operations" min-width="120">
      <template #default="scope">
        <el-button link type="primary" size="small" @click="handleEdit(scope.row)">
          编辑
        </el-button>
        <el-button link type="danger" size="small" @click="handleDelete(scope.row)">
          删除
        </el-button>
      </template>
    </el-table-column>
  </el-table>
  <el-pagination 
    class="pagination"
    background 
    layout="prev, pager, next" 
    :total="totalCount" 
    size="small"
    @current-change="handleChange"
    />
  </div>
  <el-dialog
    v-model="dialogVisible"
    :title="action == 'add' ? '新增用户' : '编辑用户'"
    width="35%"
    :before-close="handleClose"
  >
       <!--需要注意的是设置了:inline="true"，
		会对el-select的样式造成影响，我们通过给他设置一个class=select-clearn
		在css进行处理-->
    <el-form :inline="true"  :model="formUser" :rules="rules" ref="userForm">
      <el-row>
        <el-col :span="12">
          <el-form-item label="姓名" prop="name">
            <el-input v-model="formUser.name" placeholder="请输入姓名" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="年龄" prop="age">
            <el-input v-model.number="formUser.age" placeholder="请输入年龄" />
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="12">
          <el-form-item class="select-clearn" label="性别" prop="sex">
            <el-select  v-model="formUser.sex" placeholder="请选择">
              <el-option label="男" value="1" />
              <el-option label="女" value="0" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="出生日期" prop="birth">
            <el-date-picker
              v-model="formUser.birth"
              type="date"
              placeholder="请输入"
              style="width: 100%"
            />
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <el-form-item
          label="地址"
          prop="addr"
        >
          <el-input v-model="formUser.addr" placeholder="请输入地址" />
        </el-form-item>
      </el-row>
      <el-row>
        <el-col :span="12">
          <el-form-item label="负责人" prop="salesperson_id">
            <el-select v-model="formUser.salesperson_id" placeholder="请选择负责人" style="width: 200px;">
              <el-option
                v-for="item in salespeopleList"
                :key="item.id"
                :label="item.username"
                :value="item.id"
              ></el-option>
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row style="justify-content: flex-end">
        <el-form-item>
          <el-button type="primary" @click="handleCancel">取消</el-button>
          <el-button type="primary" @click="onSubmit">确定</el-button>
        </el-form-item>
      </el-row>
    </el-form>
  </el-dialog>
</template>

<style scoped lang = "less">
.user-header{
  display: flex;
  justify-content: space-between;

}
.user-table{
    position: relative;
    height: 520px;
    // 为Element Plus的分页组件添加样式，使用深度选择器
    .pagination {
      position: absolute;
      bottom: 30px; /* 添加px单位 */
      right: 10px; /* 添加px单位 */
      margin: 0;
      display: flex;
      justify-content: flex-end;
    }
    // 为Element Plus的表格组件添加样式
    :deep(.el-table) { 
        width: 100%;
        height: 500px;
    }
}
.select-clearn{
  display: flex;
}

</style>