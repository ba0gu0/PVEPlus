import axios from 'axios'

async function getVmDisk(vmId){
    const res = await axios.postForm(
    '/api/pve/vm/disks',
    {
        vmId: vmId
    })
    return res.data.code === 200 ? res.data.data : []
}

export { getVmDisk }