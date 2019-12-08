<template>
  <div>
    <head-top :head="head">
        <img slot="left" src="../../../images/icon-return.png" @click="goBack"/>
    </head-top>
    <div class="person" style="padding: 2.1rem 0.75rem 0;">
        <div class="p-top">
            <div class="left-box">
                <div class="item-name" :class="{ font6: (detail.full_name.length==5 || detail.full_name.length==6),'font8': (detail.full_name.length==7 || detail.full_name.length==7) }">{{ detail.full_name }} - {{ detail.type_name }}</div>
                <div class="item-msg">{{ relation }}</div>
            </div>
            <div class="right-imgbox"><img :src="detail.image_url" v-if="detail.image_url!=''" alt=""> <img src="../../../images/icon-default-avatar.png" v-if="detail.image_url==''" alt=""> </div>
        </div>
        <div class="oper-items">
            <div class="item" @click="go_switch()" ><span class="item-name" >切换身份</span><div class="item-ico"><img src="../../../images/refresh-icon.png" alt=""></div></div>
            <div class="item" @click="go_infor()" ><span class="item-name"  >个人信息</span><div class="item-ico"><img src="../../../images/user-icon.png" alt=""></div></div>
            <div class="item" @click="go_quanzi()"   ><span class="item-name" >我的风采</span><div class="item-ico"><img src="../../../images/shouchang.png" alt=""></div></div>
            <div class="item" @click="go_family()" ><span class="item-name"  >我的家庭</span><div class="item-ico"><img src="../../../images/home-icon.png" alt=""></div></div>
        </div>
    </div>

  </div>
</template>

<script type="text/ecmascript-6">
  import HeadTop from '@/components/Head.vue'
  import { TransferDomDirective as TransferDom  } from 'vux'
  import { Cell, CellBox, Group  } from 'vux'
  import { accountDetail,getDomain,getParentDetaiInfor } from '../../../service/getData.js'
  import {initializeEnv,exitCurApp} from '../../../components/framework/serviceMgr.js'
  export default {
    directives: {
        TransferDom
    },
    data () {
      return {
        head:{
          icon: 'return',
          title: '个人中心',
          more: false,
        },
        detail:{},
        domain:'',
        relation:'',
      }
   },
   methods:{
      async getAccountDetail(){
          let res = await accountDetail();
          this.detail = res.d[0];
          if(res.d[0].type_id==2){
              this.$router.replace('/m/personal/teacher/home')
          }
          let resdetail = await getParentDetaiInfor(this.detail.id,this.detail.account_id);
          if(resdetail.c==0){
              for(let i in resdetail.d[0].children){
                  let relation = resdetail.d[0].children[i].relation;
                  if(relation==''){
                      relation='家长'
                  }
                this.relation+=resdetail.d[0].children[i].student_full_name+relation +'  '
              }
          }
      },
      go_switch(){
        let id = this.detail.id;
        let sid = this.$route.query.sid;
        this.$router.push({ path:'/m/personal/teacher/switch', query: { id: id , sid:sid }})
      },
      go_infor(){
        this.$router.push('/m/personal/parent/information')
      },
      go_family(){
        this.$router.push('/m/personal/parent/family');
      },
      goBack() {
          exitCurApp(this);
      },
      go_quanzi(){
          if(this.domain=='')return;
          window.location.href = 'http://'+this.domain+'/m/moment/momentMyList';
      }
   },
    async created(){
        window.document.title="个人中心"
        initializeEnv(this);
        this.getAccountDetail();
        let res = await getDomain();
        if(res.c==0){
            this.domain = res.d.domain;
        }
    },
    components: {
      HeadTop,
      Cell,
      CellBox,
      Group,
    },
  }

</script>

<style scoped>
    .p-top{height: 3.75rem;margin-top: 1.5rem;position: relative;}
    .p-top .left-box{width: 10.5rem;height:100%;}
    .p-top .item-name{height: 2.25rem;color: #444444;font-size: 1.5rem;text-align: center;line-height: 1;}
    .p-top .item-name.font6{font-size: 1.2rem;}
    .p-top .item-name.font8{font-size: 1rem;}
    .p-top .item-msg{height: 1.5rem;color: #888888;font-size: 0.75rem;width: 100%;background: #f5f5f5;border-radius: 0.75rem;line-height: 1.5rem;text-align: center;}
    .p-top .right-imgbox{position: absolute;right: 0;top: 0;width: 3.75rem;height: 3.75rem;box-sizing: border-box;border: solid 0.125rem #FFFFFF;border-radius: 50%;box-shadow: 0 0 0.15rem rgba(0,0,0,0.2);border-radius: 50%;overflow: hidden;}
    .p-top .right-imgbox img{width: 100%;}
    .oper-items .item{height: 3.75rem;border-bottom: solid 1px #eee;}
    .oper-items .item .item-name{line-height: 3.75rem;font-size: 0.9rem;color: #444;}
    .oper-items .item .item-ico{float: right;width: 1.25rem;height: 1.25rem;margin-top: 1.25rem;overflow: hidden; }
    .oper-items .item .item-ico img{display: block;width: 100%;}
</style>
