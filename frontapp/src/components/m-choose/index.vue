<template>

    <div style="position: relative;margin-top: 60px;">

      <template v-if="checkSub('m-audio')">
        <!-- modify by perry-->
        <m-audio ref="mAudioView"
                 @on-should-showH5Record="mShouldH5Record"
                 @on-change="mAudioChange"
                 :btnSecStyle="mAudio.btnSecStyle"
                 :contentSecStyle="mAudio.contentSecStyle"
                 :changeMode="_mAudio.changeMode"
                 :url="_mAudio.url"
                 :origin="_mAudio.origin"
                 :popupBtn="_mAudio.popupBtn"
                 :removeIcon="_mAudio.removeIcon">

        </m-audio>
      </template>

      <template v-if="checkSub('m-img')">
        <m-img  ref="m-img"
                @on-change="mImgChange"
               :btnSecStyle="mImg.btnSecStyle"
               :contentSecStyle="mImg.contentSecStyle"
               :cols="_mImg.cols"
               :gutter="_mImg.gutter"
               :maxCount="_mImg.maxCount"
               :origin="_mImg.origin"
               :murl="_mImg.murl"
               :url="_mImg.url"
               :popupBtn="_mImg.popupBtn"
               :removeIcon="_mImg.removeIcon">
        </m-img>
      </template>

      <template v-if="checkSub('choose-file')">
        <choosefile ref="choose-file"
                    @on-changed="fileChanged"
                    :btnSecStyle="cFile.btnSecStyle"
                    :contentSecStyle="cFile.contentSecStyle"
                    :popupBtn="_cFile.popupBtn"
                    :maxCount="_cFile.maxCount"
                    :fileType="_cFile.fileType"
                    :showDelete="_cFile.showDelete">

        </choosefile>
      </template>
      <template v-if="checkSub('m-video')">
        <m-video ref="m-video"
                 @on-changed="videoChanged"
                 :btnSecStyle="mVideo.btnSecStyle"
                 :contentSecStyle="mVideo.contentSecStyle"
                 :popupBtn="_mVideo.popupBtn">

        </m-video>

      </template>

    </div>

</template>

<script>

  import MImg from '../m-img/index.vue'
  import MAudio from '../m-audio/index.vue'
  import Choosefile from '../m-file/chooseFile.vue'
  import MVideo from '../m-video/index.vue'

    export default {
      name: "MChoose",
      components: {
        MImg,
        MAudio,
        Choosefile,
        MVideo
      },
      props: {
        _subComponents: {
          type: Array,
          default: () => []
        },
        _mAudio: {
          type: Object,
          default: () => {}
        },
        _mImg: {
          type: Object,
          default: () => {}
        },
        _cFile: {
          type: Object,
          default: () => {}
        },
        _mVideo: {
          type: Object,
          default: () => {}
        },
      },

        data() {
          return {
            mImg: {
              btnSecStyle: {
                'position': 'absolute',
                'left': '5rem',
                'top': '-60px'
              },
              contentSecStyle: {
                'position': 'relative',
                'marginTop':'0.5rem'
              }
            },
            mAudio: {
              btnSecStyle: {
                'position': 'absolute',
                'left': '0rem',
                'top': '-60px'
              },
              contentSecStyle: {
                'position': 'relative',
              },
            },
            cFile: {
              btnSecStyle: {
                'position': 'absolute',
                'left': '10rem',
                'top': '-60px'
              },
              contentSecStyle: {
                'position': 'relative',
                'marginTop':'0.5rem'
              },
            },
            mVideo: {
              btnSecStyle: {
                'position': 'absolute',
                'left': '15rem',
                'top': '-60px'
              },
              contentSecStyle: {
                'position': 'relative',
                'marginTop':'0.5rem'
              },
            },
          }
        },
        methods: {
         //allFileData所有选择文件的数据
          fileChanged(allFileData) {
            this.$emit('on-cFileChange', allFileData);
          },
          checkSub(component_name) {
            if (this._subComponents.indexOf(component_name) > -1) {
              return true
            }
            return false
          },

          // modify by perry
          mShouldH5Record(shouldH5Record) {
            this.$emit('on-shouldShowH5Record', shouldH5Record)
          },
          mAudioChange(data) {
            this.$emit('on-mAudioChange', data)
          },

          mImgChange(data) {
            this.$emit('on-mImgChange', data)
          },
          videoChanged(data){
            this.$emit('on-mVideoChange',data);
          },

          execAudioAction(event, args) {
              //alert(event);
              if ('startRecord' == event) {
                this.$refs.mAudioView.start();
                return;
              }

              if ('stopRecord' == event) {
                this.$refs.mAudioView.stop();
                return;
              }

              if ('makeSure' == event) {
                this.$refs.mAudioView.makeSure(args);
                return;
              }

              if ('cancelClick' == event) {
                this.$refs.mAudioView.cancelClick();
                return;
              }
          },
        },
        mounted(){
          for(let i=0;i<this._subComponents.length;i++){
             let  refStr = this._subComponents[i];
             if(refStr == 'm-audio'){
               refStr = 'mAudioView';
             }
             let componentsObj = this.$refs[refStr];
             componentsObj.btnSecStyle.left = 5 *i + 'rem';
          }
        },
        watch:{

        }
    }
</script>

<style scoped>


</style>
