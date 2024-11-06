<template>

  <el-row style="margin: 20px;">
    <el-col :span="7" style="margin-left: 45px;">
      <span>节点</span>
    </el-col>
    <el-col :span="7" style="margin-left: 45px">
      <span>资源池</span>
    </el-col>
    <el-col :span="7" style="margin-left: 45px">
      <span>存储</span>
    </el-col>
  </el-row>
  <el-row style="margin: 20px;">
    <el-col :span="7" style="margin-left: 40px">
      <el-card style="width: 100%;">
        <el-table :data="nodesData" height="200" empty-text="暂无数据..." stripe border>
          <el-table-column prop="id" label="节点ID" align="center"/>
          <el-table-column prop="node" label="节点" align="center"/>
        </el-table>
      </el-card>
    </el-col>
    <el-col :span="7" style="margin-left: 40px">
      <el-card style="width: 100%;">
        <el-table :data="poolsData" height="200" empty-text="暂无数据..." stripe border>
          <el-table-column prop="poolid" label="资源池ID" align="center"/>
          <el-table-column prop="comment" label="资源池" align="center"/>
        </el-table>
      </el-card>
    </el-col>
    <el-col :span="7" style="margin-left: 40px">
      <el-card style="width: 100%;">
        <el-table :data="storagesData" height="200" empty-text="暂无数据..." stripe border>
          <el-table-column prop="storage" label="存储ID" align="center"/>
          <el-table-column prop="type" label="存储类别" align="center"/>
          <el-table-column prop="content" label="存储内容类型" align="center"/>
        </el-table>
      </el-card>
    </el-col>
  </el-row>


  <el-row style="margin: 20px 50px">
    <el-col :span="4">
      <span>虚拟机列表</span>
    </el-col>
  </el-row>
  <el-row style="margin: 20px">
    <el-card style="width: 100%">
      <el-table :data="vmsData" height="250" empty-text="暂无数据..." stripe border>
        <el-table-column prop="name" label="虚拟机名字"/>
        <el-table-column prop="vmid" label="虚拟机ID" width="100" align="center"/>
        <el-table-column prop="pool" label="存储池位置" width="200" align="center"/>
        <el-table-column prop="status" label="虚拟机状态" width="100" align="center"/>
        <el-table-column prop="type" label="类型" width="100" align="center"/>
        <el-table-column prop="node" label="节点位置" width="100" align="center"/>
        <el-table-column label="磁盘" width="200" align="center">
          <template #default="scope">
            <el-button
              size="small"
              type="primary"
              @click="importDiskFromVM(scope)"
            >导入</el-button>
            <el-button
              size="small"
              type="success"
              @click="exportDiskFromVM(scope)"
            >导出</el-button>
            <el-button
              size="small"
              type="warning"
              @click="mountDiskFromVM(scope)"
            >挂载</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </el-row>
  <el-row style="margin: 20px 50px">
    <el-col :span="4">
      <span>磁盘列表</span>
    </el-col>
  </el-row>
  <el-row style="margin: 20px">
    <el-card style="width: 100%;">
    <el-table :data="disksData" height="250" empty-text="暂无数据..." stripe border>
      <el-table-column prop="filename" label="磁盘名字" />
      <el-table-column prop="uuid" label="磁盘ID" />
      <el-table-column prop="type" label="磁盘类型" width="100" align="center"/>
      <el-table-column prop="source" label="磁盘来源" width="100" align="center"/>
      <el-table-column label="管理" width="200" align="center">
        <template #default="scope">
          <el-button
            size="small"
            type="success"
            @click="downloadDiskFromUser(scope)"
          >下载</el-button>
          <el-button
            size="small"
            type="primary"
            @click="importDiskFromUser(scope)"
          >导入</el-button>
          <el-button
            size="small"
            type="danger"
            @click="deleteDiskFromUser(scope)"
            >删除</el-button
          >
        </template>
      </el-table-column>
    </el-table>
    </el-card>
  </el-row>
</template>

<script setup>
import {ref} from "vue";
import {getVms, getStorages, getPools, getNodes} from "@/libs/pve";
import {getDisks} from "@/libs/user";
import {msgBox} from "@/libs/msgBox";
import {router} from "@/router";
import {deleteDisk, downloadDisk} from "@/libs/user";

const vmsData = ref()
const disksData = ref()
const nodesData = ref()
const poolsData = ref()
const storagesData = ref()

getVms()
  .then((res)=>{
    vmsData.value = res
  })
  .catch((e)=>{
    console.log(e)
  })

getDisks()
  .then((res)=>{
    disksData.value = res
  })
  .catch((e)=>{
    console.log(e)
  })

getStorages()
  .then((res)=>{
    storagesData.value = res
  })
  .catch((e)=>{
    console.log(e)
  })

getPools()
  .then((res)=>{
    poolsData.value = res
  })
  .catch((e)=>{
    console.log(e)
  })

getNodes()
  .then((res)=>{
    nodesData.value = res
  })
  .catch((e)=>{
    console.log(e)
  })


const exportDiskFromVM = (scope)=>{
  const vmid = scope.row.vmid
  router.push("/export/" + vmid)
}

const downloadDiskFromUser = (scope)=>{
  const uuid = scope.row.uuid
  downloadDisk(uuid)
    .then((res)=>{
      if (res === true){
        msgBox('下载成功!', 'success')
      }else {
        msgBox(res.msg, 'error', 'alert')
      }
    })
}
const importDiskFromVM = (scope)=>{
  const vmId = scope.row.vmid
  router.push("/import/" + vmId + "/null")
}

const importDiskFromUser = (scope)=>{
  const diskId = scope.row.uuid
  router.push("/import/null/" + diskId)
}

const deleteDiskFromUser = (scope)=>{
  const uuid = scope.row.uuid
  msgBox('正在删除磁盘, 请确认?', 'error', 'confirm', ()=>{
    deleteDisk(uuid)
      .then((res)=>{
        if (res === true){
          msgBox('磁盘删除成功!', 'success', 'alert', ()=>{
            router.push('/refresh')
          })
        }else {
          msgBox(res.msg, 'error', 'alert')
        }
      })
  })

}

const mountDiskFromVM = (scope)=>{
  const vmId = scope.row.vmid
  router.push("/mount/" + vmId)
}
</script>

<style scoped>

</style>