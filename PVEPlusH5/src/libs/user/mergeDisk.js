import axios from 'axios'

async function mergeDisk(filename, diskType, identifier, totalChunks){
    const res = await axios.postForm(
  '/api/user/disks/upload/merge',
  {
      fileName: filename,
      diskType: diskType,
      identifier: identifier,
      totalChunks: totalChunks
    })
    return res.data
}

export { mergeDisk }