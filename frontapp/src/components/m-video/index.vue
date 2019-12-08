<template>
    <span>
       <span @click="popupFile" v-if="popupBtn && nativeVideo.showInNativeApp()" :style="btnSecStyle">
         <slot name="popBtn">
            <div class="pub-video">添加视频</div>
         </slot>
        </span>
        <span @click="popupFile" v-if="popupBtn && !nativeVideo.showInNativeApp()" :style="btnSecStyle">
          <div class="h5-video-view-style">
            <div class="pub-video">添加视频</div>
            <input ref="uVideoFile" type="file" class="h5-video-view-input-style" @change="onSelVideo()"/>
          </div>
        </span>
        <div class="content" :style="contentSecStyle" v-if="videoData">
          <img class="coverImg" :style="getImageStyle" :src="videoData.video_cover_url" v-if="videoData.video_cover_url"/>
          <p class="coverImg fix" :style="getImageStyle" v-else></p>
          <img :class="{playIcon:true,fix:!videoData.video_cover_url}" :style="getPlayIconStyle" @click="playVideo" src="./images/icon-playVideo.png"/>
        </div>
       <div class="content" :style="contentSecStyle" v-else-if="responseVideoData.video_url">
          <img class="coverImg" :style="getImageStyle" :src="responseVideoData.video_cover_url"/>
          <img class="playIcon" :style="getPlayIconStyle" @click="playVideo" src="./images/icon-playVideo.png"/>
          <img class="deleteIcon" @click="deleteVideo" src="./images/icon-delete.png"/>
        </div>
        <video ref="videoObjSetted" :width="coverImgWidth" height="1" controls="false" v-show="false" v-if="videoData && videoData.video_url">
          <source :src="videoData.video_converted_url?videoData.video_converted_url :videoData.video_url" type="video/mp4">
          <source :src="videoData.video_converted_url?videoData.video_converted_url :videoData.video_url" type="video/ogg">
          <source :src="videoData.video_converted_url?videoData.video_converted_url :videoData.video_url" type="video/webm">
          <object :data="videoData.video_converted_url?videoData.video_converted_url :videoData.video_url" :width="coverImgWidth" height="1">
            <embed :src="videoData.video_converted_url?videoData.video_converted_url :videoData.video_url" :width="coverImgWidth" height="1">
          </object>
         </video>
        <video ref="videoChoosed" :width="coverImgWidth" height="1" controls="false" v-show="false" v-else-if="responseVideoData.video_url">
            <source :src="responseVideoData.video_converted_url?responseVideoData.video_converted_url :responseVideoData.video_url" type="video/mp4">
            <source :src="responseVideoData.video_converted_url?responseVideoData.video_converted_url :responseVideoData.video_url" type="video/ogg">
            <source :src="responseVideoData.video_converted_url?responseVideoData.video_converted_url :responseVideoData.video_url" type="video/webm">
            <object :data="responseVideoData.video_converted_url?responseVideoData.video_converted_url :responseVideoData.video_url" :width="coverImgWidth" height="1">
              <embed :src="responseVideoData.video_converted_url?responseVideoData.video_converted_url :responseVideoData.video_url" :width="coverImgWidth" height="1">
            </object>
           </video>
    </span>
</template>

