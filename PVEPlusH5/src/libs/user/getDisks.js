import axios from 'axios'

async function getDisks(){
    const res = await axios.get('/api/user/disks')
    return res.data.code === 200 ? res.data.data : []
}

export { getDisks }