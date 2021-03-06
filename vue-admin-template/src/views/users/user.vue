<template>
  <div class="app-container">
    <!-- 搜索和添加用户按钮-->
    <el-row>
      <el-col :span="12">
        <el-input v-model="params.username"
                  placeholder="搜索用户名"
                  @keyup.enter.native="handleSearch">
          <el-button slot="append"
                     icon="el-icon-search"
                     @click="handleSearch" />
        </el-input>
      </el-col>
      <el-col :span="12"
              align="right"
              style="padding-right:20px;">
        <el-button v-if="addGroupPerm"
                   type="primary"
                   @click="addUserVisible=true">添加用户</el-button>
      </el-col>
    </el-row>
    <!-- 展示用户信息按钮-->
    <el-table :data="userList"
              stripe
              style="width: 100%">
      <el-table-column prop="username"
                       label="username" />
      <el-table-column prop="name"
                       label="姓名" />
      <el-table-column prop="phone"
                       label="电话" />
      <el-table-column prop="email"
                       label="email" />
      <el-table-column prop="is_active"
                       label="状态">
        <template slot-scope="scope">
          <el-switch v-model="scope.row.is_active"
                     @change="handleUserStatusChange(scope.row)" />
        </template>
      </el-table-column>
      <el-table-column prop="last_login"
                       label="last_login" />
      <el-table-column fixed="right"
                       label="操作">
        <template slot-scope="scope">
          <el-button type="text"
                     size="small"
                     @click="handleAssignGroup(scope.row)">指定角色</el-button>
          <el-button type="text"
                     size="small"
                     @click="handleModify(scope.row)">修改</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页-->
    <el-row v-show="total>10"
            ype="flex"
            justify="center"
            style="padding-top:20px;">
      <el-pagination :total="total"
                     layout="prev, pager, next"
                     background
                     @current-change="handleChange" />
    </el-row>

    <!-- 调用子组件 -->
    <AddUserForm v-model="addUserVisible"
                 @fetch="handleFetch" />
    <ModifyUserForm v-model="modifyUserVisible"
                    :user-id="userId"
                    @fetch="handleFetch" />
    <AssignGroup v-model="assignGroupVisible"
                 :user-id="userId"
                 :user-name="userName" />
  </div>
</template>
<script>
// 导入api和子组件
import { getUserList, modifyUser } from '@/api/user'
import { checkPermission } from '@/utils/auth'
import AddUserForm from './components/AddUserForm'
import ModifyUserForm from './components/ModifyUser'
import AssignGroup from './components/assignGroup'
export default {
  name: 'UserList',
  components: { // 子组件注册
    AddUserForm,
    ModifyUserForm,
    AssignGroup
  },
  data () {
    return {
      userList: [],
      addUserVisible: false,
      modifyUserVisible: false,
      userId: 0,
      userName: '',
      total: 0,
      params: {
        page: 1,
        username: ''
      },
      assignGroupVisible: false
    }
  },
  computed: { // 权限验证
    addGroupPerm: function () {
      return checkPermission('users.add_user') // 参数:添加用户的权限
    }
  },
  created () { // 页面加载完之后获取用户列表
    this.fetchUserList()
  },
  methods: {
    fetchUserList () { // 获取用户列表,调用api接口getUserList
      getUserList(this.params).then(res => {
        this.userList = res.results
        this.total = res.count
      })
    },
    handleUserStatusChange (obj) { // 修改用户状态is_active,调用api接口modifyUser
      modifyUser(obj.id, { is_active: obj.is_active }).then(() => {
        this.$message({
          message: `修改 ${obj.name} 的状态成功`,
          type: 'success'
        })
      })
    },
    handleFetch () { // 获取用户列表,调用方法fetchUserList()
      this.fetchUserList()
    },
    handleModify (obj) {
      this.userId = obj.id
      this.modifyUserVisible = true
    },
    handleChange (val) { // 分页
      this.params.page = val
      this.fetchUserList()
    },
    handleSearch () { // 搜索
      this.params.page = 1
      this.fetchUserList()
    },
    handleAssignGroup (obj) {
      this.userId = obj.id
      this.userName = obj.name
      this.assignGroupVisible = true
    }
  }
}
</script>
