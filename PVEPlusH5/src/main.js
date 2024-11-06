import { createApp } from 'vue'
import App from './App.vue'
import { router } from './router'

import 'element-plus/theme-chalk/dark/css-vars.css'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

import uploader from 'vue-simple-uploader'
import 'vue-simple-uploader/dist/style.css'

const app = createApp(App)

app.use(router).use(ElementPlus).use(uploader)

app.mount('#app')
