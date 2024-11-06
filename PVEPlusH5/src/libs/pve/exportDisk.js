import axios from 'axios'

async function exportDisk(exportData){
    const res = await axios.postForm(
      '/api/pve/export',
      {
        vmId: exportData.vmId,
        diskType: exportData.diskType,
        vmDiskKey: exportData.vmDiskKey
      }
    )
    return res.data.code === 200 ? true : res.data
}

export { exportDisk }