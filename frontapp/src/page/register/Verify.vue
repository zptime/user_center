<template>
  <div :class="{'noHeadContent':!regShowHead}">
    <headTop :head="head" v-if="regShowHead"></headTop>
    <div class="contentBox" v-cloak>
      <div class="phone">
        请使用<span>{{ mobile }}</span>的手机号验证
      </div>
      <!--<div>{{ info.openid }}</div>-->
      <!--<div>{{ info.sid }}</div>-->
      <div class="code borderRadius boxShadowGray">
        <input placeholder="请输入验证码" type="text" maxlength="4" v-model="code"/>
      </div>
      <div class="btnOpt">
        <div class="btnCommon btnBottomOpt boxShadowGray clb">
          <span class="btn_sure left" @click="optClick('code')" v-if="codeFlag">
            发送验证码
          </span>
          <span class="btn_sure left c-gray" @click="optClick('code')" v-else>
            重发({{ countdown }})
          </span>
          <span class="btn_divide"></span>
          <span class="btn_sure right" @click="optClick('sure')">确定</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script type="es6">
  import HeadTop from '@/components/Head'
  import Global from '@/components/Global.vue'
  import { mapState,mapMutations } from 'vuex'
  import { wxSendTeacherCode,wxSendParentCode,wxBindParent,wxBindTeacher,InviteParent } from '../../service/getData'

  //验证码界面
  export default ({
    data (){
      return {
        head:{
          icon: 'return',
          title: '身份验证',
          more: false
        },
        regShowHead:Global.regShowHead,
        mobile:"",//绑定的手机号
        codeFlag:true,//是否显示“发送验证码”按钮
        code:"",//input验证码的值
        countdown:60,
        enroll:'',//教师或家长注册标志
        info:{},//注册信息
      }
    },
    computed:{
      ...mapState([
        'parentInfo',
        'teacherInfo',
        'openid',
        'sid',
      ])
    },
    components:{
      HeadTop,
    },
    created(){
      this.initData();
      if(!this.regShowHead){
        document.title='身份验证';
      }
    },
    methods: {
      ...mapMutations([
        'PARENTINFO',
        'TEACHERINFO',
      ]),

      initData(){
        this.enroll = this.$route.query.enroll;
        if(this.enroll=='parent'){
          this.info = this.parentInfo;
        }else if(this.enroll=='teacher'){
          this.info = this.teacherInfo;
        }
        this.mobile = this.info.mobile;
        this.info.openid = this.openid;
        this.info.sid = this.sid;
      },

      //底部操作栏
      optClick(opt){
        if(opt=='code'){
          if(this.codeFlag){
            this.sendCode();
          }
        }else if(opt=='sure'){
          if(this.code){
            this.info.messagecode = this.code;
            if(this.enroll=='parent'){
              this.registerParent();
            }else if(this.enroll=='teacher'){
              this.registerTeacher();
            }
          }else{
            this.$vux.toast.show({
              type: 'text',
              text: '请输入验证码'
            });
          }
        }
      },

      //发送验证码
      async sendCode(){
        let _this=this;
        let res;
        if(this.enroll=='parent'){
          res = await wxSendParentCode(_this.mobile);
        }else{
          res = await wxSendTeacherCode(_this.mobile);
        }
        if (res.c == 0){
          _this.codeFlag=false;
          //倒计时
          let t = setInterval(function () {
            if (_this.countdown == 1) {
              _this.codeFlag =true;
              _this.countdown = 60;
              clearInterval(t);
            } else {
              _this.countdown--;
            }
          },1000);
        }else{
          this.$vux.toast.show({
            type: 'text',
            text: res.m
          });
        }
      },

      //注册家长信息
      async registerParent(){
        let tmp = this.info;
        let res = '';
        let id = this.$route.query.id;
        if(!!id){
            res = await InviteParent(id,tmp.mobile,tmp.fullname,tmp.sex,tmp.address,tmp.messagecode,tmp.openid,tmp.student_list_json[0].relation)
        }else{
            res = await wxBindParent(tmp.mobile,tmp.fullname,tmp.sex,tmp.address,
            JSON.stringify(tmp.student_list_json),tmp.messagecode,tmp.openid,tmp.sid,'');
        }
        if(res.c==0){
          this.$vux.toast.show({
            type: 'text',
            text: '绑定成功'
          });
          //this.$router.push('/m/homePage');
          window.location.href = '/m/homePage?sid='+this.sid;
        }else{
          this.$vux.toast.show({
            type: 'text',
            text: res.m
          });
        }
      },

      //注册教师信息
      async registerTeacher(){
        let tmp = this.info;
        let res = await wxBindTeacher(tmp.mobile,tmp.address, JSON.stringify(tmp.student_list_json),
          tmp.messagecode,tmp.openid,tmp.sid,'');
        if(res.c==0){
          this.$vux.toast.show({
            type: 'text',
            text: '绑定成功'
          });
          //this.$router.push('/m/homePage');
          window.location.href = '/m/homePage?sid='+this.sid;
        }else{
          this.$vux.toast.show({
            type: 'text',
            text: res.m
          });
        }
      }
    },
  })
</script>

<style scoped>
  .phone{
    text-align: center;
    font-size: 0.75rem;
    margin:2.5rem auto;
    color:#444;
  }
  .phone span{
    margin:0 0.4rem;
  }
  .code{
    width:13rem;
    height:2rem;
    margin:0 auto;
  }
  .code input{
    height:2rem;
    caret-color:#ff5d42;
    font-size: 0.7rem;
    line-height: 0.7rem;
    padding-left:0.5rem;
  }
  .c-gray{
    color:#aaa !important;
  }
  .button{
    width:5rem;
    height:2rem;
    line-height: 2rem;
    background-color: #4685ff;
    border-radius: 4px;
    font-size: 0.75rem;
    color:#fff;
    text-align: center;
  }
</style>
