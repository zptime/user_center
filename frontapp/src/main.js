// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import VueRouter from 'vue-router'
import routes from './router/router.js'
import store from './store/'
import {routerMode} from './config/env'
import './config/rem'
import FastClick from 'fastclick'
import App from './App'
import { ToastPlugin } from 'vux'
import { LoadingPlugin } from 'vux'
import vueTap from 'v-tap';

Vue.config.productionTip = false

if ('addEventListener' in document) {
    document.addEventListener('DOMContentLoaded', function() {
        FastClick.attach(document.body);
    }, false);
}

Vue.use(VueRouter)
Vue.use(ToastPlugin)
Vue.use(LoadingPlugin)
Vue.use(vueTap);


const router = new VueRouter({
	routes,
	mode: routerMode,
	strict: process.env.NODE_ENV !== 'production',
})

new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})
