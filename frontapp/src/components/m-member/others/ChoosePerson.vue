<template>
  <div class="member">
    <head-top :head="head"></head-top>
    <div class="contentBox" v-cloak>
      <div class="content" v-if="showTip">
        <div><img src="../../../images/icon-warning.png"></div>
        <div class="tip">您没有关联任何班级!</div>
        <div>请在个人中心 > 任教设置 中关联您所需要的班级</div>
      </div>
      <div class="person" v-else>
        <div class="list">
          <group-member :origin="classData" :toggleBtn="true" :chooseBtn="true"
                        :showSearch="true" :showChoose="true" :showOptBtn="true"
                        @on-cancel="optCancel" @on-sure="optSure"
                        :setMemberStyle="setMemberStyle">
          </group-member>
        </div>
      </div>
    </div>
  </div>
</template>

<script type="es6">
  import HeadTop from '@/components/Head.vue'
  import GroupMember from '@/components/m-member/GroupMember.vue'
  import { getClassList,contactGroupCreate } from '../../../service/getData'
  import { contactGroupInviteAgain,contactGroupUserInvite,contactClassUserList } from '../dealData'
  export default {
    data(){
      return {
        head:{
          icon: 'return',
          title: '选择人员',
          more: false
        },
        showTip:false,//是否显示无关联班级提示
        groupId:'',//小组名称
        classData:[],//班级用户列表
        groupName:[],//创建群组时的群组名称
        classItems:[],//关联的班级ID
        setMemberStyle:{
          'top':'9.1rem',
          'bottom':'4rem'
        }
      }
    },
    components: {
      HeadTop,
      GroupMember,
    },
    created(){
      this.initData();
    },
    methods:{
      initData(){
        if(this.$route.query.groupId){//传入群组id
          this.groupId = this.$route.query.groupId;
          this.getInviteData();
        }else if(this.$route.query.gName){//传入群组名称
          this.groupName = this.$route.query.gName;
          this.getClassList();
        }
      },

      //获取关联班级
      async getClassList(){
        let res = await getClassList();
        if(res.c==0){
          this.classItems = res.d;
          if(this.classItems.length==0){
            this.showTip = true;
          }
          this.getClassMember();
        }else{
          this.$vux.toast.show({
            type: 'text',
            text: res.m
          });
        }
      },

      //获取关联班级的学生列表
      async getClassMember(){
        this.classData = [];
        for(let i=0;i<this.classItems.length;i++){
          let res = await contactClassUserList(this.classItems[i].class_id);
          if(res.c==0){
            let students = [];
            for(let i=0;i<res.d.length;i++){
              if(res.d[i].user_type_id=='1'){
                students.push(res.d[i]);
              }
            }
            this.classData.push({
              "id":this.classItems[i].class_id,
              "data": students,
              "title":this.classItems[i].class_name,
              "number":students.length,
              "show":true
            });
          }else{
            this.$vux.toast.show({
              type: 'text',
              text: res.m
            });
          }
        }
      },

      //获取尚可邀请的用户列表
      async getInviteData(){
        let res = await contactGroupInviteAgain(this.groupId);
        if(res.c == 0){
          this.classData = [];
          for(let i=0;i<res.d.student.length;i++){
            this.classData.push({
              "id":res.d.student[i].class_id,
              "data": res.d.student[i].students,
              "title":res.d.student[i].class_name,
              "number":res.d.student[i].students.length,
              "show":true
            });
          }
        }else{
          this.$vux.toast.show({
            type: 'text',
            text: res.m
          });
        }
      },

      //“取消”事件回调
      optCancel(){
        this.$router.back();
      },

      //“确定”事件回调
      async optSure(data){
        let invite_users='';
        for(let i=0;i<data.length;i++){
          invite_users += data[i].account_id+','+data[i].user_type_id+','+data[i].school_id+';';
        }
        if(this.groupId){//已有群组邀请用户
          this.addUserInvite(invite_users);
        }else if(this.groupName){//创建群组邀请用户
          this.createUserInvite(data,invite_users);
        }
      },

      //已有群组邀请用户
      async addUserInvite(invite_users){
        let res = await contactGroupUserInvite(this.groupId,invite_users);
        if(res.c==0){
          this.$vux.toast.show({
            type: 'text',
            text: '添加成功'
          });
          this.$router.back();
        }else{
          this.$vux.toast.show({
            type: 'text',
            text: res.m
          });
        }
      },

      //创建群组邀请用户
      async createUserInvite(data,invite_users){
        if(data.length>=2){
          let res = await contactGroupCreate(this.groupName,invite_users);
          if(res.c==0){
            this.$vux.toast.show({
              type: 'text',
              text: '创建群组成功'
            });
            this.$router.push({
              name:'phoneList',
              query:{
                navFlag:2
              }
            });
          }else{
            this.$vux.toast.show({
              type: 'text',
              text: res.m
            });
          }
        }else{
          this.$vux.toast.show({
            type: 'text',
            text: '请至少选择两人'
          });
        }

      },


    }
  }
</script>

<style scoped>
  .content{
    text-align: center;
    margin-top:4rem;
    color:#444;
    font-size: 0.8rem;
    padding: 0 0.75rem;
  }
  .tip{
    margin:0.5rem 0 0.3rem 0;
  }
</style>
