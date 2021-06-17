import axios from 'axios';
import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

Vue.config.productionTip = false
axios.defaults.baseURL = 'http://0.0.0.0:8080/';
// axios.defaults.headers = {
//   'Access-Control-Allow-Origin' : '*',
//   'Access-Control-Allow-Methods':'GET,PUT,POST,DELETE,PATCH,OPTIONS',
// };

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
