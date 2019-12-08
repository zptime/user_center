<!--任教班级界面-->
<template>
  <div>
    <head-top :head="head">
      <img slot="right" src="../../../images/icon_nav_add.png" @click="goAddClass"/>
    </head-top>
    <div class="contentBox" v-cloak>
      <div :style="{marginTop:'0.75rem'}">
        <div v-for="(item,index) in classList">
          <div class="itemView" :style="getLineView(item,index)" @click="clickClass(item)">
            <span class="leftTxt">{{item.class_name}}</span>
            <span class="rightTxt" @click.stop="clickToDelete(item,index)">删除</span>
          </div>
          <div class="clb"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import {getMyClasses,deleteTeacherClass} from '../../../service/getData.js'
   import HeadTop from '../../../components/Head.vue'
    export default {
        name: "teach-classes",
        components:{
          HeadTop
        },
        data(){
          return {
            classList:[],
            head:{
              icon: 'return',
              title: '任教班级',
              more: true
            },
          }
        },
        methods:{
          clickClass(item){
            let str = JSON.stringify(item);
            this.$router.push({
              name:'classCode',
              params:{
                classObj:str,
              }
            })
          },
          showTip(str){
            if ((typeof str) != 'string'){
              return
            }
            this.$vux.toast.show({
              type: 'text',
              text: str
            })
          },
          //进入设置任教班级界面
          goAddClass(){
            this.$router.push({
              name:'addClasses',
            })
          },
          clickToDelete(item,index){
            if (item.is_master == '1'){
              this.showTip('不能删除自己管理的班级');
              return;
            }
            this.deleteTeacherClass(item,index);
          },
          //删除任教班级
          async deleteTeacherClass(item,index){
            let deleteClassids = '[' + item.class_id + ']'
            let res = await deleteTeacherClass(deleteClassids);
            if (res.c == 0){
              this.classList.splice(index,1);
              this.showTip('删除成功');
            }else{
              this.showTip(res.m);
            }
          },
          //获取老师的任教班级
          async getMyClasses(){
            let res = await getMyClasses('');
            if (res.c == 0){
              this.classList = res.d;
            }else{
              this.$vux.toast.show({
                type: 'text',
                text: res.m
              })
            }
          },
          getLineView(item,index){
            // let hideLine = index == this.classList.length - 1 ? true:false
            // if (hideLine){
            //   return {
            //   }
            // }
            return {
              borderBottom:'1px solid #eeeeee'
            }
          },
        },
        created(){
          this.getMyClasses();
          document.title = '任教班级';
        },
    }
</script>

<style scoped>
  .itemView {height: 2.25rem;background-color: white;}
  .leftTxt {font-size: 0.75rem;color: #444444;float: left;margin-left: 0.75rem;line-height: 2.25rem;}
  .rightTxt {font-size: 0.75rem;color: #F74747;float: right;margin-right: 0.75rem;line-height: 2.25rem;}
  .clb {clear: both;}
</style>

<!--{-->
<!--"class_id": "string",-->
<!--"class_name": "string",-->
<!--"class_alias": "string"-->
<!--"is_master":"string"-->
<!--}-->
