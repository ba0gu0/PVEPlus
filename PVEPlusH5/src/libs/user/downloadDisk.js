import axios from 'axios'

async function downloadDisk(diskId){

  const eleLink = document.createElement('a');

  eleLink.style.display = 'none';
  // // 字符内容转变成blob地址
  eleLink.href = '/api/user/disks/download?diskId=' + diskId;
  // // 触发点击
  document.body.appendChild(eleLink);
  eleLink.click();
  // // 然后移除
  document.body.removeChild(eleLink);

  return true
}

export { downloadDisk }