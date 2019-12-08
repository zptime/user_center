<template>
  <div>
    <head-top :head="head"></head-top>
    <div style="padding: 3.6rem 0.75rem 0;">
        <div class="add-btn" @click="go_invite()">邀请家庭成员</div>
        <div class="f-items">
            <div class="item boxShadowGray" v-for="item in list">
                <div class="item-imgbox"><img v-if="item.student_image_url !='' " :src="item.student_image_url" alt=""><img v-if="item.student_image_url =='' " src="../../../images/icon-default-avatar.png" alt=""></div>
                <div class="item-name">{{ item.student_full_name }} - {{ item.relation }}</div>
                <div v-if="false" class="item-write"></div>
                <div v-if="false" class="item-out"></div>
            </div>
        </div>
        <div class="bottomButton boxShadowBlue" @click="addChild()">+ 添加孩子</div>
    </div>
  </div>
</template>

<script type="text/ecmascript-6">
  import HeadTop from '@/components/Head.vue'
  import { TransferDomDirective as TransferDom  } from 'vux'
  import { accountDetail,familyMember } from '../../../service/getData.js'

  export default {
    directives: {
        TransferDom
    },
    data () {
      return {
        head:{
          icon: 'return',
          title: '我的家庭',
          more: false
        },
        id:'',
        name:'',
        list:[]
      }
   },
   methods:{
      go_invite(){
          this.$router.push({path:'/m/personal/parent/invite',query:{ id : this.id ,name:this.name }})
      },
      async getAccountDetail(){
          let res = await accountDetail();
          this.id = res.d[0].school_id;
          this.name = res.d[0].full_name;
      },
      async getFamilyMember(){
          let res = await familyMember();
          this.list = res.d
      },
      addChild(){
          this.$router.push('/m/personal/parent/addChild')
      }
   },
  created(){
      window.document.title="个人中心"
      this.getAccountDetail();
      this.getFamilyMember();
  },
    components: {
      HeadTop,
    },
  }

</script>

<style scoped>
.add-btn{height: 2rem;border-radius: 1rem;text-align: center;line-height: 2rem;border: solid 1px #4685ff;color: #4685ff;font-size: 0.75rem;}
.f-items{margin-top: 1.5rem;}
.f-items .item{height: 2.5rem;border-radius: 1rem;position: relative;padding: 0.25rem;margin-bottom: 1rem;}
.f-items .item .item-imgbox{width: 2rem;height: 2rem;border-radius: 50%;overflow: hidden;position: absolute;left: 0.25rem;top: 0.25rem;}
.f-items .item .item-imgbox img{width: 100%;}
.f-items .item .item-name{padding-left: 2.75rem;line-height: 2rem;font-size: 0.75rem;color: #444444;}
.f-items .item .item-write{width: 1.25rem;height: 1.25rem;position: absolute;top: 0.625rem;right: 3.5rem;background: url("../../../images/icon-write.png")no-repeat center;background-size: 100% 100%;}
.f-items .item .item-out{width: 1.25rem;height: 1.25rem;position: absolute;top: 0.625rem;right: 1rem;background: url("../../../images/icon-out.png")no-repeat center;background-size: 100% 100%;}
.bottomButton{  width:7.5rem;  margin:2.5rem auto;height: 2rem;  line-height: 2rem;  text-align: center;  background-color: #4685ff;  color:#fff;  font-size: 0.75rem;  -webkit-border-radius: 1rem;  -moz-border-radius: 1rem;  -ms-border-radius: 1rem;  -o-border-radius: 1rem;  border-radius: 1rem;}

</style>
