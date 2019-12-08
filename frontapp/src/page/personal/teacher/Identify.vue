<template>
  <div class="identify">
    <head-top :head="head"></head-top>
    <div class="contentBox" v-cloak>
      <div class="content">
        <div class="identify-img">
          <img src="../../../images/icon-identify-teacher.png" @click="enroll('teacher')">
        </div>
        <div class="title">我是教师</div>
        <div class="tip">注册时请使用学校登记的手机号，进行注册</div>
        <div class="identify-img">
          <img src="../../../images/icon-identify-parent.png" @click="enroll('parent')">
        </div>
        <div class="title">我是家长</div>
      </div>
      <!--<div>{{ openid }}</div>-->
      <!--<div>{{ sid }}</div>-->
    </div>
  </div>
</template>

<script type="text/ecmascript-6">
  import HeadTop from '@/components/Head.vue'
  import { mapState,mapMutations } from 'vuex'
  import { getQueryString } from '../../../config/mUtils.js'
  export default {
    data(){
      return {
        head:{
          icon: 'return',
          title: '华中科技大学附属小学',
          more: false
        },
      }
    },
    components:{
      HeadTop,
    },
    computed:{
      ...mapState([
        'openid',
        'sid',
      ])
    },
    created(){
      window.document.title='个人中心';
      this.initData();
    },
    methods:{
      ...mapMutations([
        'OPENID',
        'SID',
      ]),

      initData(){
        this.OPENID(getQueryString('openid'));
        this.SID(getQueryString('sid'));
      },

      //跳入注册页面
      enroll(val){
        if(val=='teacher'){
          this.$router.push('enrollTeacher');
        }else if(val=='parent'){
          this.$router.push('enrollParent');
        }
      }
    }
  }
</script>

<style scope>
  .content{
    text-align: center;
  }
  .identify .identify-img{
    margin-top:3.5rem;
  }
  .identify .identify-img img{
    /*400*240(360*200)*/
    /*600*360(540*300)*/
    width:10rem;
    height:6rem;
  }
  .identify .title{
    font-size: 0.75rem;
    color:#444;
    margin-top:0.25rem;
  }
  .identify .tip{
    font-size: 0.5rem;
    color:#aaa;
    margin-top:0.5rem;
  }
</style>
