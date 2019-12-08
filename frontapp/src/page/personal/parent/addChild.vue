<template>
  <div>
    <head-top :head="head"></head-top>
    <div class="contentBox" v-cloak>
      <div class="info">
        <div class="base-info" v-for="(item,index) in childInfo">
          <div class="title">
            <span >孩子信息</span>
          </div>
          <div class="detail">
            <div class="detail-item">
              <span class="detail-opt">
                <x-input v-model="item.full_name" placeholder="请填写孩子姓名"></x-input>
              </span>
            </div>
            <div class="detail-item">
              <span class="detail-opt">
                <x-input v-model="item.code" placeholder="请填写孩子的学号，学号与姓名必须匹配"></x-input>
              </span>
            </div>
            <div class="detail-item border-bottom-none">
              <span class="detail-title">性别</span>
              <span class="detail-opt sex-opt">
                <span @click="changeSex(true)">
                  <img src="../../../images/icon-select.png" v-if="baseInfo.sex">
                  <img src="../../../images/icon-deselect.png" v-else>
                </span>
                <span class="sex">男</span>
                <span @click="changeSex(false)">
                  <img src="../../../images/icon-deselect.png" v-if="baseInfo.sex">
                  <img src="../../../images/icon-select.png" v-else>
                </span>
                <span>女</span>
              </span>
            </div>
            <div class="detail-item border-bottom-none" @click="chooseRelation(index)">
              <span>选择与孩子的关系</span>
              <span class="detail-opt select-opt">
                <img src="../../../images/icon-arrow-right.png">
              </span>
              <span class="relation right">{{ item.relation }}</span>
            </div>
          </div>
        </div>
        <div class="btnCommon bottomButton boxShadowBlue" @click="addChild()">确定</div>

      </div>
      <popup v-model="showPopup" width="100%" height="100%" position="right" :show-mask=false>
        <relation :child-ind="childInd" @on-close="changePopup" @on-choose="choosePop"></relation>
      </popup>
    </div>
  </div>
</template>

<script type="text/ecmascript-6">
  import HeadTop from '@/components/Head.vue'
  import XTextarea from 'vux/src/components/x-textarea/index'
  import XInput from 'vux/src/components/x-input/index'
  import Popup from 'vux/src/components/popup/index.vue'
  import Relation from '../../register/Relation.vue'
  import { getQueryString } from '../../../config/mUtils.js'
  import { addChildByParent } from '../../../service/getData.js'

  export default {
    data(){
      return {
        head:{
          icon: 'return',
          title: '添加孩子',
          more: false
        },
        baseInfo:{//注册信息列表
          "fullname":'', //家长姓名
          "sex":true, //家长性别
          "address":'', //地址
          "mobile":'', //电话号码-必填
          "student_list_json":'',//学生信息列表-必填
          "messagecode":'', //短信验证码-必填
          "openid":'', //微信openid-必填
          "sid":'', //学校编码-必填
        },
        childInfo:[{//孩子信息
          "full_name":'',
          "code":'',
          "relation":''
        }],

        childInd:'',//孩子列表序号
        showPopup:false,
      }
    },
    components:{
      HeadTop,
      XTextarea,
      XInput,
      Popup,
      Relation,
    },
    created(){
        window.document.title="个人中心"
   //   this.initData();
    },
    methods:{
      //性别切换
      changeSex(value){
        this.baseInfo.sex = value;
      },

      //添加孩子
      async addChild(){
        let showMsg = '';

        if(this.childInfo[0].full_name=='' || this.childInfo[0].code=='' || this.childInfo[0].relation==''){
          showMsg = '请填写孩子完整的信息';
        }
        if(showMsg){
          this.$vux.toast.show({
            type: 'text',
            text:  showMsg
          })
        }else{
          if(this.baseInfo.sex){
            this.childInfo[0].sex = '男';
          }else{
            this.childInfo[0].sex = '女';
          }
            this.$vux.loading.show();
            let student_list_json = [];
            student_list_json.push(this.childInfo[0])
            let res = await addChildByParent(JSON.stringify(student_list_json))
            if(res.c==0){
                this.$vux.loading.hide();
                this.$route.back(-1)
            }
        }

      },

      //选择关系
      chooseRelation(index){
        this.childInd = index;
        this.changePopup();
      },

      changePopup(){
        this.showPopup = !this.showPopup;
      },

      //选择关系完成事件
      choosePop(index,relation){
        this.childInfo[index].relation = relation;
        this.changePopup();
      },

      //底部操作栏
      optClick(opt){
        if(opt=='cancel'){
          this.$router.back();
        }else if(opt=='sure'){
          this.dealInfo();
        }
      },

      //"下一步"处理数据
      dealInfo(){

      }
    },
  }
</script>

<style scope>
  @import '../../../style/register.css';
  .contentBox{
    overflow-y: auto;
    bottom:0;
    -webkit-overflow-scrolling: touch;
  }
  .right{float: right !important;}
  .btnOpt{  margin-bottom: 2rem;  }
</style>
