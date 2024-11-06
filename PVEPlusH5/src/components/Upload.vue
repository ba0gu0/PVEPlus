<template>
  <el-form :model="uploadData" label-position="top" label-width="150px" size="large">
    <el-row style="margin-top: 20px">
      <el-col :span="8" :offset="8">
        <el-form-item label="上传磁盘类型">
          <el-select v-model="uploadData.diskType" size="large" style="width: 100%">
            <el-option label="原始镜像格式 (RAW)" value="raw"/>
            <el-option label="QEMU镜像格式 (QCOW2)" value="qcow2"/>
            <el-option label="VMware镜像格式 (VMDK)" value="vmdk"/>
            <el-option label="VirtualBox镜像格式 (VDI)" value="vdi"/>
          </el-select>
        </el-form-item>
      </el-col>
    </el-row>
    <el-row style="margin-top: 20px">
      <el-col :span="10" :offset="8">
        <el-form-item label="上传磁盘名字">
          <el-input v-model="uploadData.diskName" size="large"/>
        </el-form-item>
      </el-col>
    </el-row>
  </el-form>
  <uploader
      :options="options"
      class="uploader-example"
      :autoStart="false"
      ref="uploaderRef"
      :file-status-text="statusText"
      :onFilesAdded="onFileAdd"
      @file-complete="uploadComplete"
  >
    <uploader-unsupport></uploader-unsupport>
    <uploader-drop :single="true" :attrs="attrs">
      <uploader-btn :single="true" :attrs="attrs">
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
        <div class="el-upload__text">
          拖拽文件到此或<em>点击进行上传</em>
        </div>
      </uploader-btn>
    </uploader-drop>
    <uploader-list></uploader-list>
    <el-button type="success" style="width: 100px; height: 45px; margin: 20px auto 0 45%" @click="startUpload">上传</el-button>
  </uploader>

</template>

<script setup>

import { UploadFilled } from '@element-plus/icons-vue'
import {ref} from "vue";
import {msgBox} from "@/libs/msgBox";
import {mergeDisk} from "@/libs/user";
import {router} from "@/router";
import {loadingFun} from "@/libs/loading";
import {isDark} from "@/libs/dark";

const statusText = {
  success: '上传完成',
  error: '上传出错',
  uploading: '上传中',
  paused: '暂停中',
  waiting: '等待中'
}

const options = {
  target: '/api/user/disks/upload',
  testMethod: 'POST',
  testChunks: false,
  singleFile: true,
  forceChunkSize: true,
  maxChunkRetries: 3,
  chunkRetryInterval: 1000,
  simultaneousUploads: 5,
  chunkSize: 10*1024*1024
}

const attrs = {
  accept: ['.vmdk', '.qcow2', '.raw', '.vdi'],
}

const uploaderRef = ref()

const startUpload = ()=>{
  uploaderRef.value.uploader.upload()
  uploaderRef.value.$el.childNodes[3].childNodes[1].childNodes[1].childNodes[0].childNodes[1].style.backgroundColor = isDark.value ? 'rgba(255, 255, 255, 0.3)' : 'rgba(0, 0, 0, 0.3)'
}

const uploadData = ref({
  diskType: 'qcow2',  // raw, qcow2, vmdk, vdi
  diskName: ''
})

const onFileAdd = (file) => {
  uploadData.value.diskName = file[0].name
}

const uploadComplete = ()=>{
  window.uploaderRef = uploaderRef.value

  const identifier = uploaderRef.value.files[0].uniqueIdentifier
  const diskType = uploadData.value.diskType
  const filename = uploadData.value.diskName
  const totalChunks = uploaderRef.value.files[0].chunks.length

  const loading = loadingFun('正在合并文件...')

  mergeDisk(filename, diskType, identifier, totalChunks)
    .then(res => {
      if (res.code === 200){
        msgBox(res.msg, 'success', 'alert', ()=>{
          router.push('/')
        })
      }else {
        msgBox(res.msg, 'error', 'confirm')
      }
      loading.close()
    })
}
</script>

<style scoped>
.uploader-example {
  width: 80%;
  padding: 20px;
  margin: 40px auto 0;
  box-shadow: 0 0 5px rgba(0, 0, 0, .4);
}
.uploader-example .uploader-drop {
  background-color: white;
  padding: 0;
}
.uploader-example .uploader-btn {
  width: 100%;
  border: 0;

}
.uploader-example .uploader-btn:hover {
  background-color: white;
}

@media (prefers-color-scheme: dark) {
  .uploader-example .uploader-drop {
    background-color: var(--el-bg-color);
    padding: 0;
  }
  .uploader-example .uploader-btn:hover {
    background-color: var(--el-bg-color);
  }
  .uploader-example .uploader-list .uploader-file .uploader-file-progress {
    background-color: rgba(255, 255, 255, 0.2);
    padding: 0;
  }
}

.el-icon--upload {
  margin-left: 44%;
  font-size: 100px;
  color: var(--el-text-color-placeholder);
  margin-bottom: 16px;
  line-height: 50px;
}
.el-upload__text {
    color: var(--el-text-color-regular);
    font-size: 14px;
    text-align: center;
}
.el-upload__text em {
    color: var(--el-color-primary);
    font-style: normal;
}
</style>