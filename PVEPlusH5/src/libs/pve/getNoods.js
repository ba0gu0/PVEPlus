import axios from 'axios'

async function getNodes(){
    const res = await axios.get('/api/pve/nodes')
    return res.data.code === 200 ? res.data.data : []
}

export { getNodes }