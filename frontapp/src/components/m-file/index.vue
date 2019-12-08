<template>
  <div>
    <headTop :head="head">
      <img slot="left" src="./images/icon-return.png" @click="goBack"/>
    </headTop>
    <div class="contentBox" v-cloak>
      <div class="content">
        <div class="item" v-for="(item,index) in fileTypeArray">
          <div class="clickHead" @click="spreadFile(item,index)">
            <span v-if="item.isSpread"><img src="./images/icon-downBlueArrow.png">{{item.fileType}}</span>
            <span v-if="!item.isSpread"><img src="./images/icon-rightBlueArrow.png">{{item.fileType}}</span>
          </div>
          <div class="fileView" v-show="item.isSpread">
            <div v-for="(fileData,index) in item.fileArray">
              <div class="fileItem" @click="chooseFile(fileData,index)">
                <span class="fileName">{{fileData.fileName}}</span>
                <img class="choosedFile" v-if="fileData.isFileChoosed" src="./images/icon-greenCheckMark.png"/>
                <span v-if="index == item.fileArray.length - 1" class="lastLine"></span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import headTop from '../Head.vue'

  export default {
    name: "djTest",
    data(){
      return {
        head:{
          icon: 'return',
          title: '选择文件',
          more: false
        },
        fileTypeArray:[{
          isSpread:false,
          fileType:'',
          fileArray:[{
            filePath:'',
            fileName:'',
            isFileChoosed:false,
          }],
        }],
      }
    },
    methods:{
      //选择、取消文件
      chooseFile(fileData,index){
        fileData.isFileChoosed = !fileData.isFileChoosed;
      },
      //界面是从底部启启来的 需要重写返回dismiss方法
      goBack(){
        alert('dd');
      },
      //点击展开收起
      spreadFile(item,index){
        item.isSpread = !item.isSpread;
      },

      //测试数据
      setDefaultData(){
        var arr = [];
        for (let  index = 0 ; index < 50 ;index++){
          var obj = {};
          obj.isSpread = index > 25 ? true :false;
          obj.fileType = 'fileType' + index;
          obj.fileArray = [{
            filePath:'file://var:local',
            fileName:'fileName' + index,
            isFileChoosed:true,
          },
            {
              filePath:'file://var:local',
              fileName:'fileName' + index + 'hah',
              isFileChoosed:false,
            }]
          arr.push(obj);
        }
        this.fileTypeArray = arr;
      },
    },
    created(){
      this.setDefaultData();
    },
    components:{
      headTop,
    }
  }
</script>




<style scoped>


  .content{
    background-color: white;
    overflow: scroll;
    margin-top: 0.5rem;
  }
  .content .item{
  }
  .content .item .clickHead{
    position: relative;
    height: 1.2rem;
    width: 100%;
  }

  .content .item .clickHead span img{
    position: absolute;
    left: 0rem;
    top: 0.25rem;
    width: 0.5rem;
    height: 0.5rem;
  }

  .content .item .clickHead span{
    position: absolute;
    height: 1.2rem;
    line-height: 1.2rem;
    font-size: 0.5rem;
    padding-left: 0.8rem;
    margin-left: 0.5rem;
  }

  .content .item .fileView {
    position: relative;
  }

  .content .item .fileView .fileItem{
    position: relative;
    height: 1.5rem;
  }

  .content .item .fileView .fileItem .fileName{
    display: block;
    position: absolute;
    color: rgb(68,68,68);
    top: 0;
    left: 1.3rem;
    height: 1.5rem;
    line-height: 1.5rem;
    font-size: 0.5rem;
  }

  .content .item .fileView .fileItem .lastLine{
    position: absolute;
    height: 1px;
    background-color: rgba(0,0,0,0.1);
    bottom: 0;
    left: 0.6rem;
    right: 0.6rem;
  }

  .content .item .fileView .fileItem .choosedFile{
    position: absolute;
    width: 0.6rem;
    height: 0.6rem;
    right: 0.5rem;
    margin-top: 0.45rem;
  }

</style>
