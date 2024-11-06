import axios from 'axios'

async function getStorages(){
    const res = await axios.get('/api/pve/storages')
    return res.data.code === 200 ? res.data.data : []
}

export { getStorages }