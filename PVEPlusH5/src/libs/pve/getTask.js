import axios from 'axios'

async function getTask(){
    const res = await axios.get('/api/pve/task')
    return res.data.code === 200 ? res.data : false
}

export { getTask }