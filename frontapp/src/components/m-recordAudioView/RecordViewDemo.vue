<!--<template>-->
  <!--<div>-->
    <!--<div ref="mainView" class="Login" :style="{overflow:'scroll'}">-->
      <!--&lt;!&ndash;<input v-model="username" placeholder="用户名">&ndash;&gt;-->
      <!--&lt;!&ndash;<input v-model="password" type="password" placeholder="密码">&ndash;&gt;-->
      <!--&lt;!&ndash;<div>&ndash;&gt;-->
      <!--&lt;!&ndash;<button @click="testLogin" class="weui_btn weui_btn_primary">登录</button>&ndash;&gt;-->
      <!--&lt;!&ndash;</div>&ndash;&gt;-->
      <!--<div>-->
        <!--<button @click="getJSApiTicket" class="weui_btn weui_btn_primary">获取ticket</button>-->
      <!--</div>-->
      <!--&lt;!&ndash;<div>&ndash;&gt;-->
      <!--&lt;!&ndash;<button @click="choosePic" class="weui_btn weui_btn_primary">选择图片</button>&ndash;&gt;-->
      <!--&lt;!&ndash;</div>&ndash;&gt;-->
      <!--<div>-->
        <!--<button @click="showRecordView" class="weui_btn weui_btn_primary">录制音频</button>-->
      <!--</div>-->
      <!--&lt;!&ndash;<div>&ndash;&gt;-->
      <!--&lt;!&ndash;<button @click="uploadAudio" class="weui_btn weui_btn_primary">上传音频</button>&ndash;&gt;-->
      <!--&lt;!&ndash;</div>&ndash;&gt;-->
      <!--&lt;!&ndash;<div>&ndash;&gt;-->
      <!--&lt;!&ndash;<button @click="playAudio" class="weui_btn weui_btn_primary">播放音频</button>&ndash;&gt;-->
      <!--&lt;!&ndash;</div>&ndash;&gt;-->
      <!--&lt;!&ndash;<div>&ndash;&gt;-->
      <!--&lt;!&ndash;<button @click="downloadVoice" class="weui_btn weui_btn_primary">下载音频</button>&ndash;&gt;-->
      <!--&lt;!&ndash;</div>&ndash;&gt;-->
      <!--&lt;!&ndash;<div>&ndash;&gt;-->
      <!--&lt;!&ndash;<button @click="scanCode" class="weui_btn weui_btn_primary">扫描二维码</button>&ndash;&gt;-->
      <!--&lt;!&ndash;</div>&ndash;&gt;-->
      <!--&lt;!&ndash;<div>&ndash;&gt;-->
      <!--&lt;!&ndash;<button @click="lookLocation" class="weui_btn weui_btn_primary">查看地理位置</button>&ndash;&gt;-->
      <!--&lt;!&ndash;</div>&ndash;&gt;-->
      <!--&lt;!&ndash;<div>&ndash;&gt;-->
      <!--&lt;!&ndash;<button @click="getLocation" class="weui_btn weui_btn_primary">定位地理位置</button>&ndash;&gt;-->
      <!--&lt;!&ndash;</div>&ndash;&gt;-->
      <!--&lt;!&ndash;<div ref="callBacFuc">&ndash;&gt;-->
      <!--&lt;!&ndash;<span>测试</span>&ndash;&gt;-->
      <!--&lt;!&ndash;<input type="file" style="/* visibility: hidden */" capture="camera" accept="image/*,video/*" name="" value="" v-on:input ="inputFunc">&ndash;&gt;-->
      <!--&lt;!&ndash;</div>&ndash;&gt;-->
      <!--&lt;!&ndash;<img ref="myImg" :style="{width:'100px',height:'100px'}" :src="imgId" alt="lalla"/>&ndash;&gt;-->
    <!--</div>-->
    <!--<popup v-model="needRecordAudio" height="12.5rem" @on-hide="popupHide" is-transparent >-->
      <!--<recordView ref="audioView" @on-startRecord="startRecrod" @on-stopRecord="stopRecord" @on-makeSure="makeSure" @on-cancleClick="cancelClick"></recordView>-->
    <!--</popup>-->
  <!--</div>-->
<!--</template>-->

