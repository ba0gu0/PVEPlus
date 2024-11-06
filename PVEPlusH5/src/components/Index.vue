<template>
  <el-container>
    <el-header height="100px" style="display: flex">
      <el-icon size="80" style="margin: 20px">
        <el-image :src="pveLogo"/>
      </el-icon>
      <el-menu
        mode="horizontal"
        @select="handleSelect"
        :ellipsis="false"
        style="width: 100%"
        default-active="home"
        >
        <el-row
          justify="center"
          style="width: 100%"
          :gutter="10"
        >
          <el-col :span="3">
            <el-menu-item index="home" style="height: 100%;justify-content: center;">首页</el-menu-item>
          </el-col>
           <el-col :span="3">
            <el-menu-item index="upload" style="height: 100%;justify-content: center;">上传</el-menu-item>
          </el-col>
          <el-col :span="3">
            <el-menu-item index="import" style="height: 100%;justify-content: center;">导入</el-menu-item>
          </el-col>
          <el-col :span="3">
            <el-menu-item index="mount" style="height: 100%;justify-content: center;">挂载</el-menu-item>
          </el-col>
          <el-col :span="3">
            <el-menu-item index="export" style="height: 100%;justify-content: center;">导出</el-menu-item>
          </el-col>
        </el-row>
      </el-menu>
      <el-button style="display: grid; margin-left: 30px; height: 100%; border-width: 0" @click="submitLogout" round>
        <el-avatar shape="square">
          {{ username }}
        </el-avatar>
        <span style="color: deepskyblue; font-size: small; text-align: center; margin-left: 10px">注销</span>
      </el-button>
    </el-header>
    <el-main>
      <router-view/>
    </el-main>
  </el-container>
  <div class="taskProgress" @touchmove.prevent @mousewheel.prevent v-if="isTask">
    <span style="color: #409EFF; font-size: x-large; margin-left: 40px">任务进行中...</span>

    <section v-if="loadingCssNum === 1">
      <div class="loader loader-1">
        <div class="loader-outter"></div>
        <div class="loader-inner"></div>
      </div>
    </section>

    <section v-else-if="loadingCssNum === 2">
      <div class="loader loader-2">
        <svg class="loader-star" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
          version="1.1">
          <polygon
            points="29.8 0.3 22.8 21.8 0 21.8 18.5 35.2 11.5 56.7 29.8 43.4 48.2 56.7 41.2 35.1 59.6 21.8 36.8 21.8 "
            fill="#18ffff"></polygon>
        </svg>
        <div class="loader-circles"></div>
      </div>
    </section>

    <section v-else-if="loadingCssNum === 3">
      <div class="loader loader-21">
        <div class="css-times times1"></div>
        <div class="css-times times2"></div>
        <div class="css-times times3"></div>
      </div>
    </section>

    <section v-else-if="loadingCssNum === 4">
      <div class="loader loader-7">
        <div class="line line1"></div>
        <div class="line line2"></div>
        <div class="line line3"></div>
      </div>
    </section>

    <section v-else-if="loadingCssNum === 5">
      <div class="loader loader-18">
        <div class="css-star star1"></div>
        <div class="css-star star2"></div>
        <div class="css-star star3"></div>
        <div class="css-star star4"></div>
        <div class="css-star star5"></div>
        <div class="css-star star6"></div>
        <div class="css-star star7"></div>
        <div class="css-star star8"></div>
      </div>
    </section>

    <section v-else-if="loadingCssNum === 6">
      <div class="loader loader-5">
        <div class="loader-pacman"></div>
      </div>
    </section>

    <section v-else-if="loadingCssNum === 7">
      <div class="loader loader-4"></div>
    </section>

    <section v-else-if="loadingCssNum === 8">
      <div class="loader loader-17">
        <div class="css-square square1"></div>
        <div class="css-square square2"></div>
        <div class="css-square square3"></div>
        <div class="css-square square4"></div>
        <div class="css-square square5"></div>
        <div class="css-square square6"></div>
        <div class="css-square square7"></div>
        <div class="css-square square8"></div>
      </div>
    </section>

    <section v-else-if="loadingCssNum === 9">
      <div class="loader loader-12">
        <svg class="loader-star star1" version="1.1" xmlns="http://www.w3.org/2000/svg"
          xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="35px" height="35px"
          viewBox="0 0 23.172 23.346" xml:space="preserve">
          <polygon
            points="11.586,0 8.864,8.9 0,8.9 7.193,14.447 4.471,23.346 11.586,17.84 18.739,23.346 16.77,14.985 23.172,8.9 14.306,8.9">
          </polygon>
        </svg>
        <svg class="loader-star star2" version="1.1" xmlns="http://www.w3.org/2000/svg"
          xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="35px" height="35px"
          viewBox="0 0 23.172 23.346" xml:space="preserve">
          <polygon
            points="11.586,0 8.864,8.9 0,8.9 7.193,14.447 4.471,23.346 11.586,17.84 18.739,23.346 16.77,14.985 23.172,8.9 14.306,8.9">
          </polygon>
        </svg>
        <svg class="loader-star star3" version="1.1" xmlns="http://www.w3.org/2000/svg"
          xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="35px" height="35px"
          viewBox="0 0 23.172 23.346" xml:space="preserve">
          <polygon
            points="11.586,0 8.864,8.9 0,8.9 7.193,14.447 4.471,23.346 11.586,17.84 18.739,23.346 16.77,14.985 23.172,8.9 14.306,8.9">
          </polygon>
        </svg>
        <svg class="loader-star star4" version="1.1" xmlns="http://www.w3.org/2000/svg"
          xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="35px" height="35px"
          viewBox="0 0 23.172 23.346" xml:space="preserve">
          <polygon
            points="11.586,0 8.864,8.9 0,8.9 7.193,14.447 4.471,23.346 11.586,17.84 18.739,23.346 16.77,14.985 23.172,8.9 14.306,8.9">
          </polygon>
        </svg>
        <svg class="loader-star star5" version="1.1" xmlns="http://www.w3.org/2000/svg"
          xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="35px" height="35px"
          viewBox="0 0 23.172 23.346" xml:space="preserve">
          <polygon
            points="11.586,0 8.864,8.9 0,8.9 7.193,14.447 4.471,23.346 11.586,17.84 18.739,23.346 16.77,14.985 23.172,8.9 14.306,8.9">
          </polygon>
        </svg>
        <svg class="loader-star star6" version="1.1" xmlns="http://www.w3.org/2000/svg"
          xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="35px" height="35px"
          viewBox="0 0 23.172 23.346" xml:space="preserve">
          <polygon
            points="11.586,0 8.864,8.9 0,8.9 7.193,14.447 4.471,23.346 11.586,17.84 18.739,23.346 16.77,14.985 23.172,8.9 14.306,8.9">
          </polygon>
        </svg>
      </div>
    </section>

    <section v-else-if="loadingCssNum === 10">
      <div class="loader loader-6">
        <div class="loader-inner"></div>
      </div>
    </section>

    <section v-else-if="loadingCssNum === 11">
      <div class="loader loader-14">
        <svg class="loader-star star-small" version="1.1" xmlns="http://www.w3.org/2000/svg"
          xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="23.172px" height="23.346px"
          viewBox="0 0 23.172 23.346" xml:space="preserve">
          <polygon fill="#01579b"
            points="11.586,0 8.864,8.9 0,8.9 7.193,14.447 4.471,23.346 11.586,17.84 18.739,23.346 16.77,14.985 23.172,8.9 14.306,8.9  ">
          </polygon>
        </svg>
        <svg class="loader-star star-big" version="1.1" xmlns="http://www.w3.org/2000/svg"
          xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="23.172px" height="23.346px"
          viewBox="0 0 23.172 23.346" xml:space="preserve">
          <polygon fill="#40c4ff"
            points="11.586,0 8.864,8.9 0,8.9 7.193,14.447 4.471,23.346 11.586,17.84 18.739,23.346 16.77,14.985 23.172,8.9 14.306,8.9  ">
          </polygon>
        </svg>
      </div>
    </section>

    <section v-else-if="loadingCssNum === 12">
      <div class="loader loader-3">
        <div class="dot dot1"></div>
        <div class="dot dot2"></div>
        <div class="dot dot3"></div>
      </div>
    </section>

    <section v-else-if="loadingCssNum === 13">
      <div class="loader loader-9">
        <svg class="loader-star star1" version="1.1" xmlns="http://www.w3.org/2000/svg"
          xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="23.172px" height="23.346px"
          viewBox="0 0 23.172 23.346" xml:space="preserve">
          <polygon fill="#c6ff00"
            points="11.586,0 8.864,8.9 0,8.9 7.193,14.447 4.471,23.346 11.586,17.84 18.739,23.346 16.77,14.985 23.172,8.9 14.306,8.9">
          </polygon>
        </svg>
        <svg class="loader-star star2" version="1.1" xmlns="http://www.w3.org/2000/svg"
          xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="23.172px" height="23.346px"
          viewBox="0 0 23.172 23.346" xml:space="preserve">
          <polygon fill="#c6ff00"
            points="11.586,0 8.864,8.9 0,8.9 7.193,14.447 4.471,23.346 11.586,17.84 18.739,23.346 16.77,14.985 23.172,8.9 14.306,8.9  ">
          </polygon>
        </svg>
        <svg class="loader-star star3" version="1.1" xmlns="http://www.w3.org/2000/svg"
          xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="23.172px" height="23.346px"
          viewBox="0 0 23.172 23.346" xml:space="preserve">
          <polygon fill="#c6ff00"
            points="11.586,0 8.864,8.9 0,8.9 7.193,14.447 4.471,23.346 11.586,17.84 18.739,23.346 16.77,14.985 23.172,8.9 14.306,8.9  ">
          </polygon>
        </svg>
      </div>
    </section>

    <section v-else-if="loadingCssNum === 14">
      <div class="loader loader-20">
        <div class="css-diamond"></div>
      </div>
    </section>

    <section v-else-if="loadingCssNum === 15">
      <div class="loader loader-13">
        <div class="css-heart heart1"></div>
        <div class="css-heart heart2"></div>
        <div class="css-heart heart3"></div>
        <div class="css-heart heart4"></div>
      </div>
    </section>
    <div style="width: 280px;">
      <el-progress
        :percentage="taskProgress"
        :indeterminate="true"
        color="#67C23A"
      />
      <span style="color: #909399; font-size: small; margin-left: 70px">已用时: {{ taskTime }}</span>
    </div>
  </div>
