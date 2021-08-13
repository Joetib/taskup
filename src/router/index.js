import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import SignUp from '../views/Signup.vue'
import Dashboard from '../views/Dashboard.vue'
import ProjectDetail from '../views/ProjectDetail.vue';
import TaskDetail from '../views/TaskDetail.vue';
import Invites from '../views/Invites.vue';
import TaskList from '../views/TaskList.vue';

const routes = [
  {
    path:'/project/:project_id/task/:task_id',
    name:'TaskDetail',
    component: TaskDetail,
    meta: {
      requiresAuth: true,
    }
  },
  {
    path:'/tasks/',
    name:'TaskList',
    component: TaskList,
    meta: {
      requiresAuth: true,
    }
  },
  {
    path:'/invites/',
    name:'Invites',
    component: Invites,
    meta: {
      requiresAuth: true,
    }
  },
  {
    path: '/project/:project_id',
    name: 'ProjectDetail',
    component: ProjectDetail,
    meta: {
      requiresAuth: true
    },
  },
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: {
      guest: true,
    }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: {
      guest: true,
    }
  },
  {
    path: '/signup',
    name: 'SignUp',
    component: SignUp,
    meta: {
      guest: true,
    }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: {
      requiresAuth: true,
    }
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue'),
    meta: {
      guest: true,
    }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (localStorage.getItem('token') == null) {
      next({
        path: '/login',
        params: { nextUrl: to.fullPath }
      })
    } else {
      next()
    }

  } 
  else {
    next()
  }
})

export default router
