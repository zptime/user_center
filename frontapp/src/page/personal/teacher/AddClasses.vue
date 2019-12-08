<template>
  <div>
    <head-top :head="head"></head-top>
    <div class="contentBox" v-cloak>
      <group label-width="5em" gutter="0" :style="{marginTop:'0.75rem'}">
        <div v-for="grade in gradeList" @click="goChooseClass(grade)">
          <cell  primary="content" :is-link="true" :title="grade.grade_name" :value='getMyTeachClassesTxt(grade)'></cell>
          <div class="myCellSeperate"></div>
        </div>
      </group>
    </div>
    <popup :style="{backgroundColor:'white'}" v-model="isShowPopup" width="100%" height="100%" position="right" :show-mask=false :hide-on-blur="false">
      <add-class ref="addClassView"  @on-netWorkFinished="chooseViewFinish" @on-cancel="cancelClick"></add-class>
    </popup>
  </div>
</template>

<script>
    import Cell from 'vux/src/components/cell/index.vue'
    import Group from 'vux/src/components/group/index.vue'
    import {getSchoolClasses,getSchoolGrades} from '../../../service/getData.js'
    import HeadTop from '@/components/Head.vue'
    import Popup from 'vux/src/components/popup/index.vue'
    import AddClass from "./AddClass";

    export default {
        name: "add-classes",
        components:{
          AddClass,
          Cell,
          Group,
          HeadTop,
          Popup
        },
        data(){
          return {
            isShowPopup:false,
            handleGrade:undefined,
            head:{
                icon: 'return',
                title: '添加任教班级',
                more: false
              },
              gradeList:[],
              classList:[],
          }
        },
        methods:{
          cancelClick(data){
            this.isShowPopup = false;
            this.handleGrade.teach_classes = data;
          },
          chooseViewFinish(){
            this.isShowPopup = false;
          },
          goChooseClass(grade){
            this.isShowPopup = true;
            this.handleGrade = grade;
            this.$refs.addClassView.dealData(this.handleGrade.teach_classes);
          },
          getMyTeachClassesTxt(grade){
            let classTxt = '';
            if (!grade.teach_classes) return;
            for(let i=0;i<grade.teach_classes.length;i++){
              let classObj = grade.teach_classes[i];
              if (classObj.is_teach == '1'){
                classTxt += classObj.class_name;
                classTxt += ',';
              }
            }
            if(classTxt.length > 0){
              classTxt = classTxt.substring(0,classTxt.length - 2);
            }
            //限制长度
            let maxIndex = 16;
            if(classTxt.length > maxIndex){
              classTxt = classTxt.substring(0,maxIndex);
              classTxt += '...';
            }
            //添加默认值
            return classTxt.length > 0 ? classTxt : '未添加';
          },
          //获取教师教授的班级
          async getTeachClasses(){
            let  res = await getSchoolClasses('','0');
            if(res.c == 0){
              let arr = [];
              for(let i=0;i<res.d.length;i++){
                let obj = res.d[i];
                obj.last_is_teach = obj.is_teach;
                arr.push(obj);
              }
              this.classList = arr;
              this.dealData();
              /*
              *  {
                "class_alias": "",
                "class_name": "101班",
                "is_teach": 1,
                "last_is_teach":1,//记录之前的选择情况，是否添加为任教班级
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
            }
          },
          //获取学校所有的年级
          async getSchoolGrades(){
            let res = await getSchoolGrades();
            if (res.c == 0){
              let arr = [];
              for (let i=0;i<res.d.length;i++){
                let obj = res.d[i];
                obj.teach_classes = [];
                arr.push(obj);
              }
              this.gradeList = arr;
              this.dealData();
              /*
              *{
              "period_grade_num": 1,
              "school_period": 1,
              "grade_num": 1,
              "grade_name": "一年级",
              "school_years": 6,
              "class_amount": 1,
              "id": 1,
              "teach_classes":[],
              "isShowPopup":false,
              * */
            }
          },
          //处理数据
          dealData(data){
            if (this.gradeList.length == 0 || this.classList.length == 0){
              return;
            }
            for (let i =0;i<this.gradeList.length;i++){
              let obj = this.gradeList[i];
              let  arr = [];
              for (let j =0;j<this.classList.length;j++){
                let classObj = this.classList[j];
                if(classObj.grade_num == obj.grade_num){
                  arr.push(classObj);
                  continue;
                }
              }
              obj.teach_classes = arr;
            }
          },
        },
        created(){
            this.getSchoolGrades();
            this.getTeachClasses();
            document.title = '添加任教班级';
        },
    }
</script>

<style scoped>
  .myCellSeperate{height: 1px;width: 100%;background-color: #EEEEEE;}

</style>