<!--<script type="text/ecmascript-6">-->
    <!--import {mapState, mapMutations } from 'vuex'-->
    <!--import {testLogin,exchangeLocation} from '../service/getData'-->
    <!--import wx from 'weixin-js-sdk'-->
    <!--import recordView from '../components/m-recordAudioView/index.vue'-->
    <!--import popup from 'vux/src/components/popup/index.vue'-->

    <!--export default ({-->
        <!--components:{-->
          <!--recordView,-->
          <!--popup-->
        <!--},-->
        <!--mounted(){-->
            <!--this.$refs.mainView.style.height = window.innerHeight + 'px';-->
        <!--},-->
        <!--data (){-->
            <!--return {-->
                <!--needRecordAudio:false,-->
                <!--longitude:'',-->
                <!--latitude:'',-->
                <!--tencentMapKey:'2VABZ-C2IW6-4MJSK-M2LJU-3O5DO-7YBW5', //其他标准gps定位转腾讯地图坐标key-->
                <!--locationMsg:{},-->
                <!--audioSeverId:'',-->
                <!--isPlayingAudio:'',-->
                <!--uploadedAudioId:'',-->
                <!--recordId:'',-->
                <!--isRecording:false,-->
                <!--imgId:undefined,-->


                <!--signature:'4c9c6e5062d2011ffe81736389b64d84dbb5e797',-->
                <!--timestamp:1528524350,-->
                <!--url:'http://3ybpvc.natappfree.cc/test/testLogin',-->
                <!--noncestr:'haoxiangkeyile',-->
                <!--jsapiTicket:'HoagFKDcsGMVCIY2vOjf9lbBrbaz9cgfnnbyQNX1xunJz8MfE_429Pkp56Vq-XuZ5wOwUM4o6j9ZkwYekcdIbA',-->
                <!--accessToken:'10_cE6TUXwG4ZgbCzB1UQ-tsmEadjW_7TbQKJ6A4NibPKZjGbeNLQnerBJ7KMusND8gsAeYkIAxEBGwwHVxDu49ZK6sa9fjVYIS9SzNYtNjC_I-1mc6f8SIxxjIL4cOMRcAEAUSX',-->
                <!--username: 'fenghuo',-->
                <!--password: 'fhuo_03'-->
            <!--}-->
        <!--},-->

        <!--methods: {-->
            <!--...mapMutations([-->
                <!--'ACCOUNT'-->
            <!--]),-->
          <!--//获取环信jssdk的ticket-->
            <!--getJSApiTicket(){-->
              <!--wx.config({-->
                <!--debug: true, // 开启调试模式,调用的所有api的返回值会在客户端alert出来，若要查看传入的参数，可以在pc端打开，参数信息会通过log打出，仅在pc端时才会打印。-->
                <!--appId: 'wxae466e947e16931c', // 必填，公众号的唯一标识-->
                <!--timestamp:this.timestamp , // 必填，生成签名的时间戳-->
                <!--nonceStr: this.noncestr, // 必填，生成签名的随机串-->
                <!--signature: this.signature,// 必填，签名-->
                <!--jsApiList: ['chooseImage','getLocalImgData','startRecord','stopRecord','onVoiceRecordEnd','uploadVoice','playVoice','pauseVoice','onVoicePlayEnd','scanQRCode','openLocation','getLocation','downloadVoice'] // 必填，需要使用的JS接口列表-->
              <!--});-->
            <!--},-->
            <!--//初始化获取数据-->
            <!--async testLogin(){-->
                <!--//获取 choice 列表-->
                <!--let res = await testLogin( this.username , this.password);-->
                <!--if (res.c == 0){-->
                    <!--this.ACCOUNT({name:this.username});-->
                    <!--window.NonetestLogin = false;-->
                    <!--this.$router.push('/m')-->
                <!--}else{-->
                    <!--alert(res.m);-->
                <!--}-->
            <!--},-->
          <!--inputFunc(data){-->

              <!--if(data){-->
                <!--this.$refs.callBackFuc.style.backgroundColor=RGB(100,0,0);-->
              <!--}else{-->
                <!--this.$refs.callBackFuc.style.backgroundColor=RGB(0,100,0);-->
              <!--}-->
          <!--},-->
          <!--//显示录音视图-->
          <!--showRecordView(){-->
            <!--this.needRecordAudio = true;-->
          <!--},-->
          <!--//录制音频-->
          <!--recordAudio(start){-->
            <!--var _self = this;-->
            <!--if(start){-->
              <!--wx.startRecord();-->
            <!--}else{-->
              <!--wx.stopRecord({-->
                <!--success: function (res) {-->
                  <!--var localId = res.localId;-->
                  <!--_self.recordId = localId;-->
                <!--}-->
              <!--});-->
            <!--}-->
            <!--wx.onVoiceRecordEnd({-->
              <!--//录音时间超过一分钟没有停止的时候会执行 complete 回调-->
              <!--complete: function (res) {-->
                <!--var localId = res.localId;-->
                <!--_self.recordId = localId;-->
                <!--_self.needRecordAudio = false;-->
              <!--}-->
            <!--});-->
          <!--},-->
          <!--//上传音频-->
          <!--uploadAudio(){-->
            <!--var _self = this;-->
            <!--wx.uploadVoice({-->
              <!--localId: _self.recordId, // 需要上传的音频的本地ID，由stopRecord接口获得-->
              <!--isShowProgressTips: 1, // 默认为1，显示进度提示-->
              <!--success: function (res) {-->
                <!--var serverId = res.serverId; // 返回音频的服务器端ID-->
                <!--_self.uploadedAudioId = serverId;-->
                <!--_self.needRecordAudio = false;-->
              <!--}-->
            <!--});-->
          <!--},-->
          <!--//播放音频-->
          <!--playAudio(){-->
             <!--this.isPlayingAudio = !this.isPlayingAudio;-->
             <!--var _self = this;-->
             <!--if(this.isPlayingAudio){-->
               <!--wx.playVoice({-->
                 <!--localId: _self.recordId // 需要播放的音频的本地ID，由stopRecord接口获得-->
               <!--});-->
             <!--}else{-->
               <!--wx.pauseVoice({-->
                 <!--localId: _self.recordId // 需要暂停的音频的本地ID，由stopRecord接口获得-->
               <!--});-->
             <!--}-->

            <!--// wx.stopVoice({-->
            <!--//   localId: '' // 需要停止的音频的本地ID，由stopRecord接口获得-->
            <!--// });-->

            <!--wx.onVoicePlayEnd({-->
              <!--success: function (res) {-->
                <!--var localId = res.localId; // 返回音频的本地ID-->
              <!--}-->
            <!--});-->

          <!--},-->
          <!--//下载音频-->
          <!--downloadVoice(){-->
            <!--var _self = this;-->
            <!--wx.downloadVoice({-->
              <!--serverId:_self.uploadedAudioId , // 需要下载的音频的服务器端ID，由uploadVoice接口获得-->
              <!--isShowProgressTips: 1, // 默认为1，显示进度提示-->
              <!--success: function (res) {-->
                <!--var localId = res.localId; // 返回音频的本地ID-->
              <!--}-->
            <!--});-->
          <!--},-->
          <!--//开始录音-->
          <!--startRecrod(){-->
              <!--this.recordAudio(true);-->
          <!--},-->
          <!--//结束录音-->
          <!--stopRecord(){-->
            <!--this.recordAudio(false);-->
          <!--},-->
          <!--//录音视图 确认按钮点击-->
          <!--//time是录音时间-->
          <!--makeSure(time){-->
             <!--this.uploadAudio();-->
          <!--},-->
          <!--//录音视图 取消按钮点击-->
          <!--cancelClick(){-->
             <!--this.needRecordAudio = false;-->
          <!--},-->
          <!--//录音视图 点击遮罩关闭-->
          <!--popupHide(){-->
            <!--this.stopRecord();-->
            <!--this.$refs.audioView.stopRecordBySuper();-->
          <!--},-->
          <!--//选择本地图片和显示-->
          <!--choosePic(){-->
            <!--var _self = this;-->
            <!--wx.chooseImage({-->
              <!--count: 1, // 默认9-->
              <!--sizeType: ['original', 'compressed'], // 可以指定是原图还是压缩图，默认二者都有-->
              <!--sourceType: ['album', 'camera'], // 可以指定来源是相册还是相机，默认二者都有-->
              <!--success: function (res) {-->
                <!--var localIds = res.localIds; // 返回选定照片的本地ID列表，localId可以作为img标签的src属性显示图片-->

                <!--wx.getLocalImgData({-->
                  <!--localId: localIds[0], // 图片的localID-->
                  <!--success: function (res) {-->
                    <!--var localData = res.localData; // localData是图片的base64数据，可以用img标签显示-->
                    <!--_self.imgId = localData-->
                  <!--}-->
                <!--});-->

              <!--}-->
            <!--});-->
          <!--},-->

          <!--//扫描一维码，二维码-->
          <!--scanCode(){-->
            <!--wx.scanQRCode({-->
              <!--needResult: 1, // 默认为0，扫描结果由微信处理，1则直接返回扫描结果，-->
              <!--scanType: ["qrCode","barCode"], // 可以指定扫二维码还是一维码，默认二者都有-->
              <!--success: function (res) {-->
                <!--var result = res.resultStr; // 当needResult 为 1 时，扫码返回的结果-->
              <!--}-->
            <!--});-->
          <!--},-->
          <!--//查看地理位置-->
          <!--lookLocation(){-->
            <!--var _self = this;-->
            <!--wx.openLocation({-->
              <!--latitude: _self.locationMsg.latitude, // 纬度，浮点数，范围为90 ~ -90-->
              <!--longitude:_self.locationMsg.longitude, // 经度，浮点数，范围为180 ~ -180。-->
              <!--name: '不知道', // 位置名-->
              <!--address: '湖北省武汉市武昌区', // 地址详情说明-->
              <!--scale: 20, // 地图缩放级别,整形值,范围从1~28。默认为最大-->
              <!--infoUrl: '' // 在查看位置界面底部显示的超链接,可点击跳转-->
            <!--});-->
          <!--},-->
          <!--//获取地理位位置信息-->
          <!--getLocation(){-->
            <!--var _self = this;-->
            <!--wx.getLocation({-->
              <!--type: 'gcj02', // 默认为wgs84的gps坐标，如果要返回直接给openLocation用的火星坐标，可传入'gcj02'-->
              <!--success: function (res) {-->
                <!--var latitude = res.latitude; // 纬度，浮点数，范围为90 ~ -90-->
                <!--var longitude = res.longitude; // 经度，浮点数，范围为180 ~ -180。-->
                <!--var speed = res.speed; // 速度，以米/每秒计-->
                <!--var accuracy = res.accuracy; // 位置精度-->

                <!--_self.locationMsg.latitude=latitude;-->
                <!--_self.locationMsg.longitude=longitude;-->
                <!--_self.locationMsg.speed=speed;-->
                <!--_self.locationMsg.accuracy=accuracy;-->

                <!--_self.exchangeLocation();-->

              <!--}-->
            <!--});-->
          <!--},-->
          <!--async exchangeLocation(){-->

            <!--var _self = this;-->
            <!--let locations= this.locationMsg.latitude + ',' + this.locationMsg.longitude;-->
            <!--debugger-->
            <!--let res = await exchangeLocation(locations,'1',this.tencentMapKey);-->
            <!--debugger-->
            <!--if(res.status ==0){-->
              <!--let locationObj = res.locations[0];-->
              <!--this.latitude = locationObj.split(',')[0];-->
              <!--this.longitude = locationObj.split(',')[1];-->
              <!--wx.openLocation({-->
                <!--latitude: _self.latitude, // 纬度，浮点数，范围为90 ~ -90-->
                <!--longitude:_self.longitude, // 经度，浮点数，范围为180 ~ -180。-->
                <!--name: '不知道', // 位置名-->
                <!--address: '湖北省武汉市武昌区', // 地址详情说明-->
                <!--scale: 20, // 地图缩放级别,整形值,范围从1~28。默认为最大-->
                <!--infoUrl: '' // 在查看位置界面底部显示的超链接,可点击跳转-->
              <!--});-->
            <!--}-->
          <!--},-->
        <!--}-->

    <!--})-->
<!--</script>-->

<!--<style>-->
    <!--.Login{-->
        <!--position: fixed;-->

        <!--font-size: 1rem;-->
        <!--color: #9b9b9b;-->
        <!--letter-spacing: 0.05rem;-->
        <!--width: 100%;-->
        <!--text-align: center;-->
    <!--}-->

    <!--.Login input{-->
        <!--height: 2rem;-->
        <!--width: 60%;-->
        <!--margin: 0.5rem auto;-->
        <!--border: 1px solid #9b9b9b;-->
        <!--border-radius: 4px;-->
        <!--padding: 8px;-->
        <!--font-size: 0.7rem;-->
        <!--outline: none;-->
    <!--}-->

    <!--.Login button{-->
        <!--width: 60%;-->
        <!--height: 2rem;-->
        <!--margin: 1.5rem auto;-->
    <!--}-->

<!--</style>-->
