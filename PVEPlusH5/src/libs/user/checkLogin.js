import axios from 'axios'

async function checkLogin(){
    const res = await axios.get('/api/user/info')
    return res.data.code === 200;
}

export { checkLogin }