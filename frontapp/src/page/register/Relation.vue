<template>
  <div :class="{'noHeadContent':!regShowHead}">
    <headTop :head="head" v-if="regShowHead">
      <img slot="left" src="../../images/icon-return.png" @click="goBack"/>
    </headTop>
    <div class="contentBox" v-cloak>
      <div class="list">
        <ul class="li-box">
          <li class="item" :data-id="item.id"  v-for="item in list" @click="choose(item.username)">
            <span class="username">{{ item.username }}</span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
  import HeadTop from '../../components/Head.vue'
  import Global from '@/components/Global.vue'
  export default {
    props:['childInd'],
    data() {
      return {
        head:{
          icon: 'return',
          title: '家长与孩子的关系',
          more: false
        },
        regShowHead:Global.regShowHead,
        list:[
          {"id":1,"username":'父亲'},
          {"id":2,"username":'母亲'},
          {"id":3,"username":'爷爷'},
          {"id":4,"username":'奶奶'},
          {"id":5,"username":'外公'},
          {"id":6,"username":'外婆'}
        ],
        chooseVal:''
      }
    },
    components: {
      HeadTop,
    },
    methods: {
      goBack() {
        this.chooseVal = '';
        this.$emit('on-close');
      },

      choose(value){
        this.chooseVal = value;
        this.$emit('on-choose',this.childInd,this.chooseVal);
      }
    }
  }
</script>

<style scoped>
  .list{
    /*margin-top: 0.8rem;*/
    background: #fff;
  }
  .list .item{
    height: 3rem;
    border-bottom: 1px solid #f5f5f5;
    padding:0.5rem 1rem;
    background-color: #fff;
  }
  .list .item span{
    display: inline-block;
    height: 2rem;
    line-height: 2rem;
    margin-bottom: 1rem;
    float: left;
  }
  .list .item .username{
    font-size: 0.8rem;
    margin-left:0.6rem;
    color:#444;
  }
  .list .item:last-child{
    border-bottom:none;
  }
</style>
