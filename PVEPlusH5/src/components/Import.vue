<template>
  <el-form :model="importData" label-position="top" label-width="150px" size="large">
    <el-row style="margin-top: 20px">
      <el-col :span="4" :offset="8">
        <el-form-item label="导入方式">
          <el-select v-model="importData.importType" size="large" style="width: 100%" @change="changeImportDataType">
            <el-option label="新建虚拟机进行导入" value="newQemu"/>
            <el-option label="导入到已存在的虚拟机" value="existQemu"/>
          </el-select>
        </el-form-item>
      </el-col>
    </el-row>
    <div v-if="importData.importType === 'existQemu'">
      <el-row style="margin-top: 20px">
        <el-col :span="7" :offset="8">
          <el-form-item label="选择虚拟机">
            <el-select v-model="importData.vmId" size="large" style="width: 100%">
              <el-option v-for="vm of vms" :label="vm.name" :value="vm.vmid.toString()"/>
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>
    </div>
    <div v-else>
      <el-row style="margin-top: 20px">
        <el-col :span="2" :offset="8">
          <el-form-item label="虚拟机ID">
            <el-input v-model="importData.vmId" size="large" disabled></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="2" :offset="1">
          <el-form-item label="选择节点">
            <el-select v-model="importData.node" size="large" style="width: 100%">
              <el-option v-for="node of nodes" :label="node.node" :value="node.node"/>
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="4" :offset="1">
          <el-form-item label="选择资源池">
            <el-select v-model="importData.pool" size="large" style="width: 100%">
              <el-option v-for="pool of pools" :label="pool.comment" :value="pool.poolid"/>
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row style="margin-top: 20px">
        <el-col :span="2" :offset="8">
          <el-form-item label="设置CPU插槽">
            <el-input-number
              v-model="importData.cores"
              :min="1"
              :max="4"
              controls-position="right"
              size="large"
              @change="intNum"
            />
          </el-form-item>
        </el-col>
        <el-col :span="2" :offset="1">
          <el-form-item label="设置CPU核心">
            <el-input-number
              v-model="importData.sockets"
              :min="1"
              :max="8"
              controls-position="right"
              size="large"
              @change="intNum"
            />
          </el-form-item>
        </el-col>
        <el-col :span="4" :offset="1">
          <el-form-item label="设置内存(MB)">
            <el-input-number
              v-model="importData.memory"
              :min="512"
              :max="8192"
              controls-position="right"
              size="large"
              :step="512"
              @change="intNum"
            />
          </el-form-item>
        </el-col>
      </el-row>
      <el-row style="margin-top: 20px">
        <el-col :span="5" :offset="8">
          <el-form-item label="操作系统类别">
            <el-select v-model="importData.systemType" size="large" style="width: 100%" @change="changeSystemList">
              <el-option label="Linux" value="linux"/>
              <el-option label="Microsoft Windows" value="windows"/>
              <el-option label="Solaris Kernel" value="solaris"/>
              <el-option label="Other" value="other"/>
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="5" :offset="1">
          <el-form-item label="操作系统版本">
            <el-select v-model="importData.systemVersion" size="large" style="width: 100%">
              <el-option v-for="systemType of systemTypeList" :label="systemType.label" :value="systemType.key"/>
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row style="margin-top: 20px">
        <el-col :span="6" :offset="8">
          <el-form-item label="虚拟机名称">
            <el-input v-model="importData.vmName" size="large" placeholder="虚拟机名字, 仅能输入大小写、数字、-、." @change="changeVmName"/>
          </el-form-item>
        </el-col>
      </el-row>
    </div>
    <el-row style="margin-top: 20px">
      <el-col :span="8" :offset="8">
        <el-form-item label="选择存储池">
          <el-select v-model="importData.storageId" size="large" style="width: 100%">
            <el-option v-for="storage of storages" :label="storage.storage" :value="storage.storage"/>
          </el-select>
        </el-form-item>
      </el-col>
    </el-row>
    <el-row style="margin-top: 20px">
      <el-col :span="8" :offset="8">
        <el-form-item label="选择磁盘">
          <el-select v-model="importData.diskId" size="large" style="width: 100%">
            <el-option v-for="disk of disks" :label="disk.filename" :value="disk.uuid"/>
          </el-select>
        </el-form-item>
      </el-col>
    </el-row>
    <el-row style="margin-top: 20px">
      <el-col :span="2" :offset="10" >
        <el-button style="width: 100%; height: 45px" size="large" type="success" @click="doImportVm">导入</el-button>
      </el-col>
    </el-row>
  </el-form>
</template>

