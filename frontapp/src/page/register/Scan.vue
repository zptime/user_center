<template>
  <div :class="{'noHeadContent':!regShowHead}">
    <head-top :head="head" v-if="regShowHead"></head-top>
    <div class="contentBox" v-cloak>
      <div class="tip-content">
        <div class="tip">{{ personInfo.school }}</div>
        <div class="tip">扫码二维码注册成为{{ personInfo.identity }}</div>
      </div>
      <div class="scan-img">
        <img src="../../images/icon-scan.png" @click="enrollParent">
      </div>
    </div>
  </div>
</template>

<script type="es6">
  import HeadTop from '@/components/Head.vue'
  import Global from '@/components/Global.vue'
  export default {
    data(){
      return {
        head:{
          icon: 'return',
          title: '学校二维码',
          more: false
        },
        regShowHead:Global.regShowHead,
        personInfo:{//个人信息
          "school":'华中科技大学附属小学',
          "identity":'学生家长'
        }
      }
    },
    components:{
      HeadTop,
    },
    created(){
      if(!this.regShowHead){
        document.title='学校注册';
      }
    },
    methods:{
      //跳入家长注册页面
      enrollParent(){
        //this.$router.push('enrollParent');
        this.$router.push({
          //name:'enrollParent',
          name:'identify',
          query:{
            sid:1,
            openid:'oi5ku1T1_9j8y1jPs58lbG9AL-Bs',
          }
        });
      },
    }
  }
</script>

<style scope>
  /*提示信息样式*/
  .tip-content{
    text-align: center;
    margin:2rem 0;
    padding: 0 0.75rem;
  }
  .tip-content .tip{
    margin:0.5rem 0 1rem 0;
    color:#aaa;
    font-size: 0.8rem;
  }
  .scan-img{
    text-align: center;
  }
  .scan-img img{
    width:10rem;
    height: 10rem;
  }
</style>
