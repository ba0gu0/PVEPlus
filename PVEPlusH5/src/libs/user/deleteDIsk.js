import axios from 'axios'

async function deleteDisk(diskId){
    const res = await axios.postForm(
  '/api/user/disks/delete',
  {
      diskId: diskId
    })
    return res.data.code === 200 ? true : res.data;
}

export { deleteDisk }