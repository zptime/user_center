/**
 * Created by yulu on 2018/6/14.
 */

import wx from 'weixin-js-sdk'
import {query_WeiXin_metaData,uploadBlobImage} from '../../service/getData.js'
import {querySignUrl,querySid} from "../framework/serviceMgr";
import {showTextLoading,showTextToast} from "../framework/toastViewMgr.js";
import {hideTextLoading} from "../framework/toastViewMgr";

function weixinImage (context,opt) {
  var _self = this;
  this.mContext = context;
  this.options = opt || {}
  window._weixin_Image = _self;
  this.lazy_load = false;
  //initWXConfig();

  this.queryImageById = (localId) =>{
    wx.getLocalImgData({
      localId: localId, // 图片的localID
      success: function (res) {
        let base64Str = res.localData.toString();

        // if device is ios
        if (base64Str.indexOf('base64,') != -1) {
          base64Str = base64Str.substring(base64Str.indexOf('base64,') +7)
        }

        uploadImageToServer(base64Str);
      }
    });
  },
  this.chooseImage = (obj) =>{
    try {

    if (obj.maxCount == obj.hasChoosedCount) {
      alert("最多选择" + obj.maxCount + "图片");
      return;
    }

    window._weixin_Image.uploadIndex = 0;
    wx.chooseImage({
      count: obj.maxCount - obj.hasChoosedCount, // 默认9
      sizeType: ['original', 'compressed'], // 可以指定是原图还是压缩图，默认二者都有
      sourceType: ['album', 'camera'], // 可以指定来源是相册还是相机，默认二者都有
      success: function (res) {
        window._weixin_Image.localIds = res.localIds;
        //alert(window._weixin_Image.localIds.length);
        showTextLoading(window._weixin_Image.options.target,'上传中');
        window._weixin_Image.queryImageById(window._weixin_Image.localIds[window._weixin_Image.uploadIndex]);
      }
    });
    }catch (error) {
      alert(error.message);
    }
  }

  this.init = function (obj) {
    window._weixin_Image = this;
    // todo 需要将微信图片选择器拉起来
    if (this.lazy_load == false) {
      initWXConfig(this, obj);
      return;
    }
    this.chooseImage(obj);
  }
    /*
    native在拿到图片对象后，调用 _win_nativeImage.progress()方法,参数传序列化的json对象
    */
    this.progress = function (data) {
      var imageObj = {}
      if (data) {
        try {
          if (typeof data == 'string') {
            imageObj = JSON.parse(data)
          } else if (typeof data == 'object') {
            imageObj = data
          }
          _self.options.webImage.fireEvent({
            type: "onProgress",
            params: imageObj,
            options: _self.options
          })
        } catch (e) {
          // setTimeout(function () {
          //   alert(e)
          // },500);
        }
      }
    },
    /*
    native在所有图片处理完之后，调用 _win_nativeImage.complete()方法,参数传序列化的json对象例如："{"flag":true}"
    */
    this.complete = function (data) {
      hideTextLoading(window._weixin_Image.options.target);
      var flagObj = {}
      if (data) {
        try {
          if (typeof data == 'string') {
            flagObj = JSON.parse(data)
          } else if (typeof data == 'object') {
            flagObj = data
          }
          _self.options.webImage.fireEvent({
            type: "onComplete",
            params: flagObj,
            options: _self.options
          })
        } catch (e) {
          // setTimeout(function () {
          //   alert(e)
          // },500);
        }
      }
    }

}

// todo 从user center获取weixin config
let initWXConfig = async(target, data)=> {
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
    window._weixin_Image.mWXConfig = res.d;

    wx.config({
      debug: false, // 开启调试模式,调用的所有api的返回值会在客户端alert出来，若要查看传入的参数，可以在pc端打开，参数信息会通过log打出，仅在pc端时才会打印。
      appId: _weixin_Image.mWXConfig.appid, // 必填，公众号的唯一标识
      timestamp: _weixin_Image.mWXConfig.timestamp, // 必填，生成签名的时间戳
      nonceStr: _weixin_Image.mWXConfig.noncestr, // 必填，生成签名的随机串
      signature: _weixin_Image.mWXConfig.signature,// 必填，签名，见附录1
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
      target.chooseImage(data);
    });
    return;
  }

  alert('获取服务器配置失败');
}

let uploadImageToServer = async (base64Str) =>{
  //alert("uploadImageToServer");
  let res = await uploadBlobImage(base64Str);
  if (res.c == 0) {
    //alert(res.d.original_image_url);
    //alert(res.d.image_crop_url);
    //alert(res.d[0].url);
    window._weixin_Image.progress(res.d);
    window._weixin_Image.uploadIndex++;
    if (window._weixin_Image.uploadIndex < window._weixin_Image.localIds.length) {
      window._weixin_Image.queryImageById(window._weixin_Image.localIds[window._weixin_Image.uploadIndex]);
      return;
    }

    window._weixin_Image.complete({flag:true});
    return;
  }

  alert("上传服务器图片失败");
  window._weixin_Image.complete({flag:false});
}
export default weixinImage = weixinImage

