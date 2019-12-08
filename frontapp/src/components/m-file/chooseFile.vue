<template>
    <span>
       <span @click="popupFile" v-if="popupBtn && nativeFile.showInNativeApp()" :style="btnSecStyle">
         <slot name="popBtn">
            <div class="pub-file">添加附件</div>
         </slot>
       </span>
      <span @click="popupFile" v-if="popupBtn && !nativeFile.showInNativeApp() && hasFilePermission" :style="btnSecStyle">
        <div class="h5-file-view-style">
          <div class="pub-file">添加附件</div>
          <input ref="uFile" type="file" class="h5-file-view-input-style" @change="onSelFiles()"/>
      </div>
      </span>
      <div class="choosedFileView" :style="contentSecStyle" v-show="fileData.length > 0">
        <div class="file" v-for="(item,index) in fileData">
          <div class="fileContent" :style="fileContentStyle"  @click="clickToPreView(item,index)">
            <img class="typeImg" v-if="item.file_name.indexOf('.ppt') > 0" src="./images/icon-ppt.png"/>
            <img class="typeImg" v-else-if="item.file_name.indexOf('.doc') > 0" src="./images/icon-doc.png"/>
            <img class="typeImg" v-else-if="item.file_name.indexOf('.xls') > 0" src="./images/icon-xls.png"/>
            <img class="typeImg" v-else-if="item.file_name.indexOf('.zip') > 0" src="./images/icon-zip.png"/>
            <img class="typeImg" v-else src="./images/icon-unknowType.png"/>
            <span class="leftMsg">
              <p :style="{flex:'1'}"></p>
              <p class="txtMsgLab">{{item.file_name}}</p>
              <p class="sizeMsgLab">{{getFileSize(item)}}</p>
              <p :style="{flex:'1'}"></p>
            </span>
            <span ref="fileStateButton" class="fileStateBtn" v-if="!popupBtn && shouldShowFileStateBtn" @click="clickRightButtotn(item,index)" v-bind:class="{'toDownload':item.downloadState == 0,'downloading':item.downloadState == 1,'downloaded':item.downloadState == -1}">{{getBtnState(item)}}</span>
          </div>
          <div v-show="showDelete" class="rightDeleteSpan" @click="fileDelete(item,index)">
            <img class="rightDelete" :style="{flex:'1',visibility:'hidden'}" src="./images/icon-delete.png">
            <img class="rightDelete" src="./images/icon-delete.png">
            <img class="rightDelete" :style="{flex:'1',visibility:'hidden'}" src="./images/icon-delete.png">
          </div>
        </div>
      </div>
    </span>
</template>

