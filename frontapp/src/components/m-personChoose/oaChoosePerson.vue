<template>
  <div>
    <headTop :head="head">
      <img slot="left" src="../../images/icon-return.png" @click="customBack"/>
    </headTop>
    <div class="contentBox" v-cloak>
      <div class="topSearch" v-show="setting.isShowSearch">
        <search></search>
      </div>
      <div v-for="(departMentItem,index) in choosedDepartmentArray" :style="getTopTitleDistanceToTop">
        <div>
          <img v-if="index != 0" :style="{width:'0.6rem',height:'0.6rem'}" src="./images/icon-rightGrayArrow.png"/>
          <span :style="departmentTxtColor(index == choosedDepartmentArray.length - 1)" @click="chooseDepartment(departMentItem,index)">{{departMentItem.name}}</span>
        </div>
      </div>
      <div class="department">
        <ul class="departmentView">
          <!--全选视图-->
          <li>
            <div class="allChooseView whiteBg clb" @click="chooseAll" v-if="setting.isShowChooseAll">
              <img src="./images/icon_choosed.png" v-if="isChoosedAll"/>
              <img src="./images/icon_choosed_notAll.png" v-else-if="isChoosedPerson"/>
              <img src="./images/icon_choosed_not.png" v-else/>
              <span>全选</span>
            </div>
          </li>
          <!--部门视图-->
          <li class="departmentItem" v-for="(department,index) in secondLevelDepartment">
            <div @click="clickDepartment(department)" :style="{display:'inline-block',width:'80%'}">
              <span class="selectView" v-if="setting.isMutiableSelect">
                <img src="./images/icon_choosed.png" v-if="department.isSelected"/>
                <img src="./images/icon_choosed_not.png" v-else/>
              </span>
              <span class="nameLabel">{{department.name.length > 15?department.name.substring(0,15) + '...' : department.name}}</span>
              <span class="moreMsgLabel">{{department.moreMsg}}</span>
            </div>
            <span class="subDepartmentTip" :style="goNextTipColor(department)" @click="goNextDepartment(department)">| 下级</span>
            <div class="clb"></div>
          </li>
        </ul>
      </div>
      <!--人物视图-->
      <div class="person whiteBg" :style="personViewToBottom">
        <ul class="personView">
          <li class="perosonItem" v-for="(person,index) in allPersonArray" @click="choosePerson(person)">
           <span class="selectView">
             <img src="./images/icon_choosed.png" v-if="person.isSelected"/>
             <img src="./images/icon_choosed_not.png" v-else/>
           </span>
            <span class="nameLabel">{{person.name.length > 8 ? person.name.substring(0,7)+'...':person.name}}</span>
            <span class="moreMsgLabel">{{person.moreMsg}}</span>
            <img class="headView" :src="person.image_url" v-if="person.image_url">
            <img class="headView" src="./images/icon-default-personAvatar.png" v-else>
          </li>
        </ul>
      </div>
    </div>
    <!--底部选择人的头像视图-->
    <div ref="bottomBar" class="choosePerBottomView" v-if="setting.isShowBottomBar">
      <div :style="{backgroundColor:'rgb(170,170,170)',height:'1px',width:'100%'}"></div>
      <scroller lock-y scrollbar-x class="bottomScrollView">
        <div :style="getBottomStyle">
              <span v-for="(person,index) in hasChoosedPersonArr"  @click="cancelChoose(person)">
                  <span class="bottomChoosedPerItem" v-if="person.object_type == 2">
                    <img class="headView" :src="person.image_url" v-if="person.image_url">
                    <img class="headView" src="./images/icon-default-personAvatar.png" v-else>
                    <img class="headViewDelete" src="./images/icon-delete.png"/>
                  </span>
                  <span class="departmentChoosedItem" v-else>
                    <span>{{person.name.length > 4 ? person.name.substring(0,4) + '...' : person.name}}</span>
                    <img class="headViewDelete" src="./images/icon-delete.png"/>
                  </span>
              </span>
        </div>
      </scroller>
      <div class="clb" :style="{display:'inline-block'}">
      </div>
      <span class="makeSureButton" @click="makeSureClick">确定</span>
    </div>
  </div>
</template>

