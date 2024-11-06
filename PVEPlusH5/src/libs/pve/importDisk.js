import axios from 'axios'

async function importDisk(importData){
    const res = await axios.postForm(
      '/api/pve/import',
      {
        importType: importData.importType,
        systemVersion: importData.systemVersion,
        vmId: importData.vmId,
        cores:  importData.cores,
        sockets:  importData.sockets,
        memory:  importData.memory,
        diskId:  importData.diskId,
        node:  importData.node,
        pool:  importData.pool,
        vmName:  importData.vmName,
        storageId: importData.storageId
      }
    )
    return res.data.code === 200 ? true : res.data
}

export { importDisk }