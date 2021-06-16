import axios from 'axios';
import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

Vue.config.productionTip = false
axios.defaults.baseURL = 'http://localhost:8080';

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
