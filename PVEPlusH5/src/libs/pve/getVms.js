import axios from 'axios'

async function getVms(){
    const res = await axios.get('/api/pve/vms')
    return res.data.code === 200 ? res.data.data : []
}

export { getVms }