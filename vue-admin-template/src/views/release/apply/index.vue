<template>
  <div class="apply">
    <el-form ref="form"
             :model="form"
             :rules="rules"
             label-width="180px">
      <el-form-item label="选择项目："
                    prop="name">
        <el-select v-model="form.name"
                   placeholder="请选择项目类型"
                   style="width: 60%;"
                   @change="getTag">
          <el-option v-for="item in project_list"
                     :key="item.index"
                     :label="item.name"
                     :value="item.name" />
        </el-select>
      </el-form-item>

      <el-form-item label="项目版本："
                    prop="version">
        <el-select v-model="form.version"
                   value-key="label"
                   placeholder="请选择项目版本"
                   style="width: 60%;"
                   @change="getTaginfo">
          <el-option v-for="item in tag_list"
                     :key="item.index"
                     :label="item.name"
                     :value="item.name" />
        </el-select>
      </el-form-item>

      <el-form-item label="版本信息："
                    prop="info">
        <el-input v-model="form.info"
                  style="width: 60%;" />
      </el-form-item>

      <el-form-item label="指派给："
                    prop="assign_to">
        <el-select v-model="form.reviewer"
                   filterable
                   placeholder="请选择项目处理人"
                   style="width: 60%;">
          <el-option v-for="item in sa_list"
                     :key="item.index"
                     :label="item.name"
                     :value="item.id" />
        </el-select>
      </el-form-item>

      <el-form-item label="上线详情："
                    prop="detail">
        <el-input v-model="form.detail"
                  type="textarea"
                  rows="8"
                  style="width: 60%;" />
      </el-form-item>

      <el-form-item>
        <el-button type="primary"
                   @click="onSubmit">申请上线</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { getGroupMemberList } from '@/api/group'
import { getProjectList, getProjectTag } from '@/api/project/project'
import { createDeploy } from '@/api/release/release'
export default {
  data () {
    return {
      form: {
        name: '',
        version: '',
        info: '',
        detail: '',
        reviewer: ''
      },
      rules: {
        name: [
          { required: true, message: '请输入项目名称', trigger: 'blur' }
        ],
        version: [
          { required: true, message: '请输入项目版本', trigger: 'blur' }
        ],
        info: [
          { required: true, message: '请输人项目内容', trigger: 'blur' }
        ],
        reviewer: [
          { required: true, message: '请输人项目执行人', trigger: 'blur' }
        ]

      },
      sa_list: [],
      project_list: [],
      tag_list: [],
      state: 0
    }
  },

  watch: {
    state () {
      getGroupMemberList(6).then(res => { // 获取组下的成员列表,ops组的id是6
        this.sa_list = res.results
        // console.log(this.sa_list)
      })

      getProjectList().then(res => {
        this.project_list = res
        // console.log(this.project_list)
      })
    }

  },

  created () {
    this.state = 1
  },

  methods: {
    /* 获取某个项目的tag列表*/
    getTag (name) { // 参数name就是项目名,选中一个项目的时候获取到的,因为value值是name
      let obj = {}
      obj = this.project_list.find((item) => { // 遍历所有的项目列表来反查,如果项目名是一致的就返回 保存到obj对象里
        return item.name === name
      })
      console.log(obj) // 拿到gitlab上这个项目的所有信息
      const params = { 'project_id': obj.id } // 获取项目id
      getProjectTag(params).then(res => { // 调用getProjectTag,需要传project_id,获取这个项目的所有tag列表
        this.tag_list = res
        // console.log(this.tag_list)
      })
    },
    /* 跟进tag名获取message */
    getTaginfo (name) {
      let obj = {}
      obj = this.tag_list.find((item) => { //  遍历所有的tag列表
        return item.name === name
      })
      console.log(obj)
      this.form.info = obj.info
      // 将tag信息赋值给this.form.info,这个又和v-model绑定了,所以页面taginfo会相应的随着tag变化而变化
    },
    /* 申请上线 */
    onSubmit () {
      this.$refs.form.validate((valid) => {
        if (!valid) {
          return
        }
        const params = Object.assign({}, this.form)
        console.log(params)
        createDeploy(params).then(res => {
          this.$message({
            message: '申请上线成功',
            type: 'success'
          })
          this.$router.push({ path: '/release/list' })
        })
      })
    }
  }

}
</script>

<style scoped>
.line {
  text-align: center;
}
.apply {
  margin-top: 2cm;
}
</style>

