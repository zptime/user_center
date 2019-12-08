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
  export default {
    data(){
      return {
        head:{
          icon: 'return',
          title: '选择人员',
          more: false
        },
        showTip:false,//是否显示无关联班级提示
        classData:[],//班级用户列表
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
        let obj = {
          "id":1,
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
        };
        this.$set(this.classData,0,obj);
      },

      //“取消”事件回调
      optCancel(){
        alert('“取消”事件回调');
      },

      //“确定”事件回调
      async optSure(data){
        //data为返回数据
        alert('“确定”事件回调'+data);
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
