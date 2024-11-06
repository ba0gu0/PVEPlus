import axios from 'axios'

async function getVmUnusedDisk(vmId){
    const res = await axios.postForm(
    '/api/pve/vm/disks/unused',
    {
        vmId: vmId
    })
    return res.data.code === 200 ? res.data.data : []
}

export { getVmUnusedDisk }