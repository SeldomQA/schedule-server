import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      redirect: 'tasks'
    },
    {
      path: '/tasks',
      name: 'tasks',
      component: () => import('@/views/tasks/Tasks.vue'),
      meta: {
        title: 'Tasks'
      }
    },
    { 
      path: '/:pathMatch(.*)*', 
      name: 'NotFound', 
      redirect: 'tasks' 
    }
  ]
})

export default router
