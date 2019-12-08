<template>
  <div id="search">
    <div class="search">
      <div class="inner clb" :style="itemStyle('all','4px','0 0 16px 4px rgba(0, 0, 0, 0.08)')">
        <input v-model="search.search_txt" type="text"
               @blur="on_blur" @focus="on_focus"  @input="on_inp"
               :placeholder="search.is_focus ? '' : search.placeholder_txt"
               class="inp"  :class="{ inp_w : !search.is_focus }"
        >
      </div>
      <div v-if="search.is_focus" class="inner-btn" @click="on_search" :style="itemStyle('all','1.12rem','0 0 10px 1px rgba(70, 133, 255, 0.4)')">
        搜索
      </div>
    </div>
  </div>
</template>

<script type="es6">
    export default {
    props: ["search"],
    data () {
      return {
        is_focus:false,
        search_txt:'',
        placeholder_txt:'配置的文字'
      }
    },

    methods: {
      on_focus() {
        this.search.is_focus = true ;
        this.$emit('onfocus');
      },
      on_blur(){
        if(this.search.search_txt==''){
          this.search.is_focus =false ;
        }
        this.$emit('onblur');
      },
      on_inp() {
        if(this.search.search_txt==''){
          this.search.is_focus =false;
          this.$emit('onsearch');
        }else{
          this.search.is_focus =true;
        }
      },
      on_search(){
        this.$emit('onsearch');
      },
      itemStyle(type,$radius,$shadow){
        let styles={};
        if(type=='all'){
          styles = {
            '-webkit-border-radius': $radius,
            '-moz-border-radius' : $radius,
            '-ms-border-radius': $radius,
            '-o-border-radius': $radius,
            'border-radius': $radius,
            'box-shadow': $shadow,
            '-moz-box-shadow': $shadow,
            '-webkit-box-shadow': $shadow,
          }

        }else if(type=='radius'){
          styles = {
            '-webkit-border-radius': $radius,
            '-moz-border-radius' : $radius,
            '-ms-border-radius': $radius,
            '-o-border-radius': $radius,
            'border-radius': $radius,
          }
        }else if(type=='shadow'){
          styles = {
            'box-shadow': $shadow,
            '-moz-box-shadow': $shadow,
            '-webkit-box-shadow': $shadow,
          }
        }
        return styles;
      }
    }
  }
</script>

<style scoped>
.clb:after{content: "";clear: both;display: block;}
.search{width:100%;height: 2.25rem;padding: 0 0.75rem;background-color: #fff;}
.inner{height:100%;padding:0.32rem 0;float: left;}
.inp{height: 1.6rem;line-height:1.6rem;padding:0 0.4rem 0 1.5rem;text-align: left;float: left;display: block;width: 14rem;background-image: url("./fdj.png");background-size: 1rem 1rem;background-repeat: no-repeat;background-position: 3% center;font-size: 0.75rem;}
.search .inp_w{width:17rem;padding-left:2.8rem;background-position: 1rem center;}
.inner-btn{float: right;background: #4685ff;color: #FFFFFF;  font-size: 0.6rem;  width: 2.25rem;  height: 2.25rem;  line-height: 2.25rem;  text-align: center;  }
:-moz-placeholder { /* Mozilla Firefox 4 to 18 */  font-size:0.7rem;  color: #aaa;  }
::-moz-placeholder { /* Mozilla Firefox 19+ */  font-size:0.7rem;  color: #aaa;  }
:-ms-input-placeholder { /* Internet Explorer 10+ */  font-size:0.7rem;  color: #aaa;  }
::-webkit-input-placeholder { /* WebKit browsers */  font-size:0.7rem;  color: #aaa;  }
:-moz-placeholder { /* Mozilla Firefox 4 to 18 */  font-size:0.7rem;  color: #aaa;  }
::-moz-placeholder { /* Mozilla Firefox 19+ */  font-size:0.7rem;  color: #aaa;  }
:-ms-input-placeholder { /* Internet Explorer 10+ */  font-size:0.7rem;  color: #aaa;  }
</style>

