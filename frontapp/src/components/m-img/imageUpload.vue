<template>
    <div @click="popupImageUpload">
      <img :src="srcUrl" v-if="srcUrl!=''" alt="" :style="imgStyle"/>
      <img src="./icon-default-avatar.png" v-if="srcUrl==''" alt="" :style="imgStyle"/>
  </div>
</template>

<script type="es6">
  import {createImageMgr} from './ImageMgr.js'
  import webImage from './webImage.js'
  export default {
    name: "m-imageUpload",
    props: ['srcUrl','imgStyle'],
    data () {
      return {
        native_image:{},
      }
    },

    methods: {
      popupImageUpload() {
        let obj = {
          maxCount: 1,
          hasChoosedCount: 0,
        };
        this.native_image.init(obj);
      },
      // 每上传成功一张图片，就被触发一次
      progress(data) {
        if (typeof(data) == 'object') {
          let imageObj = data
        } else {
          throw error('图片对象格式错误')
        }

        this.$emit('on-upload-complete', data);
      },

      complete(data) {
        this.$emit('on-complete', data);
      },
    },

    created() {
      this.native_image = createImageMgr(this, {
        webImage: webImage,
        target: this,
        settings: {
          maxCount: 1,
          hasChoosedCount: 0,
        }
      });
    }
  }
</script>

<style scoped>
</style>

