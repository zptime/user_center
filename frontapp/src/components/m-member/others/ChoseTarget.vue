<template>
  <div class="member">
    <head-top :head="head">
      <img slot="left" src="../../../images/icon-return.png" @click="goBack"/>
    </head-top>
    <div class="contentBox" v-cloak>
      <div class="search">
        <m-search :search="search"  @onsearch="mySearch"></m-search>
      </div>
      <div class="list-common">
        <div class="item">
          <div class="item-title clb">
            <span class="number left">已选择{{ chooseNum }}人</span>
            <span class="opt right">
              <span class="operate right" :class="checkVal=='全选'?'check_all':'deselect_all'" @click="toggleCheckAll">{{ checkVal }}</span>
            </span>
          </div>
          <div v-for="(itemData,index) in bulkOptData">
            <div class="item-detail clb" @click="toggleCheckOne(index)" v-if="itemData.username.search(keyword)!=-1" :class="{'item-border-none': index==bulkOptData.length-1}">
              <span class="other-all left">
                <span class="avatar left">
                  <img :src="itemData.avatar" v-if="itemData.avatar">
                  <img src="../images/icon-default-avatar.png" v-else>
                </span>
                <span class="username left">{{ itemData.username }}</span>
              </span>
              <span class="opt right">
                <span>
                  <img class="opt-check" src="../images/icon-selected.png" v-if="itemData.is_checked">
                  <img class="opt-check" src="../images/icon-not-selected.png" v-else/>
                </span>
              </span>
            </div>
          </div>
        </div>
      </div>
      <div class="btnOpt">
        <div class="btnCommon btnBottomOpt boxShadowGray clb">
          <span class="btn_cancel left" @click="optClick('cancel')">取消</span>
          <span class="btn_divide"></span>
          <span class="btn_sure right" @click="optClick('sure')">确定</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script type="es6">
  import HeadTop from '@/components/Head.vue'
  import MSearch from '@/components/m-search/Search.vue'
  import { getInviteFirst } from '../others/exchange.js'
  export default {
    props:{
      orderFlag: {//是否按照字母排序
        type: Boolean,
        default: true
      },
      headTitle: {//头部title
        type: String,
        default: ''
      },
      dataIndex: {//数据列表index
        type: Number,
        default: -1
      },
      bulkData: {//数据列表
        type: Array,
        default: function () {
          return []
        }
      },
    },
    data () {
      return {
        head:{
          icon: 'return',
          title: '',
          more: false
        },
        search:{
          is_focus:false,
          search_txt:'',
          placeholder_txt:'请输入姓名',
        },
        chooseNum:0,//已选人数
        checkVal:'全选',//全选、取消全选文字
        keyword:'',//搜索关键字
        bulkOptData:[],
      }
    },
    components: {
      HeadTop,
      MSearch,
    },
    methods:{
      goBack(){
        this.clearDeal();
        this.$emit('on-close');
      },

      //将数据按照字母（A-Z）排序
      orderFiled(){    
        let obj = getInviteFirst(this.bulkOptData,'username');

      },

      //清空操作-恢复变量状态
      clearDeal(){
        this.checkVal = '全选';
        this.keyword = '';
        this.search.is_focus = false;
        this.search.search_txt = '';
        let ele = document.getElementsByClassName('list-common')[0];
        ele.scrollTop = 0;
      },

      //搜索框-搜索事件
      mySearch(){
        this.keyword = this.search.search_txt;
      },

      //全选、取消全选事件
      toggleCheckAll(){
        if(this.checkVal=='全选'){
          this.chooseNum = this.bulkOptData.length;
          for(let i=0;i<this.bulkOptData.length;i++){
            this.bulkOptData[i].is_checked = true;
          }
        }else{
          this.chooseNum = 0;
          for(let i=0;i<this.bulkOptData.length;i++){
            this.bulkOptData[i].is_checked = false;
          }
        }
      },

      //选择、取消选择事件
      toggleCheckOne(index){
        if(this.bulkOptData[index].is_checked){
          this.chooseNum-=1;
        }else{
          this.chooseNum+=1;
        }
        this.bulkOptData[index].is_checked = !this.bulkOptData[index].is_checked;
      },

      //底部操作按钮事件
      async optClick(opt){
        if(opt=='cancel'){//取消
          this.goBack();
        }else if(opt=='sure'){
          this.clearDeal();
          let reData = {
            'bulkData':this.bulkOptData,
            'count':this.chooseNum,
            'index':this.dataIndex
          };
          this.$emit('on-sure',reData);
        }
      },
    },
    watch:{
      chooseNum(val){
        if(val==this.bulkOptData.length){
          this.checkVal = '取消全选';
        }else if(val==0){
          this.checkVal = '全选';
        }
      },
      headTitle(val){
        this.$set(this.head,'title',val);
      },
      bulkData(newValue){
        this.chooseNum = 0;
        for(let i=0;i<newValue.length;i++){
          if(newValue[i].is_checked){
            this.chooseNum = this.chooseNum + 1;
          }
        }
        /*1.组件间的数据传递只能是父到子(props)，数据流向的单一保证了数据变化的可追踪性；
          2.如果子组件操作该值要求父组件作出相应变化时，那就子组件emit一个事件，
            父组件内捕获这个事件，然后在父组件内执行相应的变化；
          3.如果只是想通过props获取一个初始值，之后无论子组件如何操作该值都不会影响父组件的变化，
            那就在传入子组件数据的时候就进行一下处理（值引用类型数据无需处理，址引用数据进行一下
            深度拷贝Object.assign({},obj)或者JSON.parse(JSON.stringify(obj))）*/
        //this.bulkOptData=newValue; //无效，会改变父组件的值
        //this.bulkOptData = Object.assign({},newValue); //无效，会改变父组件的值
        this.bulkOptData = JSON.parse(JSON.stringify(newValue)); //有效，不会改变父组件的值
        if(this.orderFlag){
          this.orderFiled();
        }
      },
    }
  }
</script>

<style scoped>
  @import "../member.css";
  .contentBox{
    background-color: #fff;
    bottom:0;
  }
</style>
