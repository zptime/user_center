<template>
  <div>
    <head-top :head="head"></head-top>
    <choose-target :title="title" @on-cancel="optCancel" @on-sure="optSure"></choose-target>
  </div>
</template>

<script type="es6">
  import ChooseTarget from '../ChooseTarget.vue'
  import HeadTop from '@/components/Head.vue'
  export default {
    data () {
      return {
        head:{
          icon: 'return',
          title: '选择通知对象',
          more: false
        },
        title:'通知',
        dataList:[],//返回数据列表
      }
    },
    components: {
      ChooseTarget,
      HeadTop,
    },
    methods:{
      //取消回调事件
      optCancel(){
        alert('取消回调事件');
      },

      //确定回调事件
      optSure(data){
        alert('确定回调事件');
        this.dataList = data;
      },
    },
  }
</script>

<style scoped>

</style>
