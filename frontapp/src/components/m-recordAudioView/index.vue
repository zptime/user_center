<template>
       <div class="audioView">
         <div class="timeView" ref="timeLabel">01:00</div>
         <div class="lineView"></div>
         <div class="buttonsView">
           <div class="textView">
             <span class="cancleBtnView"></span>
             <span class="cancleBtnView" @click="cancleRecord" v-show="showHandleButton">取消</span>
             <span class="cancleBtnView"></span>
           </div>

           <div class="audioBtnView">
             <img src="./images/icon-stopRecord.png" @click="recordAudio" v-show="isRecording"/>
             <img src="./images/icon-startRecord.png" @click="recordAudio" v-show="!isRecording"/>
           </div>
           <div class="textView">
             <span class="makeSureBtnView"></span>
             <span class="makeSureBtnView" @click="uploadRecord" v-show="showHandleButton">确定</span>
             <span class="makeSureBtnView"></span>
           </div>
         </div>
       </div>
</template>

<script>
    export default {
        name: "index",
        data(){
          return {
            timer:undefined,//倒计时对象
            recordState:0,
            isRecording:false,//是否正在录音
            showHandleButton:false,//是否显示确定 取消按钮
          }
        },
        methods:{
          recordAudio(){
            while(this.recordState-3 >=0){
              this.recordState -= 3;
            }
            switch (this.recordState){
              //初始状态 点击开始录音
              case 0:
                this.isRecording = true;
                this.showHandleButton = false;
                this.timer= undefined;
                this.setTimeLabel('01:00');
                this.countdowm();
                this.$emit('on-startRecord');
                break;
              //录音状态 点击停止录音
              case 1:
                this.isRecording = false;
                this.showHandleButton = true;
                this.stopCountDown();
                this.$emit('on-stopRecord');
                break;
              //回复初始状态
              case 2:
                this.isRecording = false;
                this.showHandleButton = false;
                this.setTimeLabel('01:00');
                break;
              default:
            }
            this.recordState += 1;
          },
          //录音时间到所执行的方法 由父组件调用
          //点击popup遮罩隐藏
          stopRecordBySuper(){
            this.recordState = 0;
            this.isRecording = false;
            this.showHandleButton = false;
            this.setTimeLabel('01:00');
          },
          //确定按钮点击
          uploadRecord(){
            //录音时间
            let timeStr = this.$refs.timeLabel.innerHTML;
            let arr = timeStr.split(':');
            let time = 60 - parseInt(arr[1]);
            this.$emit('on-makeSure',time);

            // modify by perry
            this.stopRecordBySuper();
          },
          //取消点击
          cancleRecord(){
            this.$emit('on-cancleClick');
            this.recordState= 0;
            this.isRecording = false;
            this.showHandleButton = false;
            this.setTimeLabel('01:00');
            this.stopCountDown();
          },
          //开始时间倒计时
          countdowm(){
            var _self = this;
            let time = 60;
            //每秒执行一次
            this.timer = setInterval(function(){
              time --;
              if (time >= 0){
                _self.setTimeLabel(time);
              }else{
                clearInterval(_self.timer);
                _self.recordAudio();
              }
            },1000);
          },
          //停止倒计时
          stopCountDown(){
            if (this.timer){
              clearInterval(this.timer);
            }
          },
          //可赋值数字和字符串
          setTimeLabel(time){
            if(typeof time == 'number'){
               let timeStr = '00:'+time;
               if(timeStr.length <5){
                 timeStr = '00:0'+time;
               }
               this.$refs.timeLabel.innerHTML = timeStr;
            }else{
              this.$refs.timeLabel.innerHTML = time;
            }
          },
        }
    }
</script>

<style scoped>

  .audioView{width: 100%;background-color: #eeeeee;height: 12.5rem;}
  .timeView{padding-top:0.75rem;left: 0;right:0;height: 2rem;color: #666666;text-align: center;}
  .lineView{margin-top: 0.25rem;height: 1px;background-color: red;}
  .buttonsView {display: flex;flex-flow: row;height: 10rem;}
  .buttonsView .makeSureBtnView{flex:1;text-align: left;display: inline-block;
    padding-top: 0.8rem;}
  .buttonsView .cancleBtnView{flex:1;display: inline-block;text-align: right;
    padding-top: 0.8rem;}
  .buttonsView .audioBtnView{width: 210px;height: 210px}
  .buttonsView .audioBtnView img{width:60% ;height: 60%;margin-top: 20%;margin-left: 20%;}

  .textView {display: flex;flex-flow: column;flex: 1}

</style>
