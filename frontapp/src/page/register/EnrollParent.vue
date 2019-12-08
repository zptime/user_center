<template>
  <div :class="{'noHeadContent':!regShowHead}">
    <head-top :head="head" v-if="regShowHead"></head-top>
    <div class="contentBox" v-cloak>
      <div class="info">
        <div class="warn">
          以下为家长注册信息，为确保数据真实性，请家长务必认真填写
        </div>
        <div class="base-info">
          <div class="title">基本信息</div>
          <div class="detail">
            <div class="detail-item">
              <span class="detail-opt">
                <x-input v-model="baseInfo.fullname" placeholder="请填写姓名"></x-input>
              </span>
            </div>
            <div class="detail-item border-bottom-none">
              <span class="detail-title">性别</span>
              <span class="detail-opt sex-opt">
                <span @click="changeSex(true)">
                  <img src="../../images/icon-select.png" v-if="baseInfo.sex">
                  <img src="../../images/icon-deselect.png" v-else>
                </span>
                <span class="sex">男</span>
                <span @click="changeSex(false)">
                  <img src="../../images/icon-deselect.png" v-if="baseInfo.sex">
                  <img src="../../images/icon-select.png" v-else>
                </span>
                <span>女</span>
              </span>
            </div>
          </div>
        </div>
        <div class="base-info" v-for="(item,index) in childInfo">
          <div class="title">
            <span>孩子信息</span>
            <span class="num" v-if="childInfo.length>1">{{ index+1 }}</span>
            <span class="del right" v-if="childInfo.length>1 && index>0" @click="delChild(index)">删除</span>
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
            <div class="detail-item border-bottom-none" @click="chooseRelation(index)">
              <span>选择与孩子的关系</span>
              <span class="detail-opt select-opt">
                <img src="../../images/icon-arrow-right.png">
              </span>
              <span class="relation right">{{ item.relation }}</span>
            </div>
          </div>
        </div>
        <div class="btnCommon bottomButton boxShadowBlue" @click="addChild">+ 添加孩子</div>
        <div class="base-info">
          <div class="title">联系方式</div>
          <div class="detail">
            <div class="detail-item border-bottom-none">
              <span class="detail-opt">
                <x-input v-model="baseInfo.mobile" keyboard="number" is-type="china-mobile" :max="13"
                         placeholder="请填写微信绑定的手机号或常用手机号">
                </x-input>
              </span>
            </div>
          </div>
        </div>
        <div class="base-info">
          <div class="title">通讯地址</div>
          <div class="detail">
            <div class="detail-item detail-item-addr border-bottom-none">
              <span class="detail-opt">
                <x-textarea v-model="baseInfo.address" placeholder="请填写准确的家庭地址，以免无法正确接受学校寄出去的通知文件" :rows="2" autosize></x-textarea>
              </span>
            </div>
          </div>
        </div>
      </div>
      <div class="btnOpt">
        <div class="btnCommon btnBottomOpt boxShadowGray clb">
          <span class="btn_cancel left" @click="optClick('cancel')">取消</span>
          <span class="btn_divide"></span>
          <span class="btn_sure right" @click="optClick('sure')">下一步</span>
        </div>
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
  import Relation from './Relation.vue'
  import Global from '@/components/Global.vue'
  import { mapState,mapMutations } from 'vuex'
  import { getQueryString } from '../../config/mUtils.js'
  import { wxBindParent } from '../../service/getData'
  export default {
    data(){
      return {
        head:{
          icon: 'return',
          title: '家长注册',
          more: false
        },
        regShowHead:Global.regShowHead,
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
    computed:{
      ...mapState([
        'parentInfo',
        'openid',
        'sid',
        'mobile',
        'addr',
      ])
    },
    created(){
      this.initData();
      if(!this.regShowHead){
        document.title='家长注册';
      }
    },
    methods:{
      ...mapMutations([
        'PARENTINFO',
        'OPENID',
        'SID',
      ]),

      initData(){
        if(getQueryString('sid')){
          this.OPENID(getQueryString('openid'));
          this.SID(getQueryString('sid'));
        }
        if(this.mobile){
          this.baseInfo.mobile = this.mobile;
          //alert(this.baseInfo.mobile);
        }
        if(this.addr){
          this.baseInfo.address = this.addr;
          //alert(this.baseInfo.address);
        }
      },

      //性别切换
      changeSex(value){
        this.baseInfo.sex = value;
      },

      //添加孩子
      addChild(){
        this.childInfo.push({
          "full_name":'',
          "code":'',
          "relation":''
        })
      },

      //删除孩子
      delChild(index){
        this.childInfo.splice(index,1);
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
        let showMsg = '';
        if(this.baseInfo.fullname==''){
          showMsg = '请输入姓名';
        }else if(this.baseInfo.mobile==''){
          showMsg = '请输入联系方式';
        }else if(!(/^1[3|4|5|7|8][0-9]{9}$/.test(this.baseInfo.mobile))){
          showMsg = '请输入格式正确的手机号';
        }else if(this.childInfo[0].full_name=='' || this.childInfo[0].code=='' || this.childInfo[0].relation==''){
          showMsg = '请至少绑定一个孩子的完整信息';
        }

        if(showMsg){
          this.$vux.toast.show({
            type: 'text',
            text:  showMsg
          })
        }else{
          if(this.baseInfo.sex){
            this.baseInfo.sex = '男';
          }else{
            this.baseInfo.sex = '女';
          }
          this.baseInfo.student_list_json = this.childInfo;
          this.PARENTINFO(this.baseInfo);
          this.nextVerify();
        }
      },
      //“下一步”验证函数
      async nextVerify(){
        let tmp = this.baseInfo;
        let  res = await wxBindParent(tmp.mobile,tmp.fullname,tmp.sex,tmp.address,
          JSON.stringify(tmp.student_list_json),tmp.messagecode,this.openid,this.sid,1);
        if(res.c==0){
          this.$router.push({
            name:'verify',
            query:{
              enroll:'parent'
            }
          })
        }else{
          this.$vux.toast.show({
            type: 'text',
            text: res.m
          });
        }
      }
    },
  }
</script>

<style scope>
  @import '../../style/register.css';
  .contentBox{
    overflow-y: auto;
    bottom:0;
    -webkit-overflow-scrolling: touch;
  }
  .right{float: right !important;}
  .btnOpt{  margin-bottom: 2rem;  }
</style>
