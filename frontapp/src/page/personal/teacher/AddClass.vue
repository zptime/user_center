<template>
  <div>
    <head-top :head="head">
       <img slot="left" src="../../../images/icon-return.png" v-tap.stop="{methods:myCustomBack}"/>
    </head-top>
    <div class="contentBox" v-cloak>
      <div :style="{height:'0.75rem'}"></div>
      <div :style="{overflow:'scroll'}"  v-for="classObj in classList">
        <div class="classMsg clb" @click.stop="choose(classObj)">
          <span>{{classObj.class_name}}</span>
          <img class="choosedFile" v-if="classObj.last_is_teach == '1'" src="../../../images/icon-greenCheckMark.png"/>
        </div>
      </div>
      <div class="btnOpt">
        <div class="btnCommon btnBottomOpt boxShadowGray clb">
          <span class="btn_cancel left" @click.stop="optClick('cancel')">取消</span>
          <span class="btn_divide"></span>
          <span class="btn_sure right" @click.stop="optClick('sure')">确定</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
    import {addTeacherClass,deleteTeacherClass} from '../../../service/getData.js'
    import HeadTop from '../../../components/Head.vue'

    export default {
        name: "add-class",
        components:{
          HeadTop,
        },
        data(){
          return {
            classList:[],
            isDeleting:undefined,//undefined 没有删除操作 true 正在删除中  false 已完成删除
            isAdding:undefined,//同上
            head:{
              icon: 'return',
              title: '',
              more: false
            },
          }
    },
    methods:{
      myCustomBack(){
        this.optClick('cancel');
      },
      async deleteTeacherClass(){
        let arr =[];
        for(let i=0;i<this.classList.length;i++){
          let obj = this.classList[i];
          if(obj.last_is_teach == '0' && obj.is_teach == '1'){
            arr.push(obj.id);
          }
        }
        if(arr.length == 0){
          return;
        }
        this.isDeleting = true;
        let str = '[' + arr.join(',') + ']';

        let res = await deleteTeacherClass(str);
        this.isDeleting = false;
        if (res.c == 0){
          this.dealDataAfterNetwork();
        }
      },

      async addTeacherClass(){
        let arr = [];
        for(let i=0;i<this.classList.length;i++){
          let obj = this.classList[i];
          if(obj.last_is_teach == '1' && obj.is_teach == '0'){
            arr.push(obj.id);
          }
        }
        if(arr.length == 0){
          return;
        }
        let str = '[' + arr.join(',') + ']';
        this.isAdding = true;
        let res = await addTeacherClass(str);
        this.isAdding = false;
        if (res.c == 0){
          this.dealDataAfterNetwork();
        }
      },
      dealDataAfterNetwork(){
        //是否正在增加操作
        let isAddAction = true;
        if(this.isAdding != 'undefined' && this.isAdding == 'true' ){
          isAddAction = false;
        }
        //是否正在删除操作
        let isDeleteAction = true;
        if (this.isDeleting != 'undefined' && this.isDeleting == 'true'){
          isDeleteAction = false;
        }
        if (!isAddAction || !isDeleteAction){
          return;
        }
        //数据处理
        for (let i=0;i<this.classList.length;i++){
          let obj = this.classList[i];
          obj.is_teach = obj.last_is_teach;
        }
        this.$emit('on-netWorkFinished',this.classList);
      },
      optClick(flagTxt){
        let flag = flagTxt == 'cancel'? false:true;

        //点击确认
        if (flag){
          this.addTeacherClass();
          this.deleteTeacherClass();
          return;
        }
        //点击取消
        for(let i=0;i<this.classList.length;i++){
          let obj = this.classList[i];
          obj.last_is_teach = obj.is_teach;
        }
        this.$emit('on-cancel',this.classList);
      },
      //选择或者取消
      choose(classObj){
        if(classObj.last_is_teach == '1'){
          classObj.last_is_teach = '0';
        }else{
          classObj.last_is_teach = '1';
        }
      },
      //处理数据
      dealData(data){
        this.classList = data.slice(0);
        let classobj = this.classList[0];
        this.head.title = classobj.grade_name;
      }
    },
    }
</script>

<style scoped>
  .classMsg {height: 2.25rem;border-bottom: 1px solid #EEEEEE;}
  .clb {clear: both;}
  .classMsg span{font-size: 0.75rem;line-height: 2.25rem;float: left;display: inline-block;margin-left: 0.75rem;}
  .classMsg img{display: inline-block;float: right;margin-right: 0.75rem;width: 0.75rem;height: 0.75rem;margin-top:0.75rem; }

  .btnOpt {position: fixed;bottom: 0;}
  .btnOpt .btnBottomOpt{background-color: white;}
</style>

/*
*  {
"class_alias": "",
"class_name": "101班",
"is_teach": 1,
"class_code": "000323",
"grade_num": 1,
"enrollment_year": 2017,
"grade_name": "一年级",
"class_num": 1,
"student_amount": 0,
"id": 323,
"teacher_data": []
},
* */
