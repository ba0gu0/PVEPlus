<template>
  <el-container>
    <el-header height="150px">
      <el-icon size="100" style="margin: 20px">
        <el-image :src="pveLogo"/>
      </el-icon>
    </el-header>
    <el-main>
      <el-form :model="loginData" :rules="rules" label-position="top" label-width="80px" size="large">
        <el-row>
          <el-col :span="6" :offset="9">
            <el-form-item label="用户名" prop="username">
              <el-input v-model="loginData.username" size="large" type="text" clearable></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="6" :offset="9">
            <el-form-item label="密码" prop="password">
              <el-input v-model="loginData.password" size="large" type="password" :show-password="true" clearable></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="6" :offset="9">
            <el-form-item label="认证类型">
              <el-select v-model="loginData.authtype" size="large" style="width: 100%">
                <el-option label="Proxmox VE authentication server" value="pve"/>
                <el-option label="Linux PAM standard authentication" value="pam"/>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="2" :offset="11" style="margin-top: 20px">
            <el-button type="primary" @click="submitLogin" style="width: 100%; height: 50px">登陆</el-button>
          </el-col>
        </el-row>
      </el-form>
    </el-main>
  </el-container>
</template>

<script setup>
import { ref } from 'vue'
import {doLogin} from "@/libs/user";
import {loadingFun} from "@/libs/loading";
import {msgBox} from "@/libs/msgBox";

import pveLogo from '@/assets/PVE Plus.png'
import {router} from "@/router";

const loginData = ref({
  username: '',
  password: '',
  authtype: 'pve'
})

const rules = ref ({
  username: [{
    required: true,
    message: '用户名不可为空',
  }],
  password: [{
    required: true,
    message: '密码不可为空',
  }],
})

const submitLogin = ()=>{
  const loading = loadingFun('正在登陆...')
  if (!loginData.value.username || !loginData.value.password) {
    msgBox('账户密码不能为空', 'error', 'alert')
    return
  }
  doLogin(loginData.value.username, loginData.value.password, loginData.value.authtype)
    .then((res)=>{
      loading.close()
      if (res === true) {
        msgBox('登陆成功', 'success', 'alert', ()=>{router.push('/')})
        localStorage.setItem('username', loginData.value.username)
      }else {
        msgBox(res.msg, 'error', 'alert')
      }
    })
}

</script>

<style scoped>

</style>