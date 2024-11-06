# PVE Plus - PVE虚拟机迁移助手

这是一个基于Python Flask和Vue.js开发的Web应用程序,用于辅助Proxmox VE(PVE)进行虚拟机迁移、导入导出操作。

## 主要功能

- 虚拟机磁盘导出(支持RAW/QCOW2/VMDK/VDI格式)
- 虚拟机磁盘导入(支持导入到新建或已有虚拟机)
- 虚拟机磁盘挂载(支持IDE/SATA/SCSI/VirtIO接口)
- 大文件分片上传
- 进度显示
- 支持PVE认证(PAM/PVE)

## 系统要求

- Proxmox VE 7.0+
- Python 3.8+
- Node.js 16+ (仅开发环境需要)

## 安装部署

1. 准备工作目录:
首先检查系统根目录空间:

```bash
# 检查根目录空间使用情况
df -h /
```

如果PVE系统`/`目录空间充足(建议>50G)，可以直接创建目录:

```bash
# 直接创建目录
mkdir -p /data/PVEPlus
cd /data/PVEPlus
git clone https://github.com/ba0gu0/PVEPlus.git .
```

如果`/`目录空间不足，需要先扩展存储卷(在PVE主节点执行):

```bash
# 创建200G的逻辑卷(根据实际磁盘大小调整)
lvcreate -V 200G -T pve/data -n PVEPlus

# 格式化为XFS文件系统
mkfs.xfs /dev/pve/PVEPlus

# 创建挂载点并挂载
mkdir /data/PVEPlus
mount /dev/pve/PVEPlus /data/PVEPlus

# 设置开机自动挂载
echo '/dev/pve/PVEPlus /data/PVEPlus xfs defaults 0 0' >> /etc/fstab

# 克隆项目代码
cd /data/PVEPlus
git clone https://github.com/ba0gu0/PVEPlus.git .
```

> 注意: 建议使用扩展存储卷的方式，这样可以避免系统盘空间不足的问题。

2. Python环境说明

PVE基于Debian系统，默认安装了Python3，但为了确保环境完整性，建议安装以下依赖：

```bash
# 安装Python开发环境和必要的系统库
apt-get update
apt-get install -y python3-pip python3-venv
apt-get install -y build-essential zlib1g-dev libffi-dev libssl-dev
apt-get install -y libbz2-dev libreadline-dev libsqlite3-dev liblzma-dev

# 检查Python版本
python3 --version  # 通常是3.9+版本

# 创建虚拟环境
cd /data/PVEPlus
python3 -m venv venv
source venv/bin/activate

# 安装项目依赖
pip install -r requirements.txt

```

3. 启动服务:

```bash
# 使用uWSGI启动
uwsgi --ini uWSGI.ini -d
```

## 使用说明

1. 访问系统(默认端口9000): http://pve-host:9000

2. 使用PVE用户登录(支持PAM和PVE认证)

3. 功能入口:
   - 上传 - 上传虚拟机磁盘文件
   - 导入 - 将磁盘导入到虚拟机
   - 导出 - 导出虚拟机磁盘
   - 挂载 - 挂载未使用的磁盘

## 注意事项

1. 需要在PVE主节点部署

2. 确保存储卷空间充足

3. 使用PVE认证用户登录,权限更完整

4. 大文件上传时注意浏览器超时设置

5. 建议使用虚拟环境(venv)来隔离项目依赖

6. PVE系统自带的Python包不建议修改，可能会影响系统运行

7. 如果pip安装过慢，可以使用国内镜像源：

```bash
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

## 技术栈

后端:
- Flask - Web框架
- proxmoxer - PVE API客户端
- uWSGI - WSGI服务器

前端:
- Vue 3 - 前端框架 
- Element Plus - UI组件库
- Axios - HTTP客户端
- Vue Router - 路由管理

## 目录结构

```
PVEPlus/
├── app.py              # Flask应用主入口
├── libs/               # 后端库文件
│   ├── PVE.py         # PVE API封装
│   ├── TASK.py        # 导入导出任务
│   └── Funs.py        # 工具函数
├── PVEPlusH5/         # 前端Vue项目
│   ├── src/
│   │   ├── components/  # Vue组件
│   │   └── libs/        # 前端库
│   └── index.html
├── static/            # 静态文件
├── templates/         # 模板文件
├── AppData/           # 应用数据
├── requirements.txt   # Python依赖
└── uWSGI.ini         # uWSGI配置
```

## 实现原理

#### 存储卷扩展
PVE默认的系统存储卷较小,不适合存储大量的虚拟机磁盘文件。本项目通过以下步骤扩展存储:

```bash
# 1. 创建新的逻辑卷(示例200G)
lvcreate -V 200G -T pve/data -n PVEPlus

# 2. 格式化并挂载
mkfs.xfs /dev/pve/PVEPlus
mkdir /data/PVEPlus
mount /dev/pve/PVEPlus /data/PVEPlus

# 3. 设置开机自动挂载
echo '/dev/pve/PVEPlus /data/PVEPlus xfs defaults 0 0' >> /etc/fstab
```

#### 虚拟机操作
项目通过PVE提供的命令行工具实现虚拟机操作:

1. 磁盘信息获取
```bash
# 获取虚拟机配置信息
qm config VMID

# 获取存储卷物理路径
pvesm path VOLUME-ID
```

2. 磁盘格式转换与导入
```bash
# 格式转换示例(raw转qcow2)
qemu-img convert -O qcow2 -f raw INPUT-PATH OUTPUT.qcow2

# 导入磁盘到虚拟机
qm disk import 105 disk.qcow2 local-lvm
```

#### API集成
项目封装了PVE的REST API,主要使用以下接口:

1. 基础信息查询
```
# 获取节点信息
GET /api2/json/nodes

# 获取存储卷信息
GET /api2/json/nodes/pve/storage?format=1&content=iso

# 获取可用VM ID
GET /api2/extjs/cluster/nextid
```

2. 虚拟机创建
```
# 创建虚拟机
POST /api2/extjs/nodes/pve/qemu

# 参数示例:
vmid=104                      # 虚拟机ID
name=xxx                      # 虚拟机名称
ostype=l26                    # 操作系统类型(l26=Linux 2.6+内核)
scsihw=virtio-scsi-single    # SCSI控制器类型
cores=2                       # CPU核心数
sockets=2                     # CPU插槽数
memory=2048                   # 内存大小(MB)
```

#### 操作系统类型对照表
```
Linux:
  5.x-2.6 Kernel:    l26
  2.4 Kernel:        l24

Windows:
  11/2022:           win11
  10/2016/2019:      win10
  8.x/2012/2012r2:   win8
  7/2008r2:          win7
  vista/2008:        w2k8
  xp/2003:           wxp
  2000:              w2000

Other:
  Solaris:           solaris
  Other:             other
```

#### 文件处理
- 使用分片上传处理大文件
- 支持断点续传
- 实时显示进度
- 支持多种虚拟机磁盘格式转换

## License

MIT