</template>

<script setup>

import {checkLogin, doLogout} from "@/libs/user";
import {loadingFun} from "@/libs/loading";
import {getTask} from "@/libs/pve/getTask";
import {ref} from "vue";
import {msgBox} from "@/libs/msgBox";
import pveLogo from '@/assets/PVE Plus.png'
import {router} from "@/router";

const loading = loadingFun('加载中...');
const loadingCssNum = ref(1);
const isTask = ref(false);
const taskProgress = ref(0);
const taskTime = ref(0);

const pollingLogin = params => {
  checkLogin()
    .then(res => {
      if (!res){
        router.push('/login')
      }
      const pollingST = setTimeout(() => {
        clearTimeout(pollingST)
        pollingLogin(params)
      }, 60000)
    })
}

const pollingTask = params => {
  getTask()
    .then(res => {
      if (res){
        isTask.value = true
        taskProgress.value = res.progress
        taskTime.value = formatSecond(res.time)
        const pollingST = setTimeout(() => {
          clearTimeout(pollingST)
          pollingTask(params)
        }, 5000)
        loadingCssNum.value = Math.floor(Math.random() * (15 - 1 + 1)) + 1
      }else {
        msgBox('任务已完成', 'success', 'alert', ()=>{
          isTask.value = false
          router.push('/home')
        })
      }
    })
}


