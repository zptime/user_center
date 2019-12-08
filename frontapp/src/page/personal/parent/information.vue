<template>
  <div>
    <head-top :head="head"></head-top>
    <div style="padding: 2.1rem 0.75rem 0;">
        <div class="p-top">
            <div class="left-box">
                <div class="item-name" :class="{ font6: (detail.full_name.length==5 || detail.full_name.length==6),'font8': (detail.full_name.length==7 || detail.full_name.length==7) }">{{ detail.full_name }} - 家长 </div>
                <div class="item-msg">{{ relation }}</div>
            </div>
            <div class="right-imgbox"><img :src="detail.image_url" v-if="detail.image_url!=''" alt=""> <img src="../../../images/icon-default-avatar.png" v-if="detail.image_url==''" alt=""> </div>
        </div>
        <div>
            <group  label-width="5.5em" label-margin-right="2em">
                <popup-radio title="性别" :options="sexs" v-model="sex" placeholder="请选择"   ></popup-radio>
                <datetime title="生日" v-model="time" value-text-align="right"  placeholder="请选择" min-year=1950  max-year=2018  ></datetime>
                <x-address title="籍贯" v-model="addressValue" raw-value :list="addressData" value-text-align="right" label-align="justify" placeholder="请选择"     ></x-address>
            </group>
        </div>
    </div>
  </div>
</template>

<script type="text/ecmascript-6">
  import HeadTop from '@/components/Head.vue'
  import { TransferDomDirective as TransferDom,Group, Cell, Datetime,ChinaAddressData, XAddress,PopupRadio } from 'vux'
  import { accountDetail,getParentDetaiInfor,updateParentInfo } from '../../../service/getData.js'

  export default {
    directives: {
        TransferDom
    },
    data () {
      return {
        head:{
          icon: 'return',
          title: '个人信息',
          more: false
        },
        detail:{},
        time:'',
        parent_id:'',
        account_id:'',
        addressData: ChinaAddressData,
        addressValue: ['', '', ''],
        sexs:["男","女"],
        sex:'',
        ischange:false,
        relation:'',
      }

   },
   methods:{
      async getAccountDetail(){
          let res = await accountDetail();
 //         this.detail = res.d[0];
          let parent_id = res.d[0].id;
          let account_id = res.d[0].account_id;
          this.account_id = account_id;
          let resdetail = await getParentDetaiInfor(parent_id,account_id);
          this.detail = resdetail.d[0];
          this.sex = this.detail.sex;
          if(this.detail.address!=''){
              this.addressValue = this.detail.address.split(" ");
          }
          this.time = this.detail.native_place;
          this.parent_id = this.detail.id;
          for(let i in this.detail.children){
              let relation = this.detail.children[i].relation;
              if(relation==''){
                  relation='家长'
              }
            this.relation+=this.detail.children[i].student_full_name+relation +'  '
          }
      },
      async getTeacherInfor(){
            let res = await getParentDetaiInfor();
      }
   },
   watch:{
       sex(val,oldval){
           console.log(val)
           this.ischange = true ;
       },
       addressValue(val,oldval){
           this.ischange = true ;

       },
       time(val,oldval){
           this.ischange = true ;
           this.time = val;
       }
   },
   async destroyed(){
       if(this.ischange){
           let addstr = '';
           let p = this.addressValue[0];
           let s = this.addressValue[1];
           let x = this.addressValue[2];
            for(let i in ChinaAddressData){
                if(ChinaAddressData[i].value==p){
                    p = ChinaAddressData[i].name;
                };
                if(ChinaAddressData[i].value==s){
                    s = ChinaAddressData[i].name;
                };
                if(ChinaAddressData[i].value==x){
                    x = ChinaAddressData[i].name;
                };
            }
           addstr = p +" "+ s +" "+ x;
           let _parent_info =  {
               id:this.parent_id,
               sex:this.sex,
               native_place:this.time,
               address:addstr,
           };
           let parent_info = JSON.stringify(_parent_info)
           let res = await updateParentInfo(this.account_id,parent_info);
       }
   },
   created(){
       window.document.title="个人中心"
       this.getAccountDetail();
   },
    components: {
      HeadTop,
      Group,
      Cell,
      Datetime,
      ChinaAddressData,
      XAddress,
      PopupRadio
    },
  }

</script>

<style scoped>
.p-top{height: 3.75rem;margin-top: 1.5rem;position: relative;}
.p-top .left-box{width: 10.5rem;height:100%;}
.p-top .item-name{color: #444444;font-size: 1.5rem;text-align: center;line-height: 1;}
.p-top .item-name.font6{font-size: 1.2rem;}
.p-top .item-name.font8{font-size: 1rem;}
.p-top .item-msg{height: 1.5rem;color: #888888;font-size: 0.75rem;width: 100%;background: #f5f5f5;border-radius: 0.75rem;line-height: 1.5rem;text-align: center;}
.p-top .right-imgbox{position: absolute;right: 0;top: 0;width: 3.75rem;height: 3.75rem;box-sizing: border-box;border: solid 0.125rem #FFFFFF;border-radius: 50%;box-shadow: 0 0 0.15rem rgba(0,0,0,0.2);overflow: hidden;}
.p-top .right-imgbox img{width: 100%;}


.switch-items{margin-top: 1.5rem;}
.switch-items .item{padding: 0.75rem;height: 2.5rem;box-sizing: content-box;position: relative;margin-bottom: 0.75rem;}
.switch-items .item .img-box{width: 2.5rem;height: 2.5rem;position: absolute;left: 0.75rem;top: 0.75rem;border-radius: 50%;}
.switch-items .item .item-msg{margin-left: 3rem;height: 100%;}
.switch-items .item .item-msg .item-name{font-size: 0.75rem;color: #444444;margin-top: 0.2rem;}
.switch-items .item .item-msg .item-school{font-size: 0.6rem;color: #888;margin-top: 0.3rem;}
.switch-items .item .item-msg .item-select{position: absolute;right: 0;top:50%;transform: translateY(-50%)}
.bottomButton{  width:7.5rem;  margin:2.5rem auto;height: 2rem;  line-height: 2rem;  text-align: center;  background-color: #4685ff;  color:#fff;  font-size: 0.75rem;  -webkit-border-radius: 1rem;  -moz-border-radius: 1rem;  -ms-border-radius: 1rem;  -o-border-radius: 1rem;  border-radius: 1rem;}
</style>
