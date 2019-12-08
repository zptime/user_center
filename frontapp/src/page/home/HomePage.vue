<template>
  <div class="contentBox" v-cloak>
    <!--<div class="headView">-->
      <!--<span :style="{flex:'1'}"></span>-->
      <!--<img class="headImgView" src="../../images/icon_jiaXiaoHuDong.png"/>-->
      <!--<span :style="{flex:'1'}"></span>-->
    <!--</div>-->
    <div class="content" v-for="item in showData">
      <div>
        <divider class="dividerLine" v-if="isTeacher != -1 && isTeacher">{{item.server_title}}</divider>
      </div>
      <div class="modualItems">
        <grid :cols="3"  :show-lr-borders="false" :show-vertical-dividers="false">
          <grid-item class="itemInModual" v-for="(subItem,index) in item.moduals" :key="index" >
            <div class="itemContent" @click="clickItem(subItem)">
              <span :style="{color:'#fafafa'}"><br></span>
              <img :src="subItem.app_icon"/>
              <span class="itemName">{{subItem.app_name}}</span>
            </div>
          </grid-item>
        </grid>
      </div>
    </div>
  </div>
</template>

<script>
  import Grid from 'vux/src/components/grid/grid.vue'
  import GridItem from 'vux/src/components/grid/grid-item.vue'
  import {accountDetail,wxServiceList} from '../../service/getData.js'
  import Divider from 'vux/src/components/divider/index.vue'
  import {forceConfigSettings} from '../../components/framework/serviceMgr.js'

  export default {
    name: "home-page",
    components: {
      Divider,
      Grid,
      GridItem,
    },
    data() {
      return {
        loading: false,
        html: '',
        itemWidth: 0,
        itemHeight: 0,
        itemSpace: 0.75,//item间距
        lineSapce: 1,//item 行间距
        showData: [],
        getData: [],
        //只判断老师 家长
        isTeacher: -1,
        head: {
          icon: 'return',
          title: '互动系统',
          more: false
        },
      }
    },
    methods: {
      clickItem(subItem) {
        let url = subItem.app_url;
        url  = subItem.app_url + '&myCustomId='+ Date.parse(new Date());
        //跳转对应的界面
        window.location.href = url;
      },
      //判断设备
      ////deviceType :1表示android, 2表示IOS,-1其他
      jundleDevice() {
        var u = navigator.userAgent;
        var isAndroid = u.indexOf('Android') > -1 || u.indexOf('Adr') > -1; //android终端
        var isiOS = !!u.match(/\(i[^;]+;( U;)? CPU.+Mac OS X/); //ios终端

        if (isAndroid) {
          return 'android'
        }
        if (isiOS) {
          return 'ios'
        }
        return 'unknown'
      },
      async wxServiceList() {
        let res = await wxServiceList();
        if (res.c == 0) {
          //app_url需要特殊处理，添加以下字段
          //from (为hxApp, weixin)
          //deviceType :android, ios
          let device = this.jundleDevice();
          let urlParam = "&from=weixin&deviceType=" + device;
          //url后面添加参数
          for (let i = 0; i < res.d.length; i++) {
            let obj = res.d[i];
            let key = Object.keys(obj)[0];
            let arr = obj[key];
            for (let j = 0; j < arr.length; j++) {
              let subItem = arr[j];
              subItem.app_url += urlParam;
            }
          }
          this.getData = res.d;
          this.dealData();
        } else {
          this.$vux.toast.show({
            type: 'text',
            text: res.m
          })
        }
      },

      async accountDetail() {
        let res = await accountDetail();
        if (res.c == 0) {
          let type_id = res.d[0].type_id;
          if (!type_id) return;
          //1 学生 2 老师 4 家长
          if (2 == type_id) {
            this.isTeacher = true;
          } else if (4 == type_id) {
            this.isTeacher = false;
          } else {
            //身份不对
            this.isTeacher = -1;
          }
          this.dealData();
        } else {
          this.$vux.toast.show({
            type: 'text',
            text: res.m
          })
        }
      },
      //处理数据
      dealData() {
        if (this.isTeacher == -1 || this.getData.length == 0) {
          return;
        }
        let arr = [];
        //老师情况
        if (this.isTeacher == true){
          for (let i = 0; i < this.getData.length; i++) {
            let changeObj = {};

            let obj = this.getData[i];
            let title = Object.keys(obj)[0];

            changeObj.server_title = title;
            changeObj.moduals = obj[title];

            arr.push(changeObj);
            /*
            * {
            *   server_title:'',
            *   moduals:[
            *       {
            *       "app_url": "http://test-blog.hbeducloud.com:8088/",  //微信无法访问8088
                    "app_name": "班级博客",
                    "app_icon": "http://test-usercenter.hbeducloud.com:8088/school_center_dev/1/f43415be28ab48d0b8912225fe9731af.png"
            *       }
            *   ]
            *
            * }
            *
            * */
          }
        }else{
          //家长情况
         let obj = {};
         obj.server_title = '家长';
         obj.moduals = [];
         for (let j =0;j<this.getData.length;j++){
           let severData = this.getData[j];
           let title = Object.keys(severData)[0];
           let severArr = severData[title];
           obj.moduals = obj.moduals.concat(severArr);
         }
         arr.push(obj);
        }
        this.showData = arr;
      },
      initData() {
        this.accountDetail();
        this.wxServiceList();
      },
    },
    beforeRouteEnter(to,from,next){
      var url = location.search; //
      var request = new Object();
      if (url.indexOf("?") == -1) {
        window.location.href=window.location.href+ '?myCustomId='+Date.parse(new Date());
      }else{
        let myUrl = window.location.href.split('?')[0];
        let strs = [];
        var str = url.substr(1);
        strs = str.split("&");
        for(var i = 0; i < strs.length; i ++) {
          request[strs[i].split("=")[0]]=unescape(strs[i].split("=")[1]);
        }
        if (!request.myCustomId){

          window.location.href=myUrl+ '?myCustomId='+Date.parse(new Date());
        }else{
          let timeScape = parseInt(request.myCustomId);
          let culTimeScape = Date.parse(new Date());
          if (culTimeScape > timeScape + 10000){
            window.location.href=myUrl+ '?myCustomId='+Date.parse(new Date());
          }
        }
      }

      next();
    },
    created() {
      //forceSetSignUrl(this);
      forceConfigSettings(this);
      this.initData();
    },
  }
</script>

<style scoped>
  .dividerLine {width: 40%;margin-left: 30%;font-size: 0.75rem;margin-top: 1.5rem;color: #444444;font-weight: 700;}
  .headView {display: flex;flex-flow:row;position: relative;margin-top:1.5rem;}
  .headImgView{width:225px;height: 60px;}
  .modualItems {top:1rem;width: 100%;}
  .modualItems .itemInModual {margin-top: 0.5rem;}
  .itemContent {display: flex;flex-flow: column;background-color: #fafafa;padding-bottom: 0.5rem;}
  .itemContent img{height: 2.5rem;width: 2.5rem;margin-left: 1.5rem;}
  .itemContent span {flex: 1;text-align: center;color: #444444;display: inline-block; overflow: hidden;
    text-overflow: ellipsis; font-size: 0.6rem;white-space: nowrap;font-weight: 700;}
  .itemContent .itemName{margin-top: 0.75rem;}

  .weui-grids:before{border-top:none;}
  .weui-grid:after{border-bottom:none;}

  .contentBox {top:0;}

</style>
