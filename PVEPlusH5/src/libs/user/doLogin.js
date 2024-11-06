import axios from 'axios'

async function doLogin(username, password, authType){
    const res = await axios.postForm('/api/user/login', {
      username: username,
      password: password,
      authType: authType
    })
    return res.data.code === 200 ? true : res.data;
}

export { doLogin }