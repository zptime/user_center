/**
 * Created by jie on 2018/3/14.
 */

function nativeAudio (opt){
    var _self = this;
    this.options  = opt || {}
    this.init = function () {
        window._win_nativeAudio = _self;
        //todo  这里添加代码，调用native麦克风
      if((typeof callNativeAudioFuc) != 'undefined') {
        callNativeAudioFuc(this.options);
      }
    },
      /*
      * 播放本地音频,结束后的回调是  _win_nativeAudio.stopPlayAudio()
      *
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
    this.playLocalAudio = function (obj) {
      if (typeof callNativePlayLocalAudio != 'undefined'){
        callNativePlayLocalAudio(JSON.stringify(obj));
      }
    },
    //播放完成，或者停止播放音频（本地）
    //data是空数组的JSON字符串
    this.stopPlayAudio = function (data) {
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
                    type: "onStart",
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
    native在录音结束之后，调用 _win_nativeAudio.stop()方法,参数传序列化的json对象。
    */
    this.stop = function (data) {
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
                    type: "onStop",
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

    /*
    用户确认上传时候触发
     */
    this.makeSure = function (data) {

    }

    /*
    用户取消上传时候触发
     */
    this.cancel = function (data) {

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
      return false;
    }
}

export default nativeAudio = nativeAudio