<script>
  import mFile from './index.vue'
  import nativeFile from './nativeFile.js'
  import webFile from './webFile.js'
  import doc from  './fileTypeIcon.js'
  import {createFileMgr} from './FileMgr.js'
  import {PERMISSION_FILE,PERMISSION_SHOW_FILE} from '../framework/permissionMgr.js'
  import {hasSystemPermission} from "../framework/serviceMgr";

    export default {

        name: "choose-file",
        props: {
          showDelete:{
            type:Boolean,
            default: true,
          },
          fileType:{
            type:String,
            default: '',
          },
          fileData:{
            type:Array,
            default: ()=> [],
          },
          maxCount: {
            type: Number,
            default: 9
          },
          popupBtn: {
            type: Boolean,
            default: true
          },
          btnSecStyle:{
            type: Object,
            default: () => {}
          },
          contentSecStyle: {
            type: Object,
            default : () => {}
          }
        },
        components:{
          mFile,
          nativeFile,
        },
        data(){
          return {
            shouldShowFileStateBtn:false,
            hasChoosedCount:0,
            nativeFile:{},
            test: 'doc',
            fileTypeSrc: {
              doc: './images/icon-doc.png'
            },
            hasFilePermission:true,
          }
        },
        methods:{
          // 微信下获取文件管理器文件
          onSelFiles() {
            //alert(this.$refs.uFile.files[0]);
            //this.asyncUpload();
            this.nativeFile.asyncUploadFile();
          },
          //控件被销毁时 做的操作
          beforeDestoryBySuper(){
            this.nativeFile.cancelFileDownload(null);
          },
          downloadFileResult(data){
            console.log('downloadFileResult' + '' + data);
            //data参数未使用
            // let fileDownloadPath = data.file_url;
            // var index = fileDownloadPath .lastIndexOf("\/");
            // let fileName  = fileDownloadPath .substring(index + 1, fileDownloadPath .length);
            this.nativeFile.getPhoneFile(this.fileData);
          },
          getPhoneFileResult(data){
            this.fileData = data;
          },

          //文件预览
          clickToPreView(item,index){
            //编辑的情况下
            if (this.popupBtn){
              this.nativeFile.filePreView(item);
            }
          },
          //文件状态按钮的点击事件
          clickRightButtotn(item,index){
            //点击下载
             if(item.downloadState == 0){
               this.nativeFile.downloadFile(item);
               item.downloadState = 1;
               return;
             }
            //点击查看
            if(item.downloadState == -1){
               this.nativeFile.filePreView(item);
               return;
            }
            //下载中，么有操作
            if(item.downloadState == 1){
               return;
            }
          },
          //文件删除
          fileDelete(item,index){
            this.fileData.splice(index,1);
            this.changed(this.fileData);
            this.hasChoosedCount -= 1;
          },
          // 每上传成功一个文件，就被触发一次
          progress(data){
            if ( typeof(data) == 'object' ){
              let changedObj = this.exchangeObj(data);
              //适配oa系统返回值
              let fileObj = changedObj;
              this.fileData.push(fileObj);
              this.hasChoosedCount += 1;
            }else{
              throw error('文件格式错误')
            }
            this.$emit('on-progress',data);
            this.changed(this.fileData);
          },
          complete(data){
            this.$emit('on-complete',data);
            this.changed(this.fileData);
          },
          changed(allData){
            this.$emit('on-changed',allData);
          },
          //点击选择文件
          popupFile(){
            let inputView = this.$refs.uFile;
            if (inputView && inputView.disabled){
              let str = '最多选择'+this.maxCount+'个文件';
              this.$vux.toast.show({
                type: 'text',
                text: str
              })
              return;
            }
            this.maxCount =  isNaN(this.maxCount) ? 9 : this.maxCount;
            this.hasChoosedCount = isNaN(this.hasChoosedCount) ? 0 : this.hasChoosedCount;
            if (this.hasChoosedCount < 0){
              this.hasChoosedCount = 0;
            }
            if (this.hasChoosedCount > this.maxCount){
              this.hasChoosedCount = this.maxCount;
            }

            let obj = {
              fileType:this.fileType ? this.fileType : '',
              maxCount: this.maxCount,
              hasChoosedCount:this.hasChoosedCount
            };
            this.nativeFile.init(obj);
          },

          setUp(){
            // modify by perry
            /*this.nativeFile = new nativeFile({
               webFile: webFile,
               target: this,
               settings: {
                  maxCount: isNaN(this.maxCount) ? '3' : this.maxCount.toString()
                }
            });*/

            this.nativeFile = createFileMgr(this, {
                webFile: webFile,
                target: this,
                settings: {
                  maxCount: isNaN(this.maxCount) ? '3' : this.maxCount.toString()
                }
              }
            );

            //显示情况下，外界赋值fileData,需要判断本地是否有文件
            if (!this.showDelete && this.fileData.length > 0){
              this.nativeFile.getPhoneFile(this.fileData);
            }
          },
          //文件大小
          getFileSize(item){
            if(item.file_size < 1024){
              let num = item.file_size ;
              num = num.toFixed(2);
              return num + 'b';
            }
            if (item.file_size / 1024 > 1 && item.file_size / 1024 < 1024){
              let num = item.file_size / 1024;
              num = num.toFixed(2);
              return num + 'kb';
            }
            if (item.file_size / 1024 > 1024 ){
              let num = item.file_size /1024 / 1024;
              num = num.toFixed(2);
              return num + 'Mb';
            }
            return 'mei';
          },
          //文件查看 下载 文案显示的判断
          getBtnState(item){
            if ( item.downloadState == -1){
              return '查看';
            }
            if(item.downloadState == 0){
              return '下载';
            }
            if (item.downloadState == 1){
              return '下载中';
            }
            return '';
          },
          //转换obj到互动系统文件返回obj
          exchangeObj(obj){
            let changedObj = {};
            if(!obj.file_name && obj.name){
              changedObj.file_name = obj.name;
              changedObj.file_url = obj.url;
              changedObj.file_id = obj.id;
              changedObj.file_size = obj.size;
              changedObj.downloadState = '0';
            }else{
              changedObj = obj;
            }
            return changedObj;
          }

        },
      /*
      * <!--"file_name": "2289398a40de411a93ac506.png",-->
        <!--"file_url": "http://test-interact.hbeducloud.com:8088/media/public/fhxx/file/2289398-a40de411a93ac506_18041610004624609529.png?fname=2289398-a40de411a93ac506",-->
        <!--"file_id": "96",-->
        <!--"file_size": "196600",-->
        <!--"downloadState": 0-->
      * */
        created(){
          this.setUp();
          this.hasFilePermission = hasSystemPermission(this, PERMISSION_FILE);
          this.shouldShowFileStateBtn = hasSystemPermission(this,PERMISSION_SHOW_FILE);
        },
        computed:{

          fileContentStyle(){
             return {
               width: this.showDelete ? '80%': '100%'
             }
          },
        },
        //外界赋值filedata变化
        watch:{
          fileData(newVal,oldVal){
            //显示模式
            if(!this.showDelete){
               if(newVal.length != oldVal.length){
                 this.nativeFile.getPhoneFile(this.fileData);
               }
            }
          },
          //微信中使用的input，需要动态修改器disabled属性
          hasChoosedCount(newVal,oldVal){
            let inputView = this.$refs.uFile?this.$refs.uFile:{};
            if(!inputView.style) return;
           if(this.hasChoosedCount < this.maxCount){
             inputView.disabled = false;
             inputView.style.display = 'inline-block';
           }else{
             inputView.disabled = true;
             inputView.style.display = 'none';
           }
          }
        },
    }

  /*
fieldata中的对象
         /*
          *   "file_id": "string",
              "file_url": "string",
              "file_size": "string",
              "file_name": "string"
              "downloadState":""// -1 查看 0 下载 1 下载中

* */