<script>
  import Search from 'vux/src/components/search/index.vue'
  import headTop from '../../components/Head.vue'
  import Scroller from 'vux/src/components/scroller/index.vue'
  import {getSendTarget} from './oaGetDepartmentData.js'

    export default {
        name: "oa-choose-person",
        components:{
          Search,
          headTop,
          Scroller,
        },
        props:{
          outSetting:{
            type:Object,
            default: ()=> {
              // //是否显示全选
              // isShowChooseAll=true,
              // //已选人
              // lastChoosedPersonArr=[],
              // //是否显示底部已选人物的栏目
              // isShowBottomBar=true,
              // //是否显示搜索
              // isShowSearch=true
              //是否是多选
              //isMutiableSelect=true
              //从哪个界面来的
              // fromPage:'',
            }
          },
        },
    /**
     * "image_url":"",
     "object_type":"2",
     "pId":1,
     "name":"张海",
     "id":6
     "isSelected":false
     "moreMsg":""   //（个数）或者 没有
     */
    data () {
          return{
            //导航栏数据
            head:{},
            //所有数据
            allData:[],
            //当前界面部门的数据
            currentDepartment:{},
            //最初进入界面显示的下级部门的数据
            secondLevelDepartment:[],
            //选择的子级部门的数组
            choosedDepartmentArray:[],
            //是否全选了
            isChoosedAll:false,
            //所有人的数据
            allPersonArray:[],
            //已选的数据
            hasChoosedPersonArr:[],
            //界面设置数据
            setting:this.outSetting,
          }
        },
        methods:{
          //顶部部门选择
          chooseDepartment(departMentItem,index){
            let arrCount = this.choosedDepartmentArray.length;
            if(index ==  arrCount - 1) return;
            this.choosedDepartmentArray.splice(index + 1,arrCount - 1 - index);
            this.initData();
          },
          //底部选择取消选中
          cancelChoose(person){
            person.isSelected = !person.isSelected;
            for(let i = 0;i < this.hasChoosedPersonArr.length;i++){
              let item = this.hasChoosedPersonArr[i];
              if(item.id == person.id){
                this.hasChoosedPersonArr.splice(i,1);
              }
            }
          },
          //选择确定
          makeSureClick(){
            //to do

            if(this.hasChoosedPersonArr.length == 0){
              this.$vux.toast.show({
                type: 'text',
                text: '请选择发送对象'
              })
              return;
            }
            this.$emit('on-makeSureClick',this.hasChoosedPersonArr);
          },
          //点击部门
          clickDepartment(department){
            //单选
            if(!this.setting.isMutiableSelect){
              this.hasChoosedPersonArr.push(department);
              this.makeSureCLick();
              return;
            }
            //多选
            department.isSelected = !department.isSelected;
            if(department.isSelected){
              this.hasChoosedPersonArr.push(department);
              return;
            }
            for(let i = 0;i < this.secondLevelDepartment.length;i++){
              let item = this.secondLevelDepartment[i];
              if(item.id == department.id){
                this.hasChoosedPersonArr.splice(i,1);
                break;
              }
            }
          },
          //点击下级
          goNextDepartment(department){
            let num = department.moreMsg.substr(1,1);
            num = parseInt(num);
            if(num == 0 || department.isSelected) return;
            //to do
            this.choosedDepartmentArray.push(department);
            this.setting = {
                // 是否显示全选
                isShowChooseAll:true,
                //已选人
                lastChoosedPersonArr:[],
                //是否显示底部已选人物的栏目
                isShowBottomBar:true,
                //是否显示搜索
                isShowSearch:false,
                //是否多选
                isMutiableSelect:true,
                //
                fromPage:'self'
            };

            this.initData();
          },
          //下级文字的颜色
          goNextTipColor(department){
            let num = department.moreMsg.substr(1,1);
            num = parseInt(num);
            let color = num > 0 && !department.isSelected ? '#4685ff':'#eeeeee';
            return {
              color:color
            }
          },
          //顶部部门数据文字的颜色
          departmentTxtColor(isLast){
            let color = isLast ? 'rgb(68,68,68)':'#4685ff';
            return {
              color : color
            }
          },
          choosePerson(person){
            //单选
            if(!this.setting.isMutiableSelect){
              this.hasChoosedPersonArr.push(department);
              this.makeSureCLick();
              return;
            }
            //多选
            person.isSelected = !person.isSelected;
            //选中
            if(person.isSelected){
              this.hasChoosedPersonArr.push(person);
              return;
            }
            //取消选中
            for(let i = 0;i < this.hasChoosedPersonArr.length;i++){
              let choosedItem = this.hasChoosedPersonArr[i];
              if(choosedItem.id == person.id){
                this.hasChoosedPersonArr.splice(i,1);
              }
            }
          },
          //全选操作
          chooseAll(){
            this.isChoosedAll = !this.isChoosedAll;
            for(let i = 0;i< this.allPersonArray.length;i++) {
              this.allPersonArray[i].isSelected = this.isChoosedAll;
            }
            for(let i = 0;i< this.secondLevelDepartment.length;i++) {
              this.secondLevelDepartment[i].isSelected = this.isChoosedAll;
            }
            //全选
            if(this.isChoosedAll){
              this.hasChoosedPersonArr = this.allPersonArray.concat(this.secondLevelDepartment);
              return;
            }
            this.hasChoosedPersonArr = [];
          },
          customBack(){
            //选择人员界面 内部回退
            if(this.choosedDepartmentArray.length > 1){
              this.choosedDepartmentArray.pop();
              this.initData();
              return;
            }
            this.$emit('on-clickGoBack',false);
          },
          async getSendTarget(){
            let res = await getSendTarget();
            if(res.c == 0){
              let tmpArr = res.d;
              for(let i =0;i < tmpArr.length;i++){
                let item = tmpArr[i];
                item.isSelected = false;
                item.moreMsg = '';
              }
              this.allData = tmpArr;
              this.initData();
            }else{
              this.$vux.toast.show({
                type: 'text',
                text: res.m
              })
            }
          },
          initData(){
            this.secondLevelDepartment = [];
            this.allPersonArray = [];
            //赋值当前部门数据
            if(this.choosedDepartmentArray.length > 0){
              this.currentDepartment = this.choosedDepartmentArray[this.choosedDepartmentArray.length - 1];
            }else{
              for(let i = 0;i< this.allData.length;i++){
                let item = this.allData[i];
                //最初的上级部门数据
                if(item.pId == 0) {
                  this.currentDepartment = item;
                  this.choosedDepartmentArray.push(item);
                  this.head.title = item.name;
                  this.head.icon = 'return';
                  this.head.more = false;
                }
              }
            }
            //设置子部门数据
            for(let j = 0;j< this.allData.length;j++){
              let item = this.allData[j];
              //object_type=2表示人 object_type=1 表示部门
              if(item.object_type == 2) continue;
              if(item.pId == this.currentDepartment.id){
               this.secondLevelDepartment.push(item);
              }
            }
            //设置子部门人数数据
            for(let p=0;p < this.secondLevelDepartment.length;p++){
              let secondeDecpartItem = this.secondLevelDepartment[p];
              let num = 0;
              for(let q = 0;q < this.allData.length;q++){
                let item = this.allData[q];
                if(item.object_type == 1) continue;
                if(item.pId == secondeDecpartItem.id){
                  num++;
                }
              }
              secondeDecpartItem.moreMsg = '('+ num +')';
            }

            //设置人物数据
            for(let k = 0;k< this.allData.length;k++) {
              let item = this.allData[k];
              if(item.object_type == 1) continue;
              if(item.pId == this.currentDepartment.id){
                item.isSelected = false;
                this.allPersonArray.push(item);
              }
            }
            for(let f=0;f<this.allPersonArray.length;f++){
             let person = this.allPersonArray[f];
             for(let p=0;p<this.hasChoosedPersonArr.length;p++){
               let hasChooseItem = this.hasChoosedPersonArr[p];
               if(person.id == hasChooseItem.id){
                 person.isSelected = true;
               }else if(p == this.hasChoosedPersonArr.length - 1 && person.id != hasChooseItem.id){
                 person.isSelected = false;
               }
             }
            }
          },
        },
        created(){
          this.getSendTarget();
        },
        computed: {
          getBottomStyle(){
            let departCount = 0;
            let personCount = 0;

            for(let i = 0;i<this.hasChoosedPersonArr.length;i++){
              let obj = this.hasChoosedPersonArr[i];
              if (obj.object_type == 1){
                departCount++;
              }
              if(obj.object_type == 2){
                personCount++;
              }
            }
            return {
              width:departCount * 5 + personCount * 2.5 + 'rem',
              position:'relative',
              height:'1.5rem',
              marginTop:'0.35rem'
            }
          },
          getTopTitleDistanceToTop(){
            if(!this.setting) return {};
            let topDis = this.setting.isShowSearch ? '2.1rem' : '0';
            return {
                display:'inline-block',
                marginTop:topDis,
                marginLeft:'0.75rem',
                fontSize: '0.8rem',
                position:'relative'
            }
          },
          isChoosedPerson(){
            return this.hasChoosedPersonArr.length > 0? true :false;
          },
          personViewToBottom(){
            let margin = this.setting.isShowBottomBar ? '2.2rem' : '0';
            return  {
              marginBottom:margin
            }
          },
        },

    }
