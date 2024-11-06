import { createRouter, createWebHistory } from 'vue-router'

import Login from '@/components/Login.vue'
import Export from "@/components/Export.vue";
import Import from "@/components/Import.vue";
import Home from '@/components/Home.vue';
import Refresh from '@/components/Refresh.vue'
import Index from '@/components/Index.vue'
import Upload from "@/components/Upload.vue";
import Mount from "@/components/Mount.vue"


export const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: Index,
      children: [
        {
          path: '/',
          component: Home
        },
        {
          path: '/home',
          component: Home
        },
        {
          path: '/upload',
          component: Upload
        },
        {
          path: '/import',
          component: Import
        },
        {
          path: '/import/:vmId/:diskId',
          component: Import,
          props: true
        },
        {
          path: '/export',
          component: Export,
        },
        {
          path: '/export/:vmId',
          component: Export,
          props: true
        },
        {
          path: '/mount',
          component: Mount,
        },
        {
          path: '/mount/:vmId',
          component: Mount,
          props: true
        },
      ]
    },
    {
      path: '/login',
      component: Login
    },
    {
      path: '/refresh',
      component: Refresh
    },
  ]
})