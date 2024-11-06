import { ElMessage, ElMessageBox } from 'element-plus'

export const msgBox = (message, messageType = 'info', boxType = 'alert', callbackThen = ()=>{}, callbackCatch = ()=>{}) => {
  switch (boxType) {
    case 'alert':
      ElMessageBox.alert(
        message,
        messageType,
        {
        type: messageType,
      })
        .then(r => callbackThen(r))
        .catch(r => callbackCatch(r))
      break
    case 'confirm':
      ElMessageBox.confirm(
        message,
        messageType,
        {
        type: messageType
      })
        .then(r => callbackThen(r))
        .catch(r => callbackCatch(r))
      break
    case 'prompt':
      ElMessageBox.prompt(
        message,
        messageType,
        {
        confirmButtonText: message,
        type: messageType
      })
        .then(r => callbackThen(r))
        .catch(r => callbackCatch(r))
      break
  }
}