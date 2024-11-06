<template>
  <el-form :model="mountData" label-position="top" label-width="150px" size="large">
    <el-row style="margin-top: 20px">
      <el-col :span="4" :offset="8">
        <el-form-item label="挂载磁盘总线/设备">
          <el-select v-model="mountData.mountDiskKey" size="large" style="width: 100%">
            <el-option label="IDE" value="ide"/>
            <el-option label="SATA" value="sata"/>
            <el-option label="VirtIO Block" value="virtio"/>
            <el-option label="SCSI" value="scsi"/>
          </el-select>
        </el-form-item>
      </el-col>
    </el-row>
    <el-row style="margin-top: 20px">
      <el-col :span="4" :offset="8">
        <el-form-item label="是否将磁盘设置为第一引导启动项">
          <el-switch v-model="mountData.fistBoot"/>
        </el-form-item>
      </el-col>
    </el-row>
    <el-row style="margin-top: 20px">
      <el-col :span="8" :offset="8">
        <el-form-item label="选择虚拟机">
          <el-select v-model="mountData.vmId" size="large" style="width: 100%" @change="selectVm">
            <el-option v-for="vm of vms" :label="vm.name" :value="vm.vmid.toString()"/>
          </el-select>
        </el-form-item>
      </el-col>
    </el-row>
    <el-row style="margin-top: 20px">
      <el-col :span="8" :offset="8">
        <el-form-item label="选择需要挂载磁盘">
          <el-select v-model="mountData.mountDiskId" size="large" style="width: 100%">
            <el-option v-for="vmDisk of unuseVmDisks" :label="vmDisk.value" :value="vmDisk.key"/>
          </el-select>
        </el-form-item>
      </el-col>
    </el-row>
    <el-row style="margin-top: 20px">
      <el-col :span="2" :offset="10">
        <el-button style="width: 100%; height: 45px" size="large" type="success" @click="doMountVmDisk">挂载</el-button>
      </el-col>
    </el-row>
  </el-form>
</template>


<script setup>
import {ref} from "vue";
import {getVmDisk, getVms, getVmUnusedDisk, mountVmDisk} from "@/libs/pve";
import {msgBox} from "@/libs/msgBox";
import {router} from "@/router";
import {loadingFun} from "@/libs/loading";


const existsDisks = ref()
const vms = ref()
const unuseVmDisks = ref()

const props = defineProps({
  vmId: String
})

const mountData = ref({
  mountDiskKey: 'virtio', //
  vmId: '',
  mountDiskId: '',
  fistBoot: true
})

if (props.vmId) {
  mountData.value.vmId = props.vmId
  getVmUnusedDisk(mountData.value.vmId)
    .then(res => {
      unuseVmDisks.value = res
    })
  getVmDisk(mountData.value.vmId)
    .then(res => {
      existsDisks.value = res
    })
}

getVms()
  .then(res => {
    vms.value = res
  })


const selectVm = ()=>{
  getVmUnusedDisk(mountData.value.vmId)
    .then(res => {
      unuseVmDisks.value = res
      mountData.value.mountDiskId = ''
    })
  getVmDisk(mountData.value.vmId)
    .then(res => {
      existsDisks.value = res
    })
}

const makeDiskNum = (key)=>{
  const diskNums = existsDisks.value
    .filter(disk => {
      return disk.key.indexOf(key) === 0
    })
    .map(disk => {
      const index = disk.key.indexOf(key)
      if (index === 0) {
        return parseInt(disk.key.slice(index+key.length))
      }
    })

  let diskNum = 0
  while (true){
    if (!diskNums.includes(diskNum)){
      break
    }
    diskNum += 1
  }
  return diskNum.toString()
}
const doMountVmDisk = ()=>{

  if (!mountData.value.vmId || !mountData.value.mountDiskId) {
    msgBox('请选择虚拟机、选择磁盘.', 'error', 'alert')
    return
  }

  mountData.value.mountDiskKey = mountData.value.mountDiskKey + makeDiskNum(mountData.value.mountDiskKey)

  const loading = loadingFun('正在挂载磁盘...')
  mountVmDisk(mountData.value)
    .then((res)=>{
      if (res === true){
        msgBox('磁盘挂载成功!', 'success', 'alert', ()=>{
          router.push('/refresh')
        })
      }else {
        msgBox(res.msg, 'error', 'alert')
      }
      loading.close()
    })
}

</script>

<style scoped>

</style>