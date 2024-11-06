#! coding=utf-8
import json
import os.path
import re
import threading
import time
import uuid
import pickle
from functools import wraps
from flask import Flask, render_template, session, jsonify, request, make_response, send_file, redirect
from proxmoxer import AuthenticationError
from requests import ConnectTimeout
from flask_session import Session
from libs.Funs import *
from libs.PVE import Proxmox
from libs.TASK import ExportTask, ImportTask

PVEHost = '127.0.0.1'
# PVEHost = '192.168.179.50'

UploadDir = './AppData/Upload/'

app = Flask(
    __name__,
    static_folder='static',
    template_folder='templates'
)

app.secret_key = os.urandom(20)
# app.secret_key = b'\xcb\xb2V\xdb\xb2Z\x9d/\n8\x95cws\xa6\xdcb1\xc8\xb1'

app.config['SESSION_FILE_DIR'] = './AppData/Sessions/'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_USE_SIGNER'] = True

Session(app)


def login_required(func):
    @wraps(func)  # 修饰内层函数，防止当前装饰器去修改被装饰函数的属性
    def inner(*args, **kwargs):
        # 从session获取用户信息，如果有，则用户已登录，否则没有登录
        proxmox = session.get('proxmox')
        if not proxmox:
            return jsonify(code=400, msg="用户未登录")
        else:
            if not pickle.loads(proxmox).check_auth():
                session.clear()
                return jsonify(code=400, msg="pve认证已过期,重新登陆.")
            return func(*args, **kwargs)

    return inner


@app.errorhandler(404)
def error_handler(error):
    return redirect('/')


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/api/user/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    auth_type = request.form.get('authType', default='pam')

    if not username or not auth_type or not password:
        return jsonify(code=400, msg="账户密码不能为空")
    try:
        proxmox = Proxmox(username=f'{username}@{auth_type}', password=password, host=PVEHost)
    except AuthenticationError as e:
        print(e)
        return jsonify(code=400, msg="账户密码错误")
    except ConnectTimeout as e:
        print(e)
        return jsonify(code=500, msg="服务器地址错误")
    except Exception as e:
        print(e)
        return jsonify(code=500, msg="未知错误")
    session['proxmox'] = pickle.dumps(proxmox)
    session['username'] = username
    session['upload_dir'] = os.path.join(UploadDir, username)
    session['upload_temp_dir'] = os.path.join(UploadDir, username, 'temp')
    session['disk_info_file_path'] = os.path.join(session['upload_dir'], 'files.json')
    session['task_id'] = None

    if not os.path.exists(session['upload_dir']):
        os.mkdir(session['upload_dir'])
    if not os.path.exists(session['upload_temp_dir']):
        os.mkdir(session['upload_temp_dir'])
    if not os.path.exists(session['disk_info_file_path']):
        with open(session['disk_info_file_path'], 'w') as file:
            json.dump([], file)

    clear_temp_dir(session['upload_temp_dir'])

    return jsonify(code=200, msg="登陆成功")


@app.route('/api/user/logout')
def logout():
    clear_temp_dir(session['upload_temp_dir'])
    session.clear()
    return jsonify(code=200, msg="注销成功")


@app.route('/api/user/info')
@login_required
def get_info():
    return jsonify(code=200, msg="ok")


# 生成新虚拟机id
@app.route('/api/pve/nextid')
@login_required
def get_nextid():
    nextid = pickle.loads(session['proxmox']).get_nextid()
    return jsonify(code=200, data=nextid) if nextid != False else jsonify(code=500, msg="获取节点ID失败")


# 节点列表
@app.route('/api/pve/nodes')
@login_required
def get_nodes():
    nodes = pickle.loads(session['proxmox']).get_nodes()
    return jsonify(code=200, data=nodes) if nodes != False else jsonify(code=500, msg="获取节点失败")


# 存储池列表
@app.route('/api/pve/pools')
@login_required
def get_pools():
    pools = pickle.loads(session['proxmox']).get_pools()
    return jsonify(code=200, data=pools) if pools != False else jsonify(code=500, msg="获取资源池失败")