<script>
    import nativeVideo from './nativeVideo.js'
    import webVideo from './webVideo.js'
    import {createVideoMgr} from './VideoMgr'

    export default {
        name: "index",
        props:{
          uploadParms:{
            type:Object,
            default: ()=>{}
          },
          //外界赋值，用于显示，可能为undefined
          videoData:{
            type:Object,
            default: ()=>{}
          },
          showDelete:{
            type:Boolean,
            default: true,
          },
          popupBtn: {
            type: Boolean,
            default: true
          },
          btnSecStyle:{
            type: Object,
            default: () => {}
          },
          contentSecStyle: {
            type: Object,
            default : () => {}
          }
        },
        data(){
          return {
            //选择视频或者拍摄视频得到的值
            responseVideoData:{},
            nativeVideo:{},
            coverImgWidth:0,
            coverImgHeight:0,
            hasShowVideoPermission : true,
          }
        },
        computed:{
          //封面图片的style
          getImageStyle(){
            if (this.videoData){
              let imgWidth ;
              let imgHeight ;
              if (!this.videoData.video_hight || this.videoData.video_hight.length == 0 || !this.videoData.video_width || this.videoData.video_width == 0){
                imgHeight = 100;
                imgWidth = 300;
              }else{
                imgWidth = parseInt(this.videoData.video_width);
                imgHeight = parseInt(this.videoData.video_hight);
              }
             //高度大于200的处理
             if (imgHeight > 200){
               imgWidth = 200 * imgWidth/imgHeight;
               imgHeight = 200;
             }
             //高度小于200的处理
             if (imgHeight < 100){
                imgWidth = 100 * imgWidth / imgHeight;
                imgHeight = 100;
             }
             //图片宽度大于屏幕的处理
             if(imgWidth >= window.clientWidth){
               imgHeight = imgHeight * (window.clientWidth - 30) /imgWidth;
               imgWidth = window.clientWidth - 30;
             }
             this.coverImgWidth = imgWidth;
             this.coverImgHeight = imgHeight;

             return {
               width:imgWidth + 'px',
               height:imgHeight + 'px',
             }
            }
            //else
            this.coverImgWidth = 300;
            this.coverImgHeight = 100;

            return {
              width:'300px',
              height:'100px',
            };
          },
          //播放按钮的style
          getPlayIconStyle(){

              let top = (this.coverImgHeight - 75.0)/2.0;
              let left = (this.coverImgWidth - 75.0)/2.0;

              return {
                top:top + 'px',
                left:left + 'px',
              }
          },
        },
        methods:{
          onSelVideo() {
            this.nativeVideo.asyncUploadVideo();
          },
          //视频删除
          deleteVideo(){
              this.responseVideoData = [];
              this.changed(undefined);
          },
          //开启选择视频
          popupFile(){
            let opt = this.uploadParms;
            this.nativeVideo.init(opt);
          },
          //每选择一个视频成功后的回调
          progress(data){
            this.responseVideoData = data;
            this.changed(this.responseVideoData);
          },
          //视频选择、上传完毕(不使用)
          complete(data){

          },
          //播放或者暂停视频
          playVideo(){
            //选择或拍摄视频的回调
            if(this.responseVideoData.video_url){
              let videoChoosed = this.$refs.videoChoosed;
              if (videoChoosed.paused){
                videoChoosed.play();
              }else{
                videoChoosed.pause();
              }
            }else{
              let videoSetted = this.$refs.videoObjSetted;
              if (videoSetted.paused){
                videoSetted.play();
              }else {
                videoSetted.pause();
              }
            }
          },
          changed(data){
            this.$emit('on-changed',data);
          },
        },
        created(){
          // modify by perry
          /*this.nativeVideo = new nativeVideo({
            webVideo:webVideo,
            target: this,
          });*/

          this.nativeVideo = createVideoMgr(this,  {
            webVideo:webVideo,
            target: this,
          });
        },
    }
</script>

<style scoped>
  .content {position: relative;}

  .playIcon {position: absolute;width:75px;height: 75px;}

  .pop-btn{width: 1.8rem;height: 1.8rem;}

  .coverImg {position: relative;background-color: rgba(0,0,0,0.5)}

  .deleteIcon { width: 16px;height: 16px;position: absolute;}

  .pub-video{
      border: 1px #4685ff solid;
      border-radius: 20px;
      color: #4685ff;
      width: 4rem;
      height: 1.5rem;
      font-size: 0.6rem;
      text-align: center;
      line-height: 1.5rem;
      margin-right: 40px;
    }

  .h5-video-view-style {
    position: relative;width: 1.5rem;height: 1.5rem;
  }
  .h5-video-view-input-style {
    position: absolute;left:0;top:0;opacity:0;width: inherit;height: inherit;
  }
  .fix {display: inline-block;}
</style>



/* videoData的数据
{
"video_cover_url": "http://test-interact.hbeducloud.com:8088/media/public/fhxx/video_snapshot/image_18050709365121056745.jpg",
"video_url": "http://test-interact.hbeducloud.com:8088/media/public/fhxx/video/video_18050709365020852457.mp4",
"video_converted_status": 2,
"video_type": "mp4",
"video_duration": "0",
"video_width": "480",
"video_converted_url": "http://test-interact.hbeducloud.com:8088/media/public/fhxx/video/video_18050709365020852457_converted.mp4",
"video_hight": "360",
"video_id": 15,
"video_size": "175855",
"video_square": "480,360",
"video_name": "video.mp4"
}
*/
