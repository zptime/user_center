<template>
  <div class="member">
    <div class="selected clb" v-if="showChoose" @click="bulkEdit('choose')">
      <div class="person clb left">
        <scroller lock-y :scrollbar-x=false>
          <div class="person-detail clb left" :style="getSelectedStyle()">
            <span class="person-single borderRadius boxShadowBlue left" v-for="item in chooseCfg.chooseItems">
              {{ item.username }}
            </span>
          </div>
        </scroller>
      </div>
      <div class="count right">{{ chooseCfg.chooseCount }}/{{ chooseCfg.totalCount }}</div>
    </div>
    <div class="search" v-if="showSearch">
      <m-search :search="search"  @onsearch="mySearch"></m-search>
    </div>
    <div class="member-list-common member-list" :style="setMemberStyle">
      <div class="item" v-for="(member,parentIndex) in members">
        <div class="item-title clb">
          <span class="other-all left" @click="isShow(parentIndex)">
            <span class="title left">{{ member.title }}</span>
            <span class="toggle left" v-if="toggleBtn">
              <img src="./images/icon-arrow.png" :style="toggleRotate(member.show,-90)">
            </span>
          </span>
          <span class="operate bulk_edit right" v-if="removeBtn" @click="bulkEdit('delete')">批量编辑</span>
          <span class="number right" v-if="showTotal">{{ member.number }}人</span>
          <span class="operate right" v-if="chooseBtn" :class="member.chooseValue=='全选'?'check_all':'deselect_all'" @click="toggleCheckAll(parentIndex)">{{ member.chooseValue }}</span>
        </div>
        <div v-for="(itemData,index) in member.data" :class="member.show?'show':'hide'">
          <div class="item-detail clb" v-if="itemData.username.search(keyword)!=-1" :class="{'item-border-none': index==member.data.length-1}">
            <span class="other-all left">
              <span class="avatar left">
                <img :src="itemData[`${avatarKey(itemData)}`]" v-if="itemData[`${avatarKey(itemData)}`]">
                <img src="./images/icon-default-avatar.png" v-else>
              </span>
              <span class="username left">{{ itemData[`${nameKey(itemData)}`] }}</span>
              <span class="desc left" v-if="showDesc">{{ itemData.desc }}</span>
            </span>
            <span class="opt right">
              <span class="opt-common opt-del right borderRadius" v-if="removeBtn" @click="isDel(parentIndex,index)">移除</span>
              <span v-if="chooseBtn" @click="toggleCheckOne(parentIndex,index)">
                <img class="opt-check" src="./images/icon-selected.png" v-if="itemData.is_checked">
                <img class="opt-check" src="./images/icon-not-selected.png" v-else/>
              </span>
            </span>
          </div>
        </div>
      </div>
    </div>
    <div class="btnOpt" v-if="showOptBtn">
      <div class="btnCommon btnBottomOpt boxShadowGray clb">
        <span class="btn_cancel left" @click="optClick('cancel')">取消</span>
        <span class="btn_divide"></span>
        <span class="btn_sure right" @click="optClick('sure')">确定</span>
      </div>
    </div>
    <actionsheet v-model="showDelAction" :menus="menus" @on-click-menu-delete="clickDelMenu" show-cancel></actionsheet>
    <popup v-model="showBulkPopup" width="100%" height="100%" position="right" :show-mask=false>
      <bulk-opt :group-id="groupId" :bulk-data="bulkOptData" :bulk-opt-cfg="bulkOptCfg"
                @on-close="closeBulkPopup" @init-member="initEditData">
      </bulk-opt>
    </popup>
  </div>
</template>