# 存储列表
@app.route('/api/pve/storages')
@login_required
def get_storages():
    storages = pickle.loads(session['proxmox']).get_storages()
    return jsonify(code=200, data=storages) if storages != False else jsonify(code=500, msg="获取存储池失败")


# 虚拟机列表
@app.route('/api/pve/vms')
@login_required
def get_vms():
    vms = pickle.loads(session['proxmox']).get_vms()
    return jsonify(code=200, data=vms) if vms != False else jsonify(code=500, msg="获取虚拟机列表失败")


# 文件列表
@app.route('/api/user/disks')
@login_required
def get_disk():
    with open(session['disk_info_file_path'], 'r') as f:
        disks = json.load(f)
    return jsonify(code=200, data=disks)


# 获取虚拟机磁盘信息
@app.route('/api/pve/vm/disks', methods=['POST'])
@login_required
def get_vm_disks():
    vm_id = int(request.form.get('vmId') if request.form.get('vmId').isdigit() else None)

    vms = pickle.loads(session['proxmox']).get_vms()
    vm = (lambda _: _[0] if len(_) > 0 else None)(list(filter(lambda _: _['vmid'] == vm_id, vms)))

    if not vm_id or not vm:
        return jsonify(code=400, msg="输入的vmId有误")

    vm_disks = pickle.loads(session['proxmox']).get_vm_disks(vm['vmid'], vm['node'])

    return jsonify(code=200, data=vm_disks) if vm_disks != False else jsonify(code=500, msg="获取虚拟机信息失败")


# 获取虚拟机配置信息
@app.route('/api/pve/vm/disks/unused', methods=['POST'])
@login_required
def get_vm_disks_unused():
    vm_id = int(request.form.get('vmId') if request.form.get('vmId').isdigit() else None)

    vms = pickle.loads(session['proxmox']).get_vms()
    vm = (lambda _: _[0] if len(_) > 0 else None)(list(filter(lambda _: _['vmid'] == vm_id, vms)))

    if not vm_id or not vm:
        return jsonify(code=400, msg="输入的vmId有误")

    unused_vm_disks = pickle.loads(session['proxmox']).get_vm_disks_unused(vm['vmid'], vm['node'])

    return jsonify(code=200, data=unused_vm_disks) if unused_vm_disks != False else jsonify(code=500,
                                                                                            msg="获取虚拟机信息失败")


# 获取虚拟机配置信息
@app.route('/api/pve/vm/disks/mount', methods=['POST'])
@login_required
def mount_vm_disk():
    vm_id = int(request.form.get('vmId') if request.form.get('vmId').isdigit() else None)
    mount_disk_id = request.form.get('mountDiskId')
    mount_disk_key = request.form.get('mountDiskKey')
    fist_boot = request.form.get('fistBoot')

    vms = pickle.loads(session['proxmox']).get_vms()
    vm = (lambda _: _[0] if len(_) > 0 else None)(list(filter(lambda _: _['vmid'] == vm_id, vms)))

    if not vm_id or not vm:
        return jsonify(code=400, msg="输入的vmId有误")

    unmount_disks = pickle.loads(session['proxmox']).get_vm_disks_unused(vm['vmid'], vm['node'])

    unmount_disk = (lambda _: _[0] if len(_) > 0 else None)(
        list(filter(lambda _: _['key'] == mount_disk_id, unmount_disks)))

    if not mount_disk_id or not unmount_disk:
        return jsonify(code=400, msg="输入的mountDiskId有误")

    check_disk_key_format = any(
        re.search(_, mount_disk_key) for _ in [r'^ide\d+$', r'^sata\d+$', r'^scsi\d+$', r'^virtio\d+$'])
    vm_disks = pickle.loads(session['proxmox']).get_vm_disks(vm['vmid'], vm['node'])
    check_disk_key_used = (lambda _: _[0] if len(_) > 0 else None)(
        list(filter(lambda _: _['value'] == mount_disk_key, vm_disks)))

    if not mount_disk_key or not check_disk_key_format or check_disk_key_used:
        return jsonify(code=400, msg="输入的mountDiskKey有误")

    if any(re.search(_, mount_disk_key) for _ in [r'^scsi\d+$', r'^virtio\d+$']):
        mount_disk_result = pickle.loads(session['proxmox']).mount_vm_disk(vm['vmid'], vm['node'], {
            mount_disk_key: f'{unmount_disk["value"]},iothread=on', 'background_delay': 5})
    else:
        mount_disk_result = pickle.loads(session['proxmox']).mount_vm_disk(vm['vmid'], vm['node'],
                                                                           {mount_disk_key: f'{unmount_disk["value"]}',
                                                                            'background_delay': 5})

    if fist_boot == 'true':
        boot_order = pickle.loads(session['proxmox']).get_vm_boot(vm['vmid'], vm['node']).strip()
        if boot_order != '':
            boot_order = re.sub(r'=', f'={mount_disk_key};', boot_order)
        else:
            boot_order = f'order={mount_disk_key}'

        set_boot_order_result = pickle.loads(session['proxmox']).set_vm_boot_order(vm['vmid'], vm['node'],
                                                                                   {'boot': boot_order})
        return jsonify(code=200,
                       msg='挂载磁盘成功.') if mount_disk_result != False and set_boot_order_result != False else jsonify(
            code=500, msg="挂载磁盘失败.")
    else:
        return jsonify(code=200, msg='挂载磁盘成功.') if mount_disk_result != False else jsonify(code=500,
                                                                                                 msg="挂载磁盘失败.")