</script>

<style scoped>
  .pop-btn{
    width: 1.8rem;
    height: 1.8rem;
  }
  .choosedFileView{

  }

  .choosedFileView .file{
    height: 2.5rem;
  }

  .choosedFileView .file .rightDelete{
    width: 15px;
    height: 15px;
    display: block;
    margin-left: 0.75rem;
  }

  .choosedFileView .file .rightDeleteSpan{
    float: left;
    display: flex;
    flex-flow: column;
    display: inline-block;
    height: 2rem;
  }

  .choosedFileView .file .fileContent{
    float: left;
    border: 1px solid rgb(220,220,220);
    border-radius: 0.2rem;
    background-color: white;
    height: 2rem;
    width: 80%;
    display: inline-block;
  }

  .choosedFileView .file .fileContent .leftMsg{
    position: relative;
    display: -webkit-flex; /* Safari */
    display: flex;
    flex-flow: column;
    height: 2rem;
    width: 50%;
    float: left;
    margin-left: 0.75rem;

  }

  .choosedFileView .file .fileContent  .typeImg{
    display: inline-block;
    margin-top: 0.33rem;
    margin-left: 0.75rem;
    width: 1.34rem;
    height: 1.34em;
    float: left;
  }

  .choosedFileView .file .fileContent .leftMsg .txtMsgLab{
    height: 0.7rem;
    width: 90%;
    flex: 2;
    font-size: 0.7rem;
    line-height: 0.75rem;
    color:rgb(68,68,68) ;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    clear: both;
  }

  .choosedFileView .file .fileContent .leftMsg .sizeMsgLab{
    flex: 1.2;
    width: 100%;
    line-height: 0.5rem;
    font-size: 0.5rem;
    color: rgb(138,138,138);
    overflow: hidden;

  }
  .choosedFileView .file .fileContent .fileStateBtn{
    font-size: 0.45rem;
    height: 0.8rem;
    line-height: 0.8rem;
    border: 1px solid rgb(220,220,220);
    border-radius: 0.1rem;
    float: right;
    margin-top: 0.6rem;
    margin-right: 0.75rem;
    width: 2rem;
    text-align: center;
  }

  .toDownload{
     background-color: #4685ff;
     color: white;
  }

  .downloading{
    background-color: rgb(220,220,220);
    color: white;
  }
  .downloaded{
    background-color: white;
    color: rgb(68,68,68);
  }
  .pub-file{
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

    .h5-file-view-style {
      position: relative;width: 1.5rem;height: 1.5rem;
    }
    .h5-file-view-input-style {
      position: absolute;left:0;top:0;opacity:0;width: inherit;height: inherit;
    }
</style>
