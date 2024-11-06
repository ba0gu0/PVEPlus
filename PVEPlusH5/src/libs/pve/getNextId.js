import axios from 'axios'

async function getNextId(){
    const res = await axios.get('/api/pve/nextid')
    return res.data.code === 200 ? res.data.data : false
}

export { getNextId }