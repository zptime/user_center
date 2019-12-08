
<template>
    <span>
        <span @click="popupMicrophone" :style="btnSecStyle" v-show="popupBtn">
            <slot name="popBtn">
                <div class="pub-audio">输入语音</div>
            </slot>
        </span>

        <div :style="contentSecStyle">
             <div class="one-row" v-for="(item,index) in voices" :key="index" @click="PlayPause(index)">
              <audio ref="dom_audio" :src="item[`${url}`]" v-show="false" controls="false" :data-index="index"
                     onended="javascript:_MAudio.ended(this)"></audio>
              <div class="gif-box" v-if="item['isPlaying']" :style="gifStyle(index)"></div>
              <img class="voice0" v-show="!item['isPlaying']" src="./image/icon-voice-0.png"/>
              <span class="time-label">{{item.voice_duration}}</span>
               <img class="delete-btn" v-if="removeIcon" src="./image/icon-delete.png" @click="removeVoice(index)">
            </div>
        </div>
    </span>
</template>

<script type="text/ecmascript-6">
    import nativeAudio from './nativeAudio.js'
    import webAudio from './webAudio.js'
    import {copy} from './utils.js'
    import {createAudioMgr} from './AudioMgr.js'
    let local_urlKey = ''
    export default {
        props: {
          changeMode: {
              type: String,
              default: 'replace'
          },
          url: {
            type: String,
            required: true,
            validator: function (value) {
              local_urlKey = value
              return true
            }
          },
          origin: {
              type: Array,
              validator: function (value) {
                let size = value.length
                let error_size = value.filter((item,index) => !item[`${local_urlKey}`]).length
                if (error_size > 0){
                    return false
                }
                return true
              },
              default: function () {
                  return []
              }
          },
          popupBtn: {
              type: Boolean,
              default: true
          },
          removeIcon: {
              type: Boolean,
              default: true
          },
          btnSecStyle: {
              type: Object,
              default : () => {}
          },
          contentSecStyle: {
              type: Object,
              default : () => {}
          },
        },

        data(){
            return{
                voices: [
                    /*{
                        "voice_size": "343308",
                        "voice_url": "http://test-repair.hbeducloud.com:8088/media/fhxx/voice/audio_djU5cyWCO9.mp3 ",
                        "voice_name": "audio.wav",
                        "voice_id": "89",
                        "voice_duration": "1",
                        "voice_localPath":''  //本地上传的时候才有这个字段
                        "isPlaying":false/true //是否播放本地音频
                    }*/
                ],
                native_audio: {}
            }
        },

        methods: {
            popupMicrophone(){
                this.native_audio.init()

              // this.voices.push({
              //   "voice_size": "343308",
              //   "voice_url": "http://test-repair.hbeducloud.com:8088/media/fhxx/voice/audio_djU5cyWCO9.mp3 ",
              //   "voice_name": "audio.wav",
              //   "voice_id": "89",
              //   "voice_duration": "1"
              // });
                // modify by perry
               this.$emit('on-should-showH5Record',this.native_audio.shouldShowH5RecordView());
            },

            init(){
                if (this.origin.length > 0){
                    this.fillVoices(this.origin)
                }

                // modify by perry
                /*this.native_audio = new nativeAudio({
                    webAudio: webAudio,
                    target: this
                })*/
              this.native_audio = createAudioMgr(this,{
                webAudio: webAudio,
                target: this
              });
            },

            getVoicesSize(){
                return this.voices.length
            },

            fillVoices(voices){
                for(let i=0;i<voices.length;i++){
                  let obj = voices[i];
                  obj.isPlaying = false;
                }
                this.voices = voices
                this.change()
            },

            addVoice(voice){
                voice.isPlaying = false;
                this.voices.push(voice)
                this.change()
            },
            //单个音频 上传后使用这个
            updateVoice(voice, index){
                voice.isPlaying = false;
                this.voices.splice(index,1,voice)
                this.change()
            },

            removeVoice(index){
                let size = this.getVoicesSize()
                if(!isNaN(index) && index>=0 && index<size){
                    this.voices.splice(index,1);
                    this.$emit('on-remove',index);
                    this.change()
                    return index
                }
            },

            load(data){
                this.$emit('on-load',data);
            },

            start(data){
                // modify by perry
                this.native_audio.start();
                this.$emit('on-start',data);
            },

            stop(data){
                // modify by perry
                this.native_audio.stop();
                this.$emit('on-stop',data);
            },

            makeSure(time) {
                // modify by perry
                this.native_audio.makeSure(time);
            },
            cancelClick(data) {
                // modify by perry
                this.native_audio.cancelClick();
            },
            complete(data){
                if ( typeof(data) == 'object' ){
                    let voiceObj = data
                    if (this.changeMode == 'replace'){
                        this.updateVoice(voiceObj,0)
                    }else if(this.changeMode == 'append'){
                        this.addVoice(voiceObj)
                    }
                }else{
                    throw error('录音对象格式错误')
                }
                this.$emit('on-complete',data);
            },

            change(){
                let data = this.voices
                this.$emit('on-change',data);
            },

            /*
            以下是一条录音播放相关事件
            */
            PlayPause(index){
                let voiceTmp = {}
                if(this.voices.length <= 0) return
                copy(voiceTmp, this.voices[index])
                voiceTmp['isPlaying'] = !this.voices[index]['isPlaying']
                this.voices.splice(index,1,voiceTmp)
                //播放远程音频
                if(!this.popupBtn && !this.removeIcon){
                  //播放audio
                  let el = this.$refs.dom_audio[index]
                  if ( el.paused ){
                    el.play()
                  }else{
                    el.pause()
                  }
                  return;
                }
              // 播放本地音频
              this.native_audio.playLocalAudio(voiceTmp);
            },
          //停止播放 回调
            stopPlayAudio(data){
              //暂时只处理了一个音频的情况 index取0
              let voiceObj = this.voices[0];
              voiceObj.isPlaying = false;
            },
            ended(element){
                let index = element.getAttribute('data-index')
                this.voices[index]['isPlaying'] = false
            },

            gifStyle(index){
              let style = {}
              let voice = this.voices[index]
              style['animation-duration'] = '1.0s'
              style['animation-iteration-count'] = voice.voice_duration ? voice.voice_duration / 1.0 : 1
              style['animation-timing-function'] = 'linear'
              return style
            },
        },
        created() {
            window._MAudio = this
            this.init()
        },
        watch:{
          origin(oldval,newval){
            if(newval.length != oldval.length ){
              this.init();
            }
          }
        }
    }

