/**
 * Created by yulu on 2018/6/15.
 */

import wx from 'weixin-js-sdk'
import {query_WeiXin_metaData,uploadVoice} from '../../service/getData.js'
import {querySignUrl,querySid} from "../framework/serviceMgr";
import {showTextLoading,hideTextLoading} from "../framework/toastViewMgr.js";

function weixinAudio (context, opt){
  //alert("create weixinAudio=" + location.href.split('#')[0]);
  var _self = this;
  this.mContext = context;
  this.options  = opt || {}
  window._weixin_Audio = _self;
  this.lazy_load = false;
  //initWXAudioConfig();

  this.init = function () {
    if (this.lazy_load == false) {
      initWXAudioConfig(this);
    }
  },

    /*
    native加载麦克风时，调用 _win_nativeAudio.load()方法,参数传序列化的json对象
    */
    this.load = function (data) {
      var audioObj = {}
      if (data){
        try {
          if (typeof data == 'string'){
            audioObj = JSON.parse(data)
          }else if(typeof data == 'object'){
            audioObj = data
          }
          audioObj = JSON.parse(data);
          _self.options.webAudio.fireEvent({
            type: "onLoad",
            params: audioObj,
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
    native开始录音时，调用 _win_nativeAudio.start()方法,参数传序列化的json对象
    */
    this.start = function (data) {
      window._weixin_Audio = this;
      //alert('weixinAudio.start'+ window._weixin_Audio);
      wx.startRecord();
    },

    /*
    native在录音结束之后，调用 _win_nativeAudio.stop()方法,参数传序列化的json对象。
    */
    this.stop = function (data) {
      window._weixin_Audio = this;
      wx.stopRecord({
        success: function (res) {
          window._weixin_Audio.mLocalId = res.localId;
          //alert('weixinAudio.stop'+ ''+ window._weixin_Audio.mLocalId + window._weixin_Audio + res.localId);
        }
      });
    }

    /*
    用户确认上传时候触发
     */
    this.makeSure = function (time) {
      showTextLoading(_self.options.target,'上传中');
      wx.uploadVoice({
        localId: window._weixin_Audio.mLocalId, // 需要上传的音频的本地ID，由stopRecord接口获得
        isShowProgressTips: 0, // 默认为1，显示进度提示
        success: function (res) {
          //alert('wx.uploadVoice'+ res.serverId);
          uploadVoiceToMyServer(res.serverId,time,"");
        }
      });
    }

    /*
    用户取消上传时候触发
     */
    this.cancelClick = function (data) {

    }
  /*
  native在录音完成之后，调用 _win_nativeAudio.complete()方法,参数传序列化的json对象。
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
        _self.options.webAudio.fireEvent({
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

  /*
   是否显示H5 录音框, modify by perry
   */
  this.shouldShowH5RecordView = ()=> {
    return true;
  },
  //播放本地音频
  /*
  * obj包含{
      *          "voice_size": "343308",
                 "voice_url": "http://test-repair.hbeducloud.com:8088/media/fhxx/voice/audio_djU5cyWCO9.mp3 ",
                "voice_name": "audio.wav",
                "voice_id": "89",
                "voice_duration": "1",
                "voice_localPath":'',
                "isPlaying":'', //是否播放  true false
      *       }
  * */
  this.playLocalAudio = (obj)=>{
    if(!window._weixin_Audio.mLocalId){
      return;
    }
    // alert('微信播放本地音频' + window._weixin_Audio.mLocalId + ' obj ' + obj.isPlaying);
    if(obj.isPlaying){
      // alert('微信播放');
      wx.playVoice({
        localId: window._weixin_Audio.mLocalId // 需要播放的音频的本地ID，由stopRecord接口获得
      });
    }else{
      // alert('微信停止');
      wx.stopVoice({
        localId: window._weixin_Audio.mLocalId // 需要停止的音频的本地ID，由stopRecord接口获得
      });
      let arr = [1];
      _self.stopPlayAudio(JSON.stringify(arr));
    }
    wx.onVoicePlayEnd({
      success: function (res) {
        // alert('微信播放完成' + 'wx.onVoicePlayEnd');
        var localId = res.localId; // 返回音频的本地ID
        let arr = [1];
        _self.stopPlayAudio(JSON.stringify(arr));
      }
    });
  },
    //播放完成，或者停止播放音频（本地）
    //data是空数组的JSON字符串
    this.stopPlayAudio = function (data) {
      // alert('微信播放完成' + 'stopPlayAudio');
      var audioObj = {}
      if (data){
        try {
          if (typeof data == 'string'){
            audioObj = JSON.parse(data)
          }else if(typeof data == 'object'){
            audioObj = data
          }
          audioObj = JSON.parse(data);
          _self.options.webAudio.fireEvent({
            type: "onStopPlayAudio",
            params: audioObj,
            options: _self.options
          })
        }catch(e){
          setTimeout(function () {
            alert(e)
          },500);
        }
      }
    }
}

// todo 从user center获取weixin config
let initWXAudioConfig = async(target)=> {
  //let url1 = 'http://interact-test.hbeducloud.com/m/moment/momentList?sid=1&from=weixin&deviceType=ios';
  //let res = await query_WeiXin_metaData('1',location.href.split('#')[0]);
  //alert(querySignUrl(target.mContext));
  let sid = querySid(target.mContext);
  if (!sid || sid == '') {
    alert("微信关联的学校信息无效");
    return;
  }

  //let res = await query_WeiXin_metaData('1',querySignUrl(target.mContext));
  let res = await query_WeiXin_metaData(sid,querySignUrl(target.mContext));
  target.lazy_load = true;
  if (res.c == 0 ) {
    window._weixin_Audio.mWXConfig = res.d;

    //alert('initWXAudioConfig' + window._weixin_Audio.mWXConfig.appid + ' ' + window._weixin_Audio.mWXConfig.timestamp + ' ' + window._weixin_Audio.mWXConfig.noncestr + ' ' + window._weixin_Audio.mWXConfig.signature);
    wx.config({
      debug: false, // 开启调试模式,调用的所有api的返回值会在客户端alert出来，若要查看传入的参数，可以在pc端打开，参数信息会通过log打出，仅在pc端时才会打印。
      appId: window._weixin_Audio.mWXConfig.appid, // 必填，公众号的唯一标识
      timestamp: window._weixin_Audio.mWXConfig.timestamp, // 必填，生成签名的时间戳
      nonceStr: window._weixin_Audio.mWXConfig.noncestr, // 必填，生成签名的随机串
      signature: window._weixin_Audio.mWXConfig.signature,// 必填，签名，见附录1
      jsApiList: ['checkJsApi',
        'onMenuShareTimeline','onMenuShareQQ','onMenuShareWeibo','onMenuShareQZone', // 分享微博，QQ空间
        'chooseImage','previewImage', // 选选图片，预览图片,successfully
        'uploadImage','downloadImage','getLocalImgData', // 上传图片。下载图片，获取图片数据,successfully
        'startRecord', 'stopRecord','onVoiceRecordEnd', //开始录制，停止录制，录制结束接口,successfully
        'playVoice','pauseVoice','stopVoice','onVoicePlayEnd', // 播放声音，暂停声音，停止声音，声音停止回调,successfully
        'uploadVoice','downloadVoice', // 上传声音， 下载声音
        'openLocation','getLocation', // 打开定位，获取定位,successfully
        'scanQRCode'] // 二维码扫描 ,successfully
    });

    wx.ready(function(){
      // config信息验证后会执行ready方法，所有接口调用都必须在config接口获得结果之后，
      // config是一个客户端的异步操作，所以如果需要在页面加载时就调用相关接口，
      // 则须把相关接口放在ready函数中调用来确保正确执行。对于用户触发时才调用的接口，
      // 则可以直接调用，不需要放在ready函数中。
      //alert("WX 配置加载完毕");
    });
    return;
  }

  alert('获取服务器配置失败');
}

//传音频到自己的服务器
let uploadVoiceToMyServer = async(media_id,duration)=>{
  let res = await uploadVoice(media_id,duration);
  hideTextLoading(window._weixin_Audio.options.target);
  if (res.c == 0){
    window._weixin_Audio.complete(res.d);
    //alert('weixinAudio.uploadVoiceToMyServer'+ window._weixin_Audio);
    showTextToast(window._weixin_Audio.options.target,res.m);
    return;
  }
  alert("上传音频失败media=" + media_id + ",duration=" + duration);
}

export default weixinAudio = weixinAudio