</script>

<style scoped>

  .contentBox {position:fixed;top:50px; bottom:50px;overflow:scroll;}

  .topSearch{position: fixed;top:2.1rem;left: 0;width: 100%;background-color: white;z-index: 99}
  .department{}
  .department .departmentView .departmentItem {background-color: white;height: 2.25rem;position: relative;}
  .selectView img{width: 1rem;height: 1rem;position:absolute;left:0.75rem;top:0.625rem;}
  .selectView{display: inline-block;float:left;width: 2.5rem;height: 2.25rem;}

   .nameLabel{float:left;display:inline-block;font-size: 0.7rem;height: 2.25rem;line-height: 2.25rem}
   .moreMsgLabel{font-size: 0.6rem;color: rgb(170,170,170);float: left;line-height: 2.25rem;height: 2.25rem;margin-left: 0.2rem;}
  .subDepartmentTip {color: #4685ff;font-size: 0.7rem;display: inline-block;position: absolute;right: 0.75rem;line-height: 2.25rem}
  .allChooseView span{line-height: 0.8rem;font-size: 0.8rem;margin: 0.75rem;float: left}
  .allChooseView img{width: 1rem;height: 1rem;float: left;margin-top: 0.5rem;margin-left: 0.75rem}
  .allChooseView {margin-bottom: 2rem}

  .clb:after{content:'';display: block;clear: both;}
  .whiteBg {background-color: white}

  .headView{width: 50px;height: 50px;border-radius: 25px;}

  .person {position: relative;margin-top: 2rem;}
  .person .perosonItem {height: 2.4rem;position: relative;}
  .person .perosonItem .headView{width: 2rem;height: 2rem;float: left;margin-left: 0.2rem;margin-top: 0.1rem;}

  .choosePerBottomView {position: fixed;bottom: 0;left: 0;width: 100%;height: 2.2rem;background-color: white;}
  .choosePerBottomView .bottomScrollView {width: 80%;height: 2.2rem}
  .bottomChoosedPerItem img{width: 1.5rem;height: 1.5rem;position: relative;right:0.5rem;border-radius: 0.75rem;}
  .bottomChoosedPerItem {float:left;background-color: white;position: relative;display: inline-block;margin-left: 0.8rem;height: 2.2rem;}
  .bottomChoosedPerItem .headViewDelete {position:absolute;top: 0;right: 0;width: 0.7rem;height: 0.7rem;}
  .choosePerBottomView .departmentChoosedItem {float: left; position: relative;margin-left: 0.9rem;height: 2.2rem;}
  .choosePerBottomView .departmentChoosedItem span{display: inline-block;color: #4685ff;position: relative;font-size: 0.8rem;border: 1px solid #4685ff;border-radius: 0.5rem;right: 0.5rem; }
  .choosePerBottomView .departmentChoosedItem .headViewDelete{position:absolute;top: 0;right: 0;width: 0.7rem;height: 0.7rem;}
  .makeSureButton {background-color: #4685ff;color: white;border-radius: 0.3rem;width: 3rem;display: inline-block;position: relative;left: 80%;top:-1.8rem;font-size: 0.8rem;text-align: center;padding:0.1rem 0;}

</style>
