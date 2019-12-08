<template>
  <div class="member">
    <head-top :head="head">
      <img slot="left" src="../../../images/icon-return.png" @click="goBack"/>
    </head-top>
    <div class="contentBox" v-cloak>
      <div class="search" v-if="bulkOptCfg.searchShow">
        <m-search :search="search"  @onsearch="mySearch"></m-search>
      </div>
      <div class="list-common">
        <div class="item">
          <div class="item-title">
            <span class="number">已选择{{ chooseNum }}人</span>
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
          <span class="btn_del right" @click="optClick('del')">移除所选</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script type="es6">
  import HeadTop from '@/components/Head.vue'
  import MSearch from '@/components/m-search/Search.vue'
  import { contactGroupUserDel } from '../dealData'
  export default {
    props:['groupId','bulkData','bulkOptCfg'],
    data(){
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
        bulkOptData:[],//批量操作数据
        bulkDataIds:[],//批量操作数据id
        chooseNum:0,//已选人数
        checkVal:'全选',//全选、取消全选文字
        keyword:'',//搜索关键字
      }
    },
    components: {
      HeadTop,
      MSearch,
    },
    methods:{
      goBack(){
        this.clearDeal();
        this.$emit('on-close',this.bulkDataIds);
      },

      //恢复变量状态
      clearDeal(){
        this.checkVal = '全选';
        this.chooseNum = 0;
        this.keyword = '';
        this.search.is_focus = false;
        this.search.search_txt = '';
        this.bulkDataIds = [];
        for(let i=0;i<this.bulkOptData.length;i++){
          this.bulkDataIds.push(this.bulkOptData[i].account_id);
        }
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
        }else{//移除所选
          if(this.groupId){//批量编辑-移除成员
            this.delEditUser();
          }else{//已选择人员-移除成员
            this.delCreateUser();
          }
        }
      },

      //批量编辑-移除成员
      async delEditUser(){
        let del_users = '';
        for(let i=0;i<this.bulkOptData.length;i++){
          let data = this.bulkOptData[i];
          if(data.is_checked){
            del_users += data.account_id+','+data.user_type_id+','+data.school_id+';';
          }
        }
        let res = await contactGroupUserDel(this.groupId,del_users);
        if(res.c==0){
          this.$vux.toast.show({
            type: 'text',
            text: '删除成功'
          });
          this.clearDeal();
          let _this = this;
          setTimeout(function () {
            _this.$emit('init-member');
          }, 500);
        }else{
          this.$vux.toast.show({
            type: 'text',
            text: res.m
          });
        }
      },

      //已选择人员-移除成员
      delCreateUser(){
        //前端页面删除
        for(let i=this.bulkOptData.length-1;i>=0;i--){
          if(this.bulkOptData[i].is_checked){
            this.bulkOptData.splice(i,1);
          }
        }
        this.goBack();
      },

      mySearch(){
        this.keyword = this.search.search_txt;
      }
    },
    watch:{
      chooseNum(val){
        if(val==this.bulkOptData.length){
          this.checkVal = '取消全选';
        }else if(val==0){
          this.checkVal = '全选';
        }
      },
      bulkOptCfg(val){
        this.$set(this.head,'title',val.headTitle);
      },
      bulkData(newValue){
        this.bulkOptData = JSON.parse(JSON.stringify(newValue))
      }
    }
  }
</script>

<style scoped>
  @import "../member.css";
  .contentBox {
    bottom: 0;
    background: #fff;
  }
</style>