# 文件列表
@app.route('/api/user/disks/delete', methods=['POST'])
@login_required
def delete_disk():
    with open(session['disk_info_file_path'], 'r') as f:
        disks = json.load(f)

    disk_id = request.form.get('diskId')
    disk = (lambda _: _[0] if len(_) > 0 else None)(list(filter(lambda _: _["uuid"] == disk_id, disks)))

    if not disk_id or not disk:
        return jsonify(code=400, msg="输入的disk_id有误")

    delete_file_path = os.path.join(session['upload_dir'], disk_id)
    disk_info_file_path = session['disk_info_file_path']

    if os.path.exists(delete_file_path):
        os.remove(delete_file_path)

    disks = list(filter(lambda _: _["uuid"] != disk_id, disks))
    with open(disk_info_file_path, 'w') as file:
        json.dump(disks, file)
    return jsonify(code=200, msg='删除成功')


# 下载
@app.route('/api/user/disks/download', methods=['GET'])
@login_required
def download_disk():
    disk_id = request.args.get('diskId')
    with open(session['disk_info_file_path'], 'r') as f:
        disks = json.load(f)

    disk = (lambda _: _[0] if len(_) > 0 else None)(list(filter(lambda _: _["uuid"] == disk_id, disks)))
    if not disk_id or not disk:
        return jsonify(code=400, msg="输入的disk_id有误")

    download_file_path = os.path.join(session['upload_dir'], disk_id)
    download_file_name = disk['filename']
    if os.path.exists(download_file_path):
        return make_response(send_file(download_file_path, as_attachment=True, download_name=download_file_name))
    else:
        return jsonify(code=400, msg="文件不存在.")


# 上传
@app.route('/api/user/disks/upload', methods=['POST'])
@login_required
def upload_disk():
    # 获取上传参数和分片数据
    identifier = request.form.get('identifier')
    filename = request.form.get('filename')
    total_chunks = int(request.form.get('totalChunks') if request.form.get('totalChunks').isdigit() else None)
    chunk_number = int(request.form.get('chunkNumber') if request.form.get('chunkNumber').isdigit() else None)
    chunk_file = request.files['file']

    # 根据用户名创建临时目录

    temp_dir = session['upload_temp_dir']

    # 将分片数据保存到临时文件中
    chunk_file.save(os.path.join(temp_dir, '{}_{}'.format(identifier, chunk_number)))

    # 返回上传进度信息
    uploaded_chunks = [f for f in os.listdir(temp_dir) if f.startswith(identifier)]
    return jsonify({
        'code': 200,
        'success': False,
        'msg': '上传中...',
        'uploadedChunks': len(uploaded_chunks),
        'totalChunks': total_chunks,
    })


