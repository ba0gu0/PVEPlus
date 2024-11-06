<template>
  <el-form :model="exportData" label-position="top" label-width="150px" size="large">
    <el-row style="margin-top: 20px">
      <el-col :span="6" :offset="8">
        <el-form-item label="导出磁盘类型">
          <el-select v-model="exportData.diskType" size="large" style="width: 100%">
            <el-option label="原始镜像格式 (RAW)" value="raw"/>
            <el-option label="QEMU镜像格式 (QCOW2)" value="qcow2"/>
            <el-option label="VMware镜像格式(VMDK)" value="vmdk"/>
            <el-option label="VirtualBox镜像格式(VDI)" value="vdi"/>
          </el-select>
        </el-form-item>
      </el-col>
    </el-row>
    <el-row style="margin-top: 20px">
      <el-col :span="8" :offset="8">
        <el-form-item label="选择虚拟机">
          <el-select v-model="exportData.vmId" size="large" style="width: 100%" @change="selectVm">
            <el-option v-for="vm of vms" :label="vm.name" :value="vm.vmid.toString()"/>
          </el-select>
        </el-form-item>
      </el-col>
    </el-row>
    <el-row style="margin-top: 20px">
      <el-col :span="8" :offset="8">
        <el-form-item label="选择磁盘">
          <el-select v-model="exportData.vmDiskKey" size="large" style="width: 100%">
            <el-option v-for="vmDisk of vmDisks" :label="vmDisk.value" :value="vmDisk.key"/>
          </el-select>
        </el-form-item>
      </el-col>
    </el-row>
    <el-row style="margin-top: 20px">
      <el-col :span="2" :offset="10">
        <el-button style="width: 100%; height: 45px" size="large" type="success" @click="doExportVm">导出</el-button>
      </el-col>
    </el-row>
  </el-form>
</template>

<script setup>
import {ref} from "vue";
import {getVmDisk, getVms} from "@/libs/pve";
import {msgBox} from "@/libs/msgBox";
import {exportDisk} from "@/libs/pve";
import {router} from "@/router";


const props = defineProps({
  vmId: String
})

const exportData = ref({
  diskType: 'qcow2', // raw, qcow2, vmdk, vdi
  vmId: '',
  vmDiskKey: ''
})

if (props.vmId) {
  exportData.value.vmId = props.vmId
  getVmDisk(exportData.value.vmId)
    .then(res => {
      vmDisks.value = res
    })
}

const vms = ref()

getVms()
  .then(res => {
    vms.value = res
  })

const vmDisks = ref()
const selectVm = ()=>{
  getVmDisk(exportData.value.vmId)
    .then(res => {
      vmDisks.value = res
      exportData.value.vmDiskKey = ''
    })
}
const doExportVm = ()=>{
  if (!exportData.value.vmId || !exportData.value.vmDiskKey) {
    msgBox('请选择虚拟机、选择磁盘.', 'error', 'alert')
    return
  }
  exportDisk(exportData.value)
    .then((res)=>{
      if (res === true){
        msgBox('开始导出...', 'success', 'alert', ()=>{
          router.push('/refresh')
        })
      }else {
        msgBox(res.msg, 'error', 'alert')
      }
    })
}

</script>

<style scoped>

</style>