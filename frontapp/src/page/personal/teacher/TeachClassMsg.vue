
<!--任教设置班级二维码界面-->

<template>
  <div>
    <head-top :head="head"></head-top>
    <div style="padding: 3.6rem 0.75rem 0;">
      <p class="tipTextView">{{getSchoolTxt}}</p>
      <p class="tipTextView">扫码二维码注册成为班级学生家长</p>
      <div class="qrbox" ref="showQrcode">
      </div>
    </div>
  </div>
</template>

<script type="text/ecmascript-6">
  import HeadTop from '@/components/Head.vue'
  import { TransferDomDirective as TransferDom  } from 'vux'
  import {getSchoolDetail,getClassQrcode ,getSchoolQrcode } from '@/service/getData.js'

  export default {
    directives: {
      TransferDom
    },
    data () {
      return {
        base64ImgData:'',
        classObj:{},//班级信息
        schoolData:{},
        head:{
          icon: 'return',
          title: '班级二维码',
          more: false
        },
        name:'',
        code:'',
      }
    },
    methods:{
      getQrcoed(){

      },
      async getSchoolQrcode(){
        let res = await  getSchoolQrcode(this.schoolData.id);
        if (res.c == 0){
          this.base64ImgData = res.d.parentbind_base64_image;
          let fatherDiv = this.$refs.showQrcode;
          let img = document.createElement('img');
          img.src = 'data:image/png;base64,' + this.base64ImgData;
          img.style='width:100%';
          fatherDiv.appendChild(img);
        }else{
          this.$vux.toast.show({
            type: 'text',
            text: res.m
          })
        }
      },
      async getSchoolDetail(){
        let res = await getSchoolDetail();
        if (res.c == 0){
            this.schoolData = res.d[0];
        }else{
          this.$vux.toast.show({
            type: 'text',
            text: res.m
          })
        }

      }
    },
    computed:{
      getImg(){
        let str = 'data:image/jpeg;base64,' + this.base64ImgData;
        return str;
      },
      getSchoolTxt(){
        if(this.schoolData.name_full){
          let str = this.schoolData.name_full + ' - ' + this.classObj.class_name;
          return str;
        }
        return this.classObj.class_name;
      },
    },
    async created(){
      let str = this.$route.params.classObj;
      this.classObj = JSON.parse(str);
      console.log(this.classObj)
      let res = await this.getSchoolDetail();
      this.getSchoolQrcode();
    },
    components: {
      HeadTop,
    },
  }

</script>

<style scoped>
  .qrbox{line-height: 10rem;text-align: center;border: solid 1px #eee;width: 10rem;margin: 2rem auto;height: 10rem;overflow: hidden;}
  .tipTextView {width: 100%;font-size: 0.9rem;height: 1rem;line-height: 1rem;overflow: hidden;text-align: center;color: #444444;}
</style>
