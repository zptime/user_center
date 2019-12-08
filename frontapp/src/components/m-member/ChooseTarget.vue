<template>
  <div>
    <div class="contentBox" v-cloak v-if="showPage">
      <div class="tip-content" v-if="showTipNone">
        <div><img src="../../images/icon-warning.png"></div>
        <div class="tip-none">您没有关联任何班级!</div>
        <div class="tip-none">请在个人中心 > 任教设置 中关联您所需要的班级</div>
      </div>
      <div class="choose-list" v-else>
        <div class="nav borderRadius clb">
          <span :class="{'active':navId==item.id}" v-for="item in navItem" @click="changeNav(item.id)">
            {{ item.item }}
          </span>
        </div>
        <div class="tip">
          注：班级和小组，两种模式只能选择一种作为{{ title }}对象
        </div>
        <div class="list member" v-if="showList">
          <div class="item">
            <div class="item-title clb">
              <span class="opt left">
                <span class="operate right" :class="checkVal=='全选'?'check_all':'deselect_all'" @click="toggleCheckAll">{{ checkVal }}</span>
              </span>
            </div>
            <div v-for="(itemData,index) in dataList">
              <div class="item-detail clb" :class="{'item-border-none': index==dataList.length-1}">
                <span class="other-left" @click="toggleCheckOne(index)">
                  <span class="opt left">
                    <img class="opt-check" src="./images/icon-selected.png" v-if="itemData.is_checked==true">
                    <img class="opt-check" src="./images/icon-part-selected.png" v-if="itemData.is_checked=='partial'">
                    <img class="opt-check" src="./images/icon-not-selected.png" v-if="itemData.is_checked==false"/>
                  </span>
                  <span class="username left">{{ itemData.name }}</span>
                </span>
                <span class="other-right" @click="goChoose(index)">
                  <span class="toggle right">
                    <img src="./images/icon-arrow-r.png">
                  </span>
                  <span class="number right">{{ itemData.total }}</span>
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
      <popup v-model="showPopup" width="100%" height="100%" position="right" :show-mask=false>
        <chose-target :head-title="headTitle" :bulk-data="bulkData" :data-index="dataIndex"
          @on-close="togglePopup" @on-sure="changeTarget">
        </chose-target>
        <!--<chose-order :head-title="headTitle" :bulk-data="bulkData" :data-index="dataIndex"-->
                      <!--@on-close="togglePopup" @on-sure="changeTarget">-->
        <!--</chose-order>-->
      </popup>
    </div>
  </div>
</template>