# 上传
@app.route('/api/user/disks/upload/merge', methods=['POST'])
@login_required
def merge_disk():
    # 获取上传参数
    identifier = request.form.get('identifier')
    filename = request.form.get('fileName')
    filetype = request.form.get('diskType')
    total_chunks = int(request.form.get('totalChunks') if request.form.get('totalChunks').isdigit() else None)

    # 根据用户名创建临时目录
    temp_dir = session['upload_temp_dir']

    # 检查是否所有分片都已上传完成
    chunks = [f for f in os.listdir(temp_dir) if f.startswith(identifier)]
    if len(chunks) != total_chunks:
        # 返回错误信息
        return jsonify({
            'code': 500,
            'msg': '有一个或多个分片未上传'
        })

    # 对分片按照编号进行排序
    sorted_chunks = sorted(chunks, key=lambda x: int(x.split('_')[-1] if x.split('_')[-1].isdigit() else None))

    diskinfo = {
        'filename': filename,
        'uuid': str(uuid.uuid4()),
        'type': filetype,
        'source': 'upload'
    }

    # 将所有分片依次合并为完整文件
    with open(os.path.join(session['upload_dir'], diskinfo['uuid']), 'wb') as target_file:
        for chunk in sorted_chunks:
            chunk_file = open(os.path.join(temp_dir, chunk), 'rb')
            target_file.write(chunk_file.read())
            chunk_file.close()

    with open(session['disk_info_file_path'], 'r') as f:
        disks = json.load(f)
    disks.append(diskinfo)
    with open(session['disk_info_file_path'], 'w') as f:
        json.dump(disks, f)

    # 删除临时文件
    for chunk in chunks:
        os.remove(os.path.join(temp_dir, chunk))

    # 返回上传成功信息
    return jsonify({
        'code': 200,
        'msg': f'文件{filename}上传成功.',
    })


# 导出
@app.route('/api/pve/export', methods=['POST'])
@login_required
def export_disk():
    vms = pickle.loads(session['proxmox']).get_vms()
    with open(session['disk_info_file_path'], 'r') as f:
        disks = json.load(f)

    vm_id = int(request.form.get('vmId') if request.form.get('vmId').isdigit() else None)
    vm = (lambda _: _[0] if len(_) > 0 else None)(list(filter(lambda _: _['vmid'] == vm_id, vms)))
    if not vm_id or not vm:
        return jsonify(code=400, msg="输入的vmId有误")

    vm_disk_key = request.form.get('vmDiskKey')
    vm_disks = pickle.loads(session['proxmox']).get_vm_disks(vm['vmid'], vm['node'])
    vm_disk_value = (lambda _: _[0]['value'] if len(_) > 0 else None)(
        list(filter(lambda _: _['key'] == vm_disk_key, vm_disks)))
    if not vm_disk_value:
        return jsonify(code=400, msg="输入的vm_disk_key有误")

    disk_type = request.form.get('diskType')
    diskinfo = {
        'filename': vm['name'] + '.' + disk_type,
        'uuid': str(uuid.uuid4()),
        'type': disk_type,
        'source': 'export'
    }

    if len(list(filter(lambda _: _['filename'] == diskinfo['filename'], disks))) != 0:
        return jsonify(code=400, msg="虚拟机已经导出, 重新导出请删除之前文件.")
    task = [thread for thread in threading.enumerate() if
            isinstance(thread, ExportTask) and thread.ident == session.get('task_id')]
    if len(task) > 0:
        return jsonify(code=400, msg="存在正在进行的任务, 请稍后!")
    else:
        task = ExportTask(vm_disk_value.split(',')[0], diskinfo, session['disk_info_file_path'])
        task.start()
        session['task_id'] = task.ident
        return jsonify(code=200, msg="任务已开始")


