import Vue from 'vue'
import Vuex from 'vuex'
import mutations from './mutations'
import actions from './action'
import getters from './getters'

Vue.use(Vuex)

const state = {
	account:{}, //登录用户
  parentInfo:{},//家长注册信息
  teacherInfo:{},//教师注册信息
  openid:'',//微信openid
  sid:'',//学校编码
  mobile:'',//用户注册-手机号
  addr:'',//用户注册-地址
  env : {
    os : '',
    process: '',
    signUrl:'',
    sid:'',
  },
}

export default new Vuex.Store({
	state,
	getters,
	actions,
	mutations,
})
