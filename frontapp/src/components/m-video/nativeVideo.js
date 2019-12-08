/**
 * Created by jie on 2018/3/14.
 */

function nativeVideo (opt){
    var _self = this;
    this.options  = opt || {}
    //选择视频
    this.init = function (obj) {
      window._win_nativeVideo = _self;
      //todo
      // //native 中接受数据的形式为{'is_secure':'0'} 是个字符串
      //{'is_secure':'0'}这个是默认值
      // otherRequestParam 是上传视频需要使用的其他参数，如 is_secure 等和视频无关的参数
      if((typeof callNativeVideoFuc) != 'undefined') {
        callNativeVideoFuc(JSON.stringify(obj));
      }
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
    return true;
  }
}

export default nativeVideo = nativeVideo

