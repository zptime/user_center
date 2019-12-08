<template>
  <div>
    <head-top :head="head"></head-top>
    <div style="padding: 2.1rem 0.75rem 0;">
        <div class="p-top">
            <div class="left-box">
                <div class="item-name"  :class="{ font6: (detail.full_name.length==5 || detail.full_name.length==6),'font8': (detail.full_name.length==7 || detail.full_name.length==7) }"  >{{ detail.full_name }} - {{ detail.title }}</div>
                <div class="item-msg">{{ detail.school_name_full }}</div>
            </div>
            <!--div class="right-imgbox"  @click=" show=true" ><img :src="detail.image_url" v-if="detail.image_url!=''" alt=""> <img src="../../../images/icon-default-avatar.png" v-if="detail.image_url==''" alt="">  </div-->
          <m-image-upload class="right-imgbox" :imgStyle="mystyle" :srcUrl="detail.image_url" @on-upload-complete="uploadComplete"></m-image-upload>
        </div>
        <div>
            <group  label-width="5.5em" label-margin-right="2em" >
                <popup-radio title="性别" :options="sexs" v-model="sex" placeholder="请选择"   ></popup-radio>
                <datetime title="生日" v-model="time" value-text-align="right"  placeholder="请选择"  min-year=1950  max-year=2018 ></datetime>
                <cell title="学校" :value="detail.school_name_full" value-text-align="left"></cell>
                <cell title="班级" value="hello" value-text-align="left">
                    <div class="classbox" :class="{ active : classdetail }">
                        <div class="item" >{{ classList }}</div>
                        <div class="item-oper"  @click="classdetail = !classdetail" >{{ classdetail ? '收起' :  '详情' }}</div>
                    </div>
                </cell>
                <cell title="科目" value="hello" value-text-align="left">
                    <div class="subbox" :class="{ active : subdetail }">
                        <div class="item"  >{{ subList }}</div>
                        <div class="item-oper" @click="subdetail = !subdetail">{{ subdetail ? '收起' :  '详情' }}</div>
                    </div>
                </cell>
            </group>

        </div>
    </div>
    <div v-transfer-dom>
        <actionsheet v-model="show" :menus="menus" @on-click-menu="changeImg" :close-on-clicking-mask="true" :close-on-clicking-menu="true">
        </actionsheet>
    </div>
  </div>
</template>

<script type="text/ecmascript-6">
  import HeadTop from '@/components/Head.vue'
  import { TransferDomDirective as TransferDom,Group, Cell, Datetime,PopupRadio,Actionsheet } from 'vux'
  import { getDetaiInfor,accountDetail,updateTeacherInfo ,getSchoolClasses,getTeachSub } from '../../../service/getData.js'
  import MImageUpload from "../../../components/m-img/imageUpload.vue";

  export default {
    directives: {
        TransferDom
    },
    data () {
      return {
        //native_image:{},
        mystyle : 'width:100%',
        head:{
          icon: 'return',
          title: '个人信息',
          more: false
        },
        detail:{},
        time:'',
        teacher_id:'',
        account_id:'',
        sexs:["男","女"],
        sex:'',
        ischange:false,
        classdetail:false,
        subdetail:false,
        classList:'',
        subList:'',
        show:false,
        menus:{
          menu1:'相册',
          menu2:'拍照',
        },
        original_image_url:'',
      }
   },
    methods:{
      uploadComplete(imgObj) {
          this.original_image_url = imgObj.original_image_url;
          this.detail.image_url = imgObj.original_image_url;
          let _teacher_info = {
              id:this.teacher_id,
              image_url:this.original_image_url
          };
          let teacher_info = JSON.stringify(_teacher_info)
          updateTeacherInfo(this.account_id,teacher_info);
      },
      changeImg(val){
        if(val=="menu1"){

        }else if(val=="menu2"){

        }
      },
      async getAccountDetail(){
          let res = await accountDetail();
          let teacher_id = res.d[0].id;
          let account_id = res.d[0].account_id;
          this.account_id = account_id;
          let resdetail = await getDetaiInfor(teacher_id,account_id);
          this.detail = resdetail.d[0];
          this.sex = this.detail.sex;
          this.time = this.detail.birthday;
          this.teacher_id = this.detail.id;
      },
      async getTeacherInfor(){
            let res = await getDetaiInfor();
            if(res.c==0){

            }
      },
      async getteacherClass(){
          let res = await getSchoolClasses('',1);
          if(res.c==0){
              let str = '';
              for(let i in res.d){
                  if(res.d[i].is_teach==1){
                      str+=res.d[i].class_name + "   "
                  }
              }
              this.classList = str;
          }
      },
      async getTeachSub(){
          let res = await getTeachSub();
          if(res.c==0){
              let arr = [];
              for(let i in res.d){
                  let subject_name = res.d[i].subject_name;
                  let isRepeat = false;
                  for(let j in arr){
                      if(arr[j]==subject_name){
                          isRepeat=true
                          break;
                      }
                  }
                  if(!isRepeat){
                      arr.push(subject_name)
                  }
              }
              this.subList = arr.join("  ");
          }
      }
   },
   watch:{
       sex(val,oldval){
           this.ischange = true ;
       },
       time(val,oldval){
           this.ischange = true ;
           this.time = val;
       }
   },
   async destroyed(){
       if(this.ischange){
           let _teacher_info = {
               id:this.teacher_id,
               sex:this.sex,
               birthday:this.time,
               image_url:this.original_image_url
           };
           let teacher_info = JSON.stringify(_teacher_info)
           let res = await updateTeacherInfo(this.account_id,teacher_info);
       }
   },
   created(){
       this.getAccountDetail();
       this.getteacherClass();
       this.getTeachSub();
       window.document.title="个人中心"
   },
    components: {
      MImageUpload,
      HeadTop,
      Group,
      Cell,
      Datetime,
      PopupRadio,
      Actionsheet
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

.classbox{text-align: left;padding-right: 2rem;position: relative;transform: translateX(0rem);width: 10rem;height: 1.2rem;overflow: hidden;min-height: 1.2rem;}
.classbox .item-oper{position: absolute;top: 0rem;right: 0rem;color: #3f80ff;}
.classbox.active{height: inherit}
.subbox{text-align: left;padding-right: 2rem;position: relative;transform: translateX(0rem);width: 10rem;height: 1.2rem;overflow: hidden;min-height: 1.2rem;}
.subbox .item-oper{position: absolute;top: 0rem;right: 0rem;color: #3f80ff;}
.subbox.active{height: inherit}

</style>