checkLogin()
  .then(res => {
    if (res){
      pollingLogin()
    }else {
      router.push('/login')
    }
    loading.close()
  })

getTask()
  .then(res => {
    if (res){
      isTask.value = true
      taskProgress.value = res.progress
      taskTime.value = formatSecond(res.time)
      pollingTask()
    }
  })

const formatSecond = (result) => {
  const h = Math.floor((result / 3600) % 24);
  const m = Math.floor((result / 60) % 60);
  const s = Math.floor(result % 60);
  result = s + "秒";
  if (m > 0) {
    result = m + "分钟" + result;
  }
  if (h > 0) {
    result = h + "小时" + result;
  }
  return result;
}


const username = ref(localStorage.getItem('username') ? localStorage.getItem('username').substring(0,4) : 'user')
const handleSelect = (index)=>{
  switch (index) {
    case 'home':
      router.push('/home')
      break
    case 'upload':
      router.push('/upload')
      break
    case 'import':
      router.push('/import')
      break
    case 'mount':
      router.push('/mount')
      break
    case 'export':
      router.push('/export')
      break
  }
}

const submitLogout = ()=>{
  const loading = loadingFun('正在登陆...')
  doLogout()
    .then((res)=>{
      loading.close()
      if (res === true) {
        msgBox('注销成功', 'success', 'alert', ()=>{router.push('/login')})
        localStorage.removeItem('username')
      }else {
        msgBox('注销失败', 'error', 'alert')
      }
    })
}

</script>

<style scoped>
@import "@/css/loading.css";
.taskProgress {
  display: grid;
  align-items: center;
  justify-content: center;
  align-content: center;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255,255,255,0.5);
  z-index: 1000;
}
@media (prefers-color-scheme: dark) {
  .taskProgress {
    background-color: rgba(0,0,0,0.5);
  }
}
</style>