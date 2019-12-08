<template>
  <div>
    <head-top :head="head"></head-top>
    <div style="padding: 3.6rem 0.75rem 0;">
        <p>扫二维码成为家庭成员。</p>
        <p>从此关心孩子的学校生活。</p>
        <div class="qrbox" ><img :src="code" alt=""></div>
    </div>
  </div>
</template>

<script type="text/ecmascript-6">
  import HeadTop from '@/components/Head.vue'
  import { TransferDomDirective as TransferDom  } from 'vux'
  import { parentQrcode } from '../../../service/getData.js'

  export default {
    directives: {
        TransferDom
    },
    data () {
      return {
        head:{
          icon: 'return',
          title: '邀请家庭成员',
          more: false
        },
        name:'',
        code:'',
      }
   },
   methods:{

   },
   async created(){
     window.document.title="个人中心"
     this.name = this.$route.query.name;
     let id = this.$route.query.id;
     let res = await parentQrcode(id);
     if(res.c==0){
         this.code = 'data:image/gif;base64, '+res.d.invite_base64_image;
     }
   },
    components: {
      HeadTop,
    },
  }

</script>

<style scoped>
.qrbox{line-height: 10rem;text-align: center;border: solid 1px #eee;width: 10rem;margin: 2rem auto;height: 10rem;overflow: hidden;}
.qrbox img{width:10rem;height: 10rem;}
</style>
