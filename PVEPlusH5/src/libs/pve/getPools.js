import axios from 'axios'

async function getPools(){
    const res = await axios.get('/api/pve/pools')
    return res.data.code === 200 ? res.data.data : []
}

export { getPools }