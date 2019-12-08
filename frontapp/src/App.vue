<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style lang="scss">
    @import './style/common.scss';
    @font-face {
      font-family: 'PingFang-Regular';   /*????*/
      src: url('./style/font/PingFang-Regular.ttf');       /*?????*/
    }
    *{
      margin: 0;
      padding: 0;
    }

    .contentBox{
      position: absolute;
      top: 2.1rem;
      width: 100%;
      background-color: #fff;
    }

    ::-webkit-input-placeholder{color:rgba(0,0,0,0.3);font-family: "microsoft yahei"}
    :-moz-placeholder{color:rgba(0,0,0,0.3);font-family: "microsoft yahei"}
    ::-moz-placeholder{color:rgba(0,0,0,0.3);font-family: "microsoft yahei"}
    :-ms-input-placeholder{color:rgba(0,0,0,0.3);font-family: "microsoft yahei"}

    button{
      height: 1.5rem;
      border: 1px solid #4685ff;
      border-radius: 4px;
      background: #fff;
      color: #4685ff;
      font-size: 0.7rem;
      width: 4.6rem;
    }
</style>
