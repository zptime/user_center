
<template>
    <span>
        <span @click="popupImage" v-if="popupBtn" :style="btnSecStyle">
            <slot name="popBtn">
                <div class="pub-img">添加图片</div>
            </slot>
        </span>
        <div ref="mImgNode" class="image-container" :style="contentSecStyle">
            <a v-for="(item,index) in images" :key="index" class="image-item" :style="itemStyle(index)">
                <img :src="item[`${murlKey()}`]" class="image" @click="viewFullImage(index)">
                <img v-if="removeIcon" src="./icon-delete.png" class="delete-icon" @click="removeImage(index)">
            </a>
        </div>

        <previewer :list="previewerImages" ref="previewer" ></previewer>

    </span>
</template>

<script type="text/ecmascript-6">
    const prefixList = ['-moz-box-', '-webkit-box-', '']
    import nativeImage from './nativeImage.js'
    import webImage from './webImage.js'
    import Previewer from 'vux/src/components/previewer/index.vue'
    import {createImageMgr} from './ImageMgr.js'
    let local_urlKey = ''
    export default {
        props: {
          cols: {
            type: Number,
            default: 3
          },
          gutter: {
            type: Number,
            default: 8
          },
          maxCount: {
              type: Number,
              default: 9
          },
          murl:  {
              type: String,
              default: 'image_crop_url'
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
          }
        },

        components: {
            Previewer
        },

        data(){
            return{
                hasChoosedCount: 0,
                images: [

                ],
                native_image: {},

                options: {
                    getThumbBoundsFn (index) {
                      // find thumbnail element
                      let thumbnail = document.querySelectorAll('.previewer-demo-img')[index]
                      // get window scroll Y
                      let pageYScroll = window.pageYOffset || document.documentElement.scrollTop
                      // optionally get horizontal scroll
                      // get position of element relative to viewport
                      let rect = thumbnail.getBoundingClientRect()
                      // w = width
                      return {x: rect.left, y: rect.top + pageYScroll, w: rect.width}
                      // Good guide on how to get element coordinates:
                      // http://javascript.info/tutorial/coordinates
                    }
                }
            }
        },

        methods: {
            itemWidth(){
                let rootWidth = this.$refs.mImgNode.offsetWidth
                let width = rootWidth - this.gutter * (this.cols - 1)
                return `${Math.floor(width/this.cols)}px`
            },

            itemStyle(index){
                const styles = {
                    'position': 'relative',
                    'float': 'left',
                    'padding-top': `${this.gutter/2}px`,
                    'width': this.itemWidth()
                }
                for (let i = 0; i < prefixList.length; i++) {
                  styles[`${prefixList[i]}box-sizing`] = 'border-box'
                }
                let col_seq = index%this.cols
                if (col_seq != 0){
                  styles['margin-left'] = `${this.gutter}px`
                }
                return styles
            },

            popupImage(){
              this.maxCount =  isNaN(this.maxCount) ? 9 : this.maxCount;
              this.hasChoosedCount = isNaN(this.hasChoosedCount) ? 0 : this.hasChoosedCount;
              if (this.hasChoosedCount < 0){
                this.hasChoosedCount = 0;
              }
              if (this.hasChoosedCount > this.maxCount){
                this.hasChoosedCount = this.maxCount;
              }

              let obj = {
                maxCount: this.maxCount,
                 hasChoosedCount:this.hasChoosedCount
              };
              this.native_image.init(obj);

              // this.images.push( {
              //     "image_id": "162",
              //     "image_url": "http://test-oa.hbeducloud.com:8088/oa_dev/1/c0cc384d67a5407881f0c182a5f68ecd_thumb.jpg",
              //     "original_height": "400",
              //     "original_size": "55091",
              //     "image_crop_url": "http://test-oa.hbeducloud.com:8088/oa_dev/1/6764802ebbaf4227b3b4316a86b14958_crop.jpg",
              //     "original_width": "550",
              //     "image_name": "赶海.jpg",
              //     "original_image_url": "http://test-oa.hbeducloud.com:8088/oa_dev/1/c9307879d00a49368fd6c199ac935634.jpg"
              //   });
              // this.change()
            },

            init(){
                if (this.origin.length > 0){
                    this.fillImages(this.origin)
                }

                // modify by perry
                /*this.native_image = new nativeImage({
                    webImage: webImage,
                    target: this,
                    settings: {
                      maxCount: isNaN(this.maxCount) ? 2 : this.maxCount.toString(),
                      hasChoosedCount:'0'
                    }
                })*/
                this.native_image = createImageMgr(this,{
                    webImage: webImage,
                    target: this,
                    settings: {
                      maxCount: isNaN(this.maxCount) ? 2 : this.maxCount.toString(),
                      hasChoosedCount:'0'
                    }
                  });
            },

            getImagesSize(){
                return this.images.length
            },

            //填充 images 数组
            fillImages(images){
                this.images = images
                this.change()
            },

            addImage(image){
                this.images.push(image)
                this.change()
            },

            removeImage(index){
                let size = this.getImagesSize()
                if(!isNaN(index) && index>=0 && index<size){
                    this.images.splice(index,1);
                    this.$emit('on-remove',index);
                    this.change()
                    this.hasChoosedCount -= 1;
                    return index
                }
            },

            // 每上传成功一张图片，就被触发一次
            progress(data){
                if ( typeof(data) == 'object' ){
                    let imageObj = data
                    this.addImage( imageObj )
                    this.hasChoosedCount += 1;
                }else{
                    throw error('图片对象格式错误')
                }
                this.$emit('on-progress',data);
            },

            complete(data){
                this.$emit('on-complete',data);
            },

            change(){
                //从计算 外层容器高度
                let width_str = this.itemWidth()
                let aHeight = parseInt(width_str.substr(0,width_str.length-2))
                let rows = Math.floor((this.getImagesSize()-1)/this.cols) + 1
                if (this.getImagesSize()==0){
                  rows = 0
                }
                let height = (aHeight + this.gutter) * rows
                this.$refs.mImgNode.style.height = height + 'px'
                //
                let data = this.images
                this.$emit('on-change',data);
            },

            // 预览大图
            viewFullImage(index){
                this.$refs.previewer.show(index)
            },

            urlKey(){
                return this.url
            },

            murlKey(){
                if (this.getImagesSize()>0 ){
                    if (this.images[0][this.murl]){
                        return this.murl
                    }
                }
                return this.urlKey()
            }

        },

        created() {
            window._MImg = this
        },

        mounted(){
          this.init()
        },

        computed: {
            previewerImages(){
                let res = []
                for(let i=0; i<this.getImagesSize(); i++){
                    let obj = {}
                    obj['src'] = this.images[i][this.urlKey()]
                    res.push( obj )
                }
                return res
            }
        }
    }

</script>

<style scoped lang="less">
    .pop-btn{
        width: 1.8rem;
        height: 1.8rem;
    }

    .image-container{
        width: 100%;
        padding: 0px;
        clear: both;
    }

    .image-item{
        position: relative;
        float: left;
    }

    .image{
        width: 100%;
    }

    .delete-icon{
        position: absolute;
        right: -5px;
        top: 0;
        width: 24px;
        height: 24px;
        padding: 10px 10px;
    }
    .pub-img{
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
