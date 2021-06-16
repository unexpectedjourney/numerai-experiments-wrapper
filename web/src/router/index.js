import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('../views/About.vue')
  },
  {
    path: '/models',
    name: 'Models',
    component: () => import('../views/Models.vue')
  },
  {
    path: '/model/:id/',
    name: 'Model',
    component: () => import('../views/Model.vue'),
    props: true,
  }
]

const router = new VueRouter({
  routes
})

export default router