<script type="es6">
  import Popup from 'vux/src/components/popup/index.vue'
  import ChoseTarget from './others/ChoseTarget.vue'
  import ChoseOrder from './others/ChoseOrder.vue'
  import global from '../Global.vue'
  import { mapState,mapMutations } from 'vuex'
  import { getClassList,commonClassStudentList,getBookCluster,contactGroupUserList } from '../../service/getData.js'
  export default {
    props:{
      title: {
        type: String,
        default: '通知'
      },
      hasChose: {
        type: Boolean,
        default: false
      },
    },
    data () {
      return {
        navId:1,//导航栏ID
        navItem:[{'item':'班级','id':1},{'item':'小组','id':2}],
        classList:[],//班级数据列表
        groupList:[],//小组数据列表
        dataList:[],//数据列表
        chooseNum:0,//已选班级个数
        checkVal:'全选',//全选、取消全选文字
        showPage:false,//是否显示页面
        showList:false,//是否显示列表
        showTipNone:false,//是否显示无关联提示
        showPopup:false,//是否显示popup
        headTitle:'',//头部的title
        bulkData:[],//传递到子页的数据
        dataIndex:-1,//传递到子页的数据序号
      }
    },
    components: {
      Popup,
      ChoseTarget,
      ChoseOrder,
    },
    computed:{
      ...mapState([
        'class_target',
        'group_target',
      ])
    },
    created(){
      this.initData();
    },
    methods:{
      ...mapMutations([
        'CLASS_TARGET',
        'GROUP_TARGET',
      ]),

      //初始化数据
      initData(){
        if(this.navId == 1){
          this.getClassList();
        }else if(this.navId==2){
          this.getClusterList();
        }
      },

      //获取班级列表
      async getClassList(){
        let res = await getClassList();
        if(res.c == 0){
          //res.d = [];
          this.showPage = true;
          if(res.d==0){
            this.showTipNone = true;
          }
          this.classList = [];
          for(let i=0;i<res.d.length;i++){
            let resS = await commonClassStudentList(res.d[i].class_id);
            if(resS.c==0){
              this.classList.push({
                'id':res.d[i].class_id,
                'name':res.d[i].class_name,
                'total':parseInt(res.d[i].student_count),
                'is_checked':global.checkStatus.deselect_all,
                'count':0,
                'data':[],
              });
              this.classList[i].data = resS.d;
              for(let j=0;j<this.classList[i].data.length;j++){
                this.classList[i].data[j].is_checked = false;
              }
            }
          }
          this.dataList = this.classList;
          this.copyData();
          this.showList = true;
        }else{
          this.$vux.toast.show({
            type: 'text',
            text: res.m
          });
        }
      },

      //获取群组列表-只包括我创建的群组
      async getClusterList(){
        let res = await getBookCluster();
        if(res.c == 0){
          this.groupList = [];
          for(let i=0;i<res.d.created.length;i++){
            let resG = await contactGroupUserList(res.d.created[i].grp_id);
            if(resG.c==0){
              this.groupList.push({
                'id':res.d.created[i].grp_id,
                'name':res.d.created[i].grp_name,
                'total':'',
                'is_checked':global.checkStatus.deselect_all,
                'count':0,
                'data':[],
              });
              for(let j=0;j<resG.d.length;j++){
                if(resG.d[j].user_type_id==1){
                  resG.d[j].is_checked=false;
                  this.groupList[i].data.push(resG.d[j]);
                }
              }
              this.groupList[i].total = this.groupList[i].data.length;
            }
          }
          this.dataList = this.groupList;
          this.copyData(this.groupList);
          this.$vux.loading.hide();
          this.showList = true;
        }else{
          this.$vux.loading.hide();
          this.$vux.toast.show({
            type: 'text',
            text: res.m
          });
        }
      },

      //赋值操作
      copyData(data){
        if(this.navId==1){
          this.CLASS_TARGET(data);
        }else if(this.navId==2){
          this.GROUP_TARGET(data);
        }
      },

      //导航栏切换
      changeNav(id){
        this.navId = id;
        this.chooseNum=0;
        this.checkVal='全选';
        this.showList = false;
        this.initData();
      },

      //全选、取消全选事件
      toggleCheckAll(){
        if(this.checkVal=='全选'){
          this.chooseNum = this.dataList.length;
          for(let i=0;i<this.dataList.length;i++){
            this.dataList[i].is_checked = global.checkStatus.check_all;
            this.dataList[i].count = this.dataList[i].total;
            for(let j=0;j<this.dataList[i].data.length;j++){
              this.$set(this.dataList[i].data[j],'is_checked',true);
            }
          }
        }else{
          this.chooseNum = 0;
          for(let i=0;i<this.dataList.length;i++){
            this.dataList[i].is_checked = global.checkStatus.deselect_all;
            this.dataList[i].count = 0;
            for(let j=0;j<this.dataList[i].data.length;j++){
              this.$set(this.dataList[i].data[j],'is_checked',false);
            }
          }
        }
        this.copyData(this.dataList);
      },

      //选择、取消选择事件
      toggleCheckOne(index){
        if(this.dataList[index].is_checked==true){
          this.chooseNum-=1;
          for(let i=0;i<this.dataList[index].data.length;i++){
            this.$set(this.dataList[index].data[i],'is_checked',false);
          }
          this.dataList[index].is_checked = false;
        }else{
          this.chooseNum+=1;
          for(let i=0;i<this.dataList[index].data.length;i++){
            this.$set(this.dataList[index].data[i],'is_checked',true);
          }
          this.dataList[index].is_checked = true;
        }
        this.copyData(this.dataList);
      },

      //进入通知对象详情页面
      goChoose(index){
        this.headTitle = this.dataList[index].name;
        this.dataIndex = index;
        this.bulkData = this.dataList[index].data.filter(item => item);
        this.togglePopup();
      },

      togglePopup(){
        this.showPopup = !this.showPopup;
      },

      changeTarget(data){
        this.dataList[data.index].count = data.count;
        this.dataList[data.index].data = data.bulkData;
        if(data.count==0){
          this.dataList[data.index].is_checked = global.checkStatus.deselect_all;
        }else if(data.count==this.dataList[data.index].total){
          this.dataList[data.index].is_checked = global.checkStatus.check_all;
        }else{
          this.dataList[data.index].is_checked = global.checkStatus.partial_select;
        }
        this.togglePopup();
      },

      //底部操作按钮事件
      async optClick(opt){
        if(opt=='cancel'){//取消
          this.$emit('on-cancel');
        }else{
          let data = [];
          for(let i=0;i<this.dataList.length;i++){
            for(let j=0;j<this.dataList[i].data.length;j++){
              if(this.dataList[i].data[j].is_checked){
                data.push(this.dataList[i].data[j]);
              }
            }
          }
          this.copyData(this.dataList);
          this.$emit('on-sure',data);
        }
      },
    },
    watch:{
      chooseNum(val){
        if(val==this.dataList.length){
          this.checkVal = '取消全选';
        }else if(val==0){
          this.checkVal = '全选';
        }
      }
    }
  }
</script>

<style scoped>
  @import "./member.css";
  .contentBox{
    background-color: #fff;
    bottom:0;
  }

  .nav{
    width:10rem;
    text-align: center;
    margin: 1rem auto 0 auto;
    border: 1px solid #4685ff;
  }
  .nav span{
    display: inline-block;
    width: 50%;
    height: 1.5rem;
    line-height: 1.5rem;
    font-size: 0.6rem;
    color: #444;
    float:left;
  }
  .nav span:last-child{
    float: right;
  }
  .nav span.active{
    background-color: #4685ff;
    color:#fff;
  }

  .tip{
    font-size: 0.6rem;
    color:#aaa;
    margin:1.5rem 0.75rem 0.5rem 0.75rem;
  }

  .list{
    position: fixed;
    width: 100%;
    background-color: #fff;
    top: 7.4rem;
    bottom: 4rem;
    z-index: 9;
    overflow-y: auto;
    -webkit-overflow-scrolling : touch;
  }

  .list .username{
    margin-left:0.75rem !important;
  }
  .list .item-detail .number{
    font-size: 0.75rem;
    color:#aaa;
  }
  .list .item-detail .toggle img{
    height: 0.85rem;
    width: 0.85rem;
    margin: 0.95rem 0 0.95rem 0.5rem;
  }
</style>
