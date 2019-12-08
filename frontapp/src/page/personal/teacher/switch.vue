<template>
  <div v-cloak >
    <head-top :head="head"></head-top>
    <div style="padding: 3.6rem 0.75rem 0;">
       <div class="switch-items">
           <div class="item boxShadowGray borderRadius"  v-for="item in userlist"  v-if="item.school_id==school_id"     @click="selectOne(item.id,item.school_id,item.type_id)"    >
               <div class="img-box boxShadowGray"><img v-if="item.image_url !=0 "      :src="item.image_url" alt=""><img v-if="item.image_url ==0 " src="../../../images/icon-default-avatar.png" alt="">   </div>
               <div class="item-msg">
                   <div class="item-name">{{ item.full_name }}  ({{ item.type_name }})</div>
                   <div class="item-school">{{ item.school_name }}</div>
                   <div class="item-select"  :class="{ has_select : item.isselect }" ></div>
               </div>
           </div>
       </div>
       <div class="bottomButton boxShadowBlue" @click="addPerson()">+ 添加角色</div>
    </div>
  </div>
</template>

<script type="text/ecmascript-6">
  import HeadTop from '@/components/Head.vue'
  import { TransferDomDirective as TransferDom  } from 'vux'
  import { getUserTypeList,switchPerson,accountDetail } from '../../../service/getData.js'
  export default {
    directives: {
        TransferDom
    },
    data () {
      return {
        head:{
          icon: 'return',
          title: '选择角色',
          more: false
        },
        userlist:[],
        school_id:'',
      }
   },
   methods:{
      async getUserList(){
            let res = await getUserTypeList()
            let id = this.$route.query.id;
            for(let i in res.d){
                if(res.d[i].id==id){
                    res.d[i].isselect = true;
                }else{
                    res.d[i].isselect = false;
                }
            }
            this.userlist = res.d;
      },
      async selectOne(id,school_id,type_id){
            this.$vux.loading.show({
              text: '切换中...'
            });
            let res = await switchPerson(school_id,type_id)
            if(res.c==0){
                this.$vux.loading.hide();
                for(let i in this.userlist){
                    if(this.userlist[i].id==id){
                        this.userlist[i].isselect = true;
                    }else{
                        this.userlist[i].isselect = false;
                    }
                }
            }
      },
      addPerson(){
          let sid = this.$route.query.sid ;
          let _url =window.location.protocol +"//"+ window.location.host ;
          window.location.href =  _url+ "/wx/authorize?state="+_url+"/wx/page/add/role?sid="+sid+"&sid="+sid;
      }
   },
   async created(){
       window.document.title="个人中心"
       let res = await accountDetail();
       if(res.c==0){
           this.school_id=res.d[0].school_id;
       }
       this.getUserList();

   },
   components: {
      HeadTop,
    },
  }

</script>

<style scoped>
.switch-items{margin-top: 1.5rem;}
.switch-items .item{padding: 0.75rem;height: 2.5rem;box-sizing: content-box;position: relative;margin-bottom: 0.75rem;}
.switch-items .item .img-box{width: 2.5rem;height: 2.5rem;position: absolute;left: 0.75rem;top: 0.75rem;border-radius: 50%;overflow: hidden;}
.switch-items .item .img-box img{width: 100%;}
.switch-items .item .item-msg{margin-left: 3rem;height: 100%;}
.switch-items .item .item-msg .item-name{font-size: 0.75rem;color: #444444;margin-top: 0.2rem;}
.switch-items .item .item-msg .item-school{font-size: 0.6rem;color: #888;margin-top: 0.3rem;}
.switch-items .item .item-msg .item-select{position: absolute;right: 0.75rem;top:50%;transform: translateY(-50%);width: 1rem;height: 1rem;}
.switch-items .item .item-msg .item-select.has_select{background: url("../../../images/select.png")no-repeat center;background-size: 100% 100%;}
.bottomButton{  width:7.5rem;  margin:2.5rem auto;height: 2rem;  line-height: 2rem;  text-align: center;  background-color: #4685ff;  color:#fff;  font-size: 0.75rem;  -webkit-border-radius: 1rem;  -moz-border-radius: 1rem;  -ms-border-radius: 1rem;  -o-border-radius: 1rem;  border-radius: 1rem;}
</style>
