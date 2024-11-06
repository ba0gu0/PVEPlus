import axios from 'axios'

async function doLogout(){
    const res = await axios.get('/api/user/logout')
    return res.data.code === 200;
}

export { doLogout }