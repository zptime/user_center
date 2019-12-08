import {setStore, getStore} from '../config/mUtils'

import {baseUrl, imgBaseUrl} from '../config/env'

import {
	ACCOUNT,
  PARENTINFO,
  TEACHERINFO,
  OPENID,
  SID,
  MOBILE,
  ADDR,
} from './mutation-types.js'

export default {
	//登录用户
	[ACCOUNT](state, account){
		state.account = account
	},

  //家长注册信息
  [PARENTINFO](state, parentInfo){
    state.parentInfo = parentInfo
  },

  //教师注册信息
  [TEACHERINFO](state, teacherInfo){
    state.teacherInfo = teacherInfo
  },

  //微信openid
  [OPENID](state, openid){
    state.openid = openid
  },

  //学校编码
  [SID](state, sid){
    state.sid = sid
  },

  //用户注册-手机号
  [MOBILE](state, mobile){
    state.mobile = mobile
  },

  //用户注册-地址
  [ADDR](state, addr){
    state.addr = addr
  },
}
