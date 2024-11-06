import axios from 'axios'

async function mountVmDisk(mountData){
    const res = await axios.postForm(
    '/api/pve/vm/disks/mount',
    {
        vmId: mountData.vmId,
        mountDiskId: mountData.mountDiskId,
        mountDiskKey: mountData.mountDiskKey,
        fistBoot: mountData.fistBoot
    })
    return res.data.code === 200 ? true : res.data
}

export { mountVmDisk }