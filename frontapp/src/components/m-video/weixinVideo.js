/**
 * Created by yulu on 2018/6/20.
 */

import {uploadVideo} from '../../service/getData.js'
import {showTextLoading,hideTextLoading,showTextToast} from "../framework/toastViewMgr.js";
//import {PERMISSION_TABLE,PERMISSION_FILE} from '../framework/permissionMgr.js'
//import {hasSystemPermission} from "../framework/serviceMgr";

function weixinVideo (target,opt){

  var _self = this;
  this.target = target;
  this.options  = opt || {}
  /*try{
    alert("permission=" + hasSystemPermission(target, PERMISSION_FILE));
  }catch(error1) {
    alert(error1.message);
  }*/

  //选择视频
  this.init = function (obj) {
  },
    //拍摄视频
    //obj为空
    this.takeVideo = function (obj) {
      window._win_nativeVideo = _self;
      if ((typeof  callNativeTakeVideo) != 'undefined'){
        callNativeTakeVideo(JSON.stringify(obj));
      }
    },
    /*
     native在拿到视频对象后，调用 _win_nativeVideo.progress()方法,参数传序列化的json对象
     每上传成功一个文件，就被触发一次
     */
    this.progress = function (data) {
      var fileObj = {}
      if (data){
        try {
          if (typeof data == 'string'){
            fileObj = JSON.parse(data)
          }else if(typeof data == 'object'){
            fileObj = data
          }
          _self.options.webVideo.fireEvent({
            type: "onProgress",
            params: fileObj,
            options: _self.options
          })
        }catch(e){
          setTimeout(function () {
            alert(e)
          },500);
        }
      }
    },
    /*
    native在所有文件处理完之后，调用 _win_nativeVideo.complete()方法,参数传序列化的json对象例如："{"flag":true}"
    */
    this.complete = function (data) {
      var flagObj = {}
      if (data){
        try {
          if (typeof data == 'string'){
            flagObj = JSON.parse(data)
          }else if(typeof data == 'object'){
            flagObj = data
          }
          _self.options.webVideo.fireEvent({
            type: "onComplete",
            params: flagObj,
            options: _self.options
          })
        }catch(e){
          setTimeout(function () {
            alert(e)
          },500);
        }
      }
    }

  // 在原生应用显示
  this.showInNativeApp = function () {
    return false;
  }

  this.asyncUploadVideo = function() {
    innerAsyncUpload(this);
  }
}

let innerAsyncUpload = async (videoMgrSelf)=> {
  showTextLoading(videoMgrSelf.options.target,'上传中');
  //let res = await uploadVideo(fileMgrSelf.options.target.$refs.uFile.files[0]);
  let res = await uploadVideo(videoMgrSelf.target.$refs.uVideoFile.files[0]);
  if (res.c == 0 ) {
    hideTextLoading(videoMgrSelf.options.target);
    showTextToast(videoMgrSelf.options.target,'完成')
    //alert(res.d.video_url);
    videoMgrSelf.progress(res.d);
    videoMgrSelf.complete({flag:true});
    return;
  }
  hideTextLoading(videoMgrSelf.options.target);
  showTextLoading(videoMgrSelf.options.target,res.m);

  fileMgrSelf.complete({flag:false});
  alert('视频上传失败');
}

export default weixinVideo = weixinVideo