</script>

<style scoped>
    .pop-btn{
      width: 1.8rem;
      height: 1.8rem;
    }

  .one-row{
    display: inline-block;
    vertical-align: middle;
    background-color: #4685ff;
    width: 9.5rem;
    height: 2rem;
    border-radius: 1rem;
    position: relative;
    font-size: 0.7rem;
    margin: 0.2rem 0;
  }

  .time-label{
    display: inline-block;
    vertical-align: middle;
    color: white;
    line-height: 2rem;
    height: 2rem;
    position: absolute;
    right: 1rem;
  }
  .delete-btn{
    display: inline-block;
    vertical-align: middle;
    width:1rem;
    height: 1rem;
    margin-top:0.5rem;
    position: absolute;
    right:-30px ;
  }

  @keyframes playVoiceAnimation
  {
    0%   {background-image: url("./image/icon-voice-1.png");}
    33%  {background-image: url("./image/icon-voice-2.png");}
    67%  {background-image: url("./image/icon-voice-3.png");}
    100% {}
  }

  .gif-box{
    display: inline-block;
    vertical-align: middle;
    width: 0.9rem;
    height: 0.9rem;
    animation-name: playVoiceAnimation;
    background-size: cover;
    position: absolute;
    left: 0.8rem;
    top: 0.45rem;
  }

  .voice0{
    display: inline-block;
    vertical-align: middle;
    width: 0.9rem;
    height: 0.9rem;
    position: absolute;
    left: 0.8rem;
    top: 0.45rem;
  }
  .pub-audio{
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

</style>