# 导入
@app.route('/api/pve/import', methods=['POST'])
@login_required
def import_disk():
    vms = pickle.loads(session['proxmox']).get_vms()
    storages = pickle.loads(session['proxmox']).get_storages()
    with open(session['disk_info_file_path'], 'r') as f:
        disks = json.load(f)

    import_type = request.form.get('importType')
    os_version = request.form.get('systemVersion')
    vm_id = int(request.form.get('vmId') if request.form.get('vmId').isdigit() else None)
    cores = int(request.form.get('cores') if request.form.get('cores').isdigit() else None)
    sockets = int(request.form.get('sockets') if request.form.get('sockets').isdigit() else None)
    memory = int(request.form.get('memory') if request.form.get('memory').isdigit() else None)
    disk_id = request.form.get('diskId')
    node = request.form.get('node')
    pool = request.form.get('pool')
    vm_name = request.form.get('vmName')
    storage_id = request.form.get('storageId')

    if import_type == 'existQemu':
        if not disk_id or not vm_id or not storage_id:
            return jsonify(code=400, msg="输入的参数有误")

        disk = (lambda _: _[0] if len(_) > 0 else None)(list(filter(lambda _: _["uuid"] == disk_id, disks)))

        vm = (lambda _: _[0] if len(_) > 0 else None)(list(filter(lambda _: _['vmid'] == vm_id, vms)))

        storage = (lambda _: _[0] if len(_) > 0 else None)(list(filter(lambda _: _['storage'] == storage_id, storages)))

        if not vm or not disk or not storage:
            return jsonify(code=400, msg="输入的vmId、diskId、storageId有误")

    elif import_type == 'newQemu':
        if not os_version or not vm_id or not cores or not sockets or not memory or not disk_id or not node or not pool or not vm_name or not storage_id:
            return jsonify(code=400, msg="输入的参数有误")

        disk = (lambda _: _[0] if len(_) > 0 else None)(list(filter(lambda _: _["uuid"] == disk_id, disks)))

        storage = (lambda _: _[0] if len(_) > 0 else None)(list(filter(lambda _: _['storage'] == storage_id, storages)))

        if not disk or not storage:
            return jsonify(code=400, msg="输入的diskId、storageId有误")
        create_vm_data = {
            'vmid': vm_id,
            'name': vm_name,
            'pool': pool,
            'ide2': 'none,media=cdrom',
            'ostype': os_version,
            'scsihw': 'virtio-scsi-single',
            'sockets': sockets,
            'cores': cores,
            'numa': '0',
            'memory': memory
        }
        create_result = pickle.loads(session['proxmox']).create_vms(node, create_vm_data)
        if not create_result:
            return jsonify(code=500, msg="创建虚拟机失败, 请检查对资源、节点是否有权限...")
    else:
        return jsonify(code=400, msg="输入的参数有误")

    import_disk_file_path = os.path.join(session['upload_dir'], disk_id)
    task = [thread for thread in threading.enumerate() if
            isinstance(thread, ExportTask) and thread.ident == session.get('task_id')]
    if len(task) > 0:
        return jsonify(code=400, msg="存在正在进行的任务, 请稍后!")
    else:
        task = ImportTask(vm_id, import_disk_file_path, storage_id)
        task.start()
        session['task_id'] = task.ident
        return jsonify(code=200, msg="任务已开始")


# 获取任务进度和结果
@app.route('/api/pve/task')
@login_required
def get_task():
    task = [thread for thread in threading.enumerate() if
            isinstance(thread, ExportTask) or isinstance(thread, ImportTask) and thread.ident == session.get('task_id')]
    if len(task) > 0:
        return jsonify(code=200, progress=task[0].get_progress(), time=int(time.time() - task[0].get_start_time()))
    else:
        # session['task_id'] = None
        return jsonify(code=400, msg="暂无任务")


# 停止任务
@app.route('/api/pve/task/stop')
@login_required
def stop_task():
    task = [thread for thread in threading.enumerate() if
            isinstance(thread, ExportTask) and thread.ident == session.get('task_id')]
    if len(task) > 0:
        task[0].stop()
        session['task_id'] = None
        return jsonify(code=200, msg="任务已停止")
    else:
        return jsonify(code=400, msg="暂无任务")


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=9000)