<script setup>
import {ref} from "vue";
import {getNodes, getPools, getStorages, getVms, importDisk} from "@/libs/pve";
import {getDisks} from "@/libs/user";
import {getNextId} from "@/libs/pve/getNextId";
import {msgBox} from "@/libs/msgBox";
import {router} from "@/router";
import {loadingFun} from "@/libs/loading";

const props = defineProps({
  vmId: String,
  diskId: String
})

const importData = ref({
  importType: 'existQemu',  //   existQemu   newQemu
  systemType: 'linux',
  systemVersion: 'l26',
  cores: 1,
  sockets: 1,
  memory: 1024,
  diskId: '',
  vmId: '',
  node: '',
  pool: '',
  vmName: '',
  storageId: ''
})

if (props.vmId && props.vmId !== 'null') {
  importData.value.vmId = props.vmId
  importData.value.importType = 'existQemu'
}

if (props.diskId && props.diskId !== 'null') {
  importData.value.diskId = props.diskId
}

const vms = ref()
getVms()
  .then(res => {
    vms.value = res
  })

const disks = ref()
getDisks()
  .then(res => {
    disks.value = res
  })

const nodes = ref()
getNodes()
  .then(res => {
    nodes.value = res
  })


const storages = ref()
getStorages()
  .then(res => {
    storages.value = res
  })

const pools = ref()
getPools()
  .then(res => {
    pools.value = res
  })
const systemTypeList = ref([
  {
    label: '5.x-2.6 Kernel',
    key: 'l26'
  },
  {
    label: '2.4 Kernel',
    key: 'l24'
  }
])

const changeSystemList = ()=>{
  importData.value.systemVersion = ''
  switch (importData.value.systemType) {
    case 'linux':
      break
    case 'windows':
      systemTypeList.value = [
        {
          label: '11/2022',
          key: 'win11'
        },
        {
          label: '10/2016/2019',
          key: 'win10'
        },
        {
          label: '8.x/2012/2012r2',
          key: 'win8'
        },
        {
          label: '7/2008r2',
          key: 'win7'
        }
        ,
        {
          label: 'vista/2008',
          key: 'w2k8'
        },
        {
          label: 'xp/2003',
          key: 'wxp'
        },
        {
          label: '2000',
          key: 'w2k'
        }
      ]
      break
    case 'solaris':
      systemTypeList.value = [
        {
          label: '-',
          key: 'solatis'
        }
      ]
      break
    case 'other':
      systemTypeList.value = [
        {
          label: '-',
          key: 'other'
        }
      ]
      break
  }
}
const intNum = ()=>{
  importData.value.cores = parseInt(importData.value.cores)
  importData.value.sockets = parseInt(importData.value.sockets)
  importData.value.memory = parseInt(importData.value.memory)
}
const changeImportDataType = async ()=>{
  if (importData.value.importType === 'newQemu'){
    const nextId = await getNextId()
    if (nextId !== false){
      importData.value.vmId = nextId
    }else {
      msgBox('无法获取新的虚拟机ID.')
    }
  }else {
    importData.value = {
      importType: 'existQemu',  //   existQemu   newQemu
      systemType: 'linux',
      systemVersion: 'l26',
      cores: 1,
      sockets: 1,
      memory: 1024,
      diskId: '',
      vmId: '',
      node: '',
      pool: '',
      vmName: '',
      storageId: ''
    }
  }
}
const changeVmName = ()=>{
  importData.value.vmName = importData.value.vmName.replace(/[^A-Za-z\d\-\\.]/g, '');
}

const loading = ref()
const doImportVm = ()=>{
  if (!importData.value.diskId || !importData.value.storageId){
    msgBox('请选择磁盘、存储池进行导入...', 'error', 'alert')
    return
  }
  if (importData.value.importType === 'existQemu'){
    if (!importData.value.vmId){
      msgBox('请选择虚拟机进行导入...', 'error', 'alert')
      return
    }
  }else {
    if (!importData.value.pool || !importData.value.node || !importData.value.vmName){
      msgBox('创建新的虚拟机, 需要指定节点、资源池、虚拟机名字...', 'error', 'alert')
      return
    }
  }

  if (importData.value.importType === 'newQemu') loading.value = loadingFun('正在创建虚拟机...')
  importDisk(importData.value)
    .then(res => {
      if (res === true){
        msgBox('虚拟机查创建完成, 开始导入磁盘...', 'success', "alert", ()=>{
          router.push('/refresh')
        })
      }else {
        msgBox(res.msg, 'error', 'alert')
      }
      if (loading.value) loading.value.close()
    })
  console.log(importData.value)
}
</script>

<style scoped>
</style>