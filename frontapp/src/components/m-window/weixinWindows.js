/**
 * Created by yulu on 2018/6/15.
 */

import wx from 'weixin-js-sdk'
import {query_WeiXin_metaData} from '../../service/getData.js'
import {querySignUrl,querySid} from "../framework/serviceMgr";

function weixinWindows (context, opt) {
  var _self = this;
  this.mContext = context;
  this.options = opt || {}
  window._weixin_windows = _self;
  this.lazy_load = false;

  this.closeWindows = function () {
    if (this.lazy_load == false) {
      initWXWindowsConfig(this);
    }

    wx.closeWindow();
  }

}

// todo 从user center获取weixin config
let initWXWindowsConfig = async(target)=> {
  let sid = querySid(target.mContext);
  if (!sid || sid == '') {
    alert("微信关联的学校信息无效");
    return;
  }
  //let res = await query_WeiXin_metaData('1',querySignUrl(target.mContext));
  let res = await query_WeiXin_metaData(sid,querySignUrl(target.mContext));
  target.lazy_load = true;
  if (res.c == 0 ) {
    window._weixin_windows.mWXConfig = res.d;

    wx.config({
      debug: false, // 开启调试模式,调用的所有api的返回值会在客户端alert出来，若要查看传入的参数，可以在pc端打开，参数信息会通过log打出，仅在pc端时才会打印。
      appId: window._weixin_windows.mWXConfig.appid, // 必填，公众号的唯一标识
      timestamp: window._weixin_windows.mWXConfig.timestamp, // 必填，生成签名的时间戳
      nonceStr: window._weixin_windows.mWXConfig.noncestr, // 必填，生成签名的随机串
      signature: window._weixin_windows.mWXConfig.signature,// 必填，签名，见附录1
      jsApiList: ['checkJsApi',
        'onMenuShareTimeline','onMenuShareQQ','onMenuShareWeibo','onMenuShareQZone', // 分享微博，QQ空间
        'chooseImage','previewImage', // 选选图片，预览图片,successfully
        'uploadImage','downloadImage','getLocalImgData', // 上传图片。下载图片，获取图片数据,successfully
        'startRecord', 'stopRecord','onVoiceRecordEnd', //开始录制，停止录制，录制结束接口,successfully
        'playVoice','pauseVoice','stopVoice','onVoicePlayEnd', // 播放声音，暂停声音，停止声音，声音停止回调,successfully
        'uploadVoice','downloadVoice', // 上传声音， 下载声音
        'openLocation','getLocation', // 打开定位，获取定位,successfully
        'scanQRCode','closeWindow'] // 二维码扫描 ,successfully
    });

    wx.ready(function(){
      // config信息验证后会执行ready方法，所有接口调用都必须在config接口获得结果之后，
      // config是一个客户端的异步操作，所以如果需要在页面加载时就调用相关接口，
      // 则须把相关接口放在ready函数中调用来确保正确执行。对于用户触发时才调用的接口，
      // 则可以直接调用，不需要放在ready函数中。
      //alert("WX 配置加载完毕");
      wx.closeWindow();
    });
    return;
  }

  alert('获取服务器配置失败');
}

export default weixinWindows = weixinWindows