<script type="es6">
  import Actionsheet from 'vux/src/components/actionsheet/index.vue'
  import Popup from 'vux/src/components/popup/index.vue'
  import MSearch from '@/components/m-search/Search.vue'
  import Scroller from 'vux/src/components/scroller/index.vue'
  import BulkOpt from './others/BulkOpt.vue'
  import { contactGroupUserDel } from './dealData'
  export default {
    props:{
      groupId:{
        type:String,
        default:''
      },
      origin: {
        type: Array,
        default: function () {
          return []
        }
      },
      username: {
        type: String,
        default: 'username'
      },
      avatar: {
        type: String,
        default: 'avatar'
      },
      toggleBtn: {
        type: Boolean,
        default: false
      },
      removeBtn: {
        type: Boolean,
        default: false
      },
      chooseBtn: {
        type: Boolean,
        default: false
      },
      showOptBtn: {
        type: Boolean,
        default: false
      },
      showDesc:{
        ype: Boolean,
        default: false
      },
      showTotal:{
        ype: Boolean,
        default: false
      },
      showSearch:{
        ype: Boolean,
        default: false
      },
      showChoose:{
        ype: Boolean,
        default: false
      },
      setMemberStyle: {
        type: Object,
        default : () => {}
      }
    },
    data(){
      return {
        members:[],
        pIndex:0,//父循环序号 members->member
        cIndexS:[],//子循环序号 member.data->itemData
        search:{
          is_focus:false,
          search_txt:'',
          placeholder_txt:'请输入姓名',
        },
        keyword:'',//搜索关键字
        filterFlag:false,//是否启用筛选查询
        showDelAction:false,//是否显示删除弹框(actionSheet)
        menus: {//actionSheet的菜单项列表
          'title.noop': '<span class="action-title">确定删除该成员？</span>',
          delete: '<span class="action-del">删除</span>'
        },
        showBulkPopup:false,//是否显示批量操作(删除，选中)页面
        bulkOptData:[],//批量操作数据
        bulkOptCfg:{//批量操作参数设置
          headTitle:'批量编辑',
          searchShow:true
        },
        chooseCfg:{ //已选人员参数设置
          totalCount:0,//人员总数
          chooseCount:0,//已选人员数
          chooseIds:[],//已选人员ID
          chooseItems:[],//已选人员
        }
      }
    },
    components:{
      Actionsheet,
      Popup,
      BulkOpt,
      MSearch,
      Scroller,
    },
    methods:{
      initEditData(){
        this.closeBulkPopup();
        this.$emit('on-init');
      },
      isShow(parentIndex){
        if(this.toggleBtn){
          this.members[parentIndex].show = !this.members[parentIndex].show;
        }else{
          return false;
        }
      },
      avatarKey(item){
        if(item[this.avatar]){
          return this.avatar;
        }
      },
      nameKey(item){
        if(item[this.username]){
          return this.username;
        }
      },
      fillMembers(members){
        /*//人员列表基本结构如下：
        this.members = [{
          "data": [{//人员数据列表
            "account_id":"13",
            "avatar":"http://test-usercenter.hbeducloud.com:8088/school_center_dev/1/3b72b9f01a564a2496931206dc43976a.jpg",
            "desc":"老师",
            "is_creator":"1",
            "school_id":"1",
            "user_type_id":"2",
            "username":"赵欣",
          }],
          "title":'群组成员',//标题
          "number":1,//数组长度
          "show":true //是否默认显示人员列表
        }];*/
        this.members = members;
        //1.显示全选（选择）、取消全选（取消选择）按钮
        if(this.chooseBtn){
          for(let i=0;i<this.members.length;i++){
            this.members[i].chooseCount = 0;
            this.members[i].chooseValue = '全选';
            for(let j=0;j<this.members[i].data.length;j++){
              this.members[i].data[j].is_checked=false;
            }
          }
        }
        //2.显示已选人数及人数统计
        if(this.showChoose){
          this.chooseCfg.totalCount = 0;
          for(let i=0;i<this.members.length;i++){
            this.chooseCfg.totalCount+=this.members[i].number;
          }
        }
      },
      getMemberLength(member){
        return member.length;
      },
      addMember(parentIndex,items){
        this.members[parentIndex].data.push(items);
      },
      //显示删除弹框
      isDel(pIndex,index){
        this.pIndex = pIndex;
        this.cIndexS = [];
        this.cIndexS.push(index);
        this.showDelAction = true;
      },
      //“删除”按钮点击事件
      clickDelMenu(){
        this.removeMember(this.pIndex,this.cIndexS);
      },
      //“删除”按钮执行事件
      async removeMember(parentIndex,indexs){
        let del_users='';
        for(let i=0;i<indexs.length;i++){
          let data = this.members[parentIndex].data[indexs[i]];
          del_users += data.account_id+','+data.user_type_id+','+data.school_id+';';
        }
        let res = await contactGroupUserDel(this.groupId,del_users);
        if(res.c==0){
          this.$vux.toast.show({
            type: 'text',
            text: '删除成功'
          });
          this.$emit('on-init');
        }else{
          this.$vux.toast.show({
            type: 'text',
            text: res.m
          });
        }
      },
      bulkEdit(opt){
        if(opt=='delete'){//编辑-批量删除
          this.bulkOptData = this.members[this.pIndex].data;
          this.bulkOptCfg={
            headTitle:'批量编辑',
            searchShow:true
          };
        }else if(opt=='choose'){//选择人员-批量删除
          this.bulkOptData = this.chooseCfg.chooseItems;
          this.bulkOptCfg={
            headTitle:'已选择人员',
            searchShow:true
          };
        }
        for(let i=0;i<this.bulkOptData.length;i++){
          this.bulkOptData[i].is_checked=false;
        }
        this.closeBulkPopup();
      },
      closeBulkPopup(bulkDataIds){
        if(bulkDataIds){
          this.choosePerson(bulkDataIds);
        }
        this.showBulkPopup = !this.showBulkPopup;
      },
      toggleRotate(rotateFlag,rotateAngle){
        if(!rotateFlag){
          let styles = {
            'transform':`rotate(${rotateAngle}deg)`,
            '-ms-transform':`rotate(${rotateAngle}deg)`,	/* IE 9 */
            '-moz-transform':`rotate(${rotateAngle}deg)`, 	/* Firefox */
            '-webkit-transform':`rotate(${rotateAngle}deg)`, /* Safari 和 Chrome */
            '-o-transform':`rotate(${rotateAngle}deg)`, 	/* Opera */
          };
          return styles;
        }else{
          return '';
        }
      },
      borderRadius(radius){
        let styles = {
          '-webkit-border-radius': radius,
          '-moz-border-radius': radius,
          '-ms-border-radius': radius,
          '-o-border-radius': radius,
          'border-radius': radius,
        };
        return styles;
      },
      getSelectedStyle(){
        let count = this.chooseCfg.chooseIds.length;
        let styles = {
//          'width':3*count+ 'rem'
          'width':3.2*count+ 'rem'
        };
        return styles;
      },
      mySearch(){
        this.keyword = this.search.search_txt;
        this.filterFlag = true;
      },
      //前端-筛选过滤数据
      filterData(data){
        if(this.filterFlag){
          let returnVal = [];
          for(let i=0;i<data.length;i++){
            if(data[i].username.search(this.keyword)!=-1){
              returnVal.push(data[i]);
            }
          }
          return returnVal;
        }else{
          return data;
        }
      },
      toggleCheckAll(pIndex){
        let changeVal = true;
        if(this.members[pIndex].chooseValue=='全选'){
          changeVal = true;
          this.members[pIndex].chooseCount = this.members[pIndex].number;
          this.members[pIndex].chooseValue='取消全选';
        }else{
          changeVal = false;
          this.members[pIndex].chooseCount = 0;
          this.members[pIndex].chooseValue='全选';
        }
        for(let i=0;i<this.members[pIndex].data.length;i++){
          let obj = this.members[pIndex].data[i];
          obj.is_checked = changeVal;
          this.$set(this.members[pIndex].data,i,obj);
        }
        this.choosePerson();
      },
      toggleCheckOne(pIndex,cIndex){
        let obj = this.members[pIndex].data[cIndex];
        if(obj.is_checked){
          this.members[pIndex].chooseCount-=1;
        }else{
          this.members[pIndex].chooseCount+=1;
        }
        if(this.members[pIndex].chooseCount == this.members[pIndex].number){
          this.members[pIndex].chooseValue = '取消全选';
        }else if(this.members[pIndex].chooseCount==0){
          this.members[pIndex].chooseValue = '全选';
        }
        //console.log(this.members[pIndex].chooseCount);
        obj.is_checked = !obj.is_checked;
        this.$set(this.members[pIndex].data, cIndex, obj);
        this.choosePerson();
      },
      choosePerson(bulkDataIds){
        this.chooseCfg.chooseIds = [];
        this.chooseCfg.chooseItems = [];
        for(let i=0;i<this.members.length;i++){
          for(let j=0;j<this.members[i].data.length;j++){
            let value = this.members[i].data[j].account_id;
            if(bulkDataIds){
              if(bulkDataIds.indexOf(value)!=-1){
                this.members[i].data[j].is_checked = true;
              }else{
                this.members[i].data[j].is_checked = false;
              }
            }
            if(this.members[i].data[j].is_checked && this.chooseCfg.chooseIds.indexOf(value)==-1){
              this.chooseCfg.chooseIds.push(this.members[i].data[j].account_id);
              this.chooseCfg.chooseItems.push(this.members[i].data[j]);
            }
          }
        }
        this.chooseCfg.chooseCount = this.chooseCfg.chooseIds.length;
      },
      //操作按钮事件（取消、确定）
      optClick(opt){
        if(opt=='cancel'){
          this.$emit('on-cancel');
        }else if(opt=='sure'){
          this.$emit('on-sure',this.chooseCfg.chooseItems);
        }
      }
    },
    watch:{
      origin:{
        immediate:true,
        handler:function(val){
          if(val && val.length>0){
            this.fillMembers(val);
            //console.log(JSON.stringify(val));
          }
        },
      }
    }
  }
</script>

<style scoped>
  @import "./member.css";
  .search{margin:1rem 0;}
</style>
