#! coding=utf-8
import re

from urllib3 import disable_warnings
from proxmoxer import ProxmoxAPI

disable_warnings()

class Proxmox:
    proxy = None

    def __init__(self, username, password, host='127.0.0.1', backend='https', port=8006, verify_ssl=False):
        super().__init__()
        self.proxy = ProxmoxAPI(
            backend=backend,
            user=username,
            password=password,
            host=host,
            port=port,
            verify_ssl=verify_ssl
        )

    def check_auth(self):
        if not self.proxy:
            return False
        try:
            user = self.proxy.access.users.get()
            return True
        except Exception as e:
            return False

    def get_nodes(self):
        return self.proxy.nodes.get() if self.proxy else False

    def get_pools(self):
        return self.proxy.pools.get() if self.proxy else False

    def get_storages(self):
        if not self.proxy:
            return False
        storages = self.proxy.storage.get()
        _ = []
        for storage in storages:
            if 'images' in storage['content']:
                _.append(storage)
        return _

    def get_vms(self):
        if not self.proxy:
            return False
        vms = self.proxy.cluster.resources.get()
        _ = []
        for vm in vms:
            if vm['type'] == 'qemu':
                _.append(vm)
        return _

    def get_vm_disks(self, vm_id, node):
        # return list(filter(lambda __: any(
        #     re.search(_, __['key']) and 'media=cdrom' not in __['value'] for _ in
        #     [r'ide\d+', r'sata\d+', r'scsi\d+', r'virtio\d+']),
        #                    self.proxy.nodes(node).qemu(vm_id).pending.get())) if self.proxy else False
        return list(filter(lambda __: any(
            re.search(_, __['key']) for _ in
            [r'ide\d+', r'sata\d+', r'scsi\d+', r'virtio\d+']),
                           self.proxy.nodes(node).qemu(vm_id).pending.get())) if self.proxy else False
        # return self.proxy.get(f'/api2/json/nodes/{node}/qemu/{vmid}/config') if self.proxy else False

    def get_vm_disks_unused(self, vm_id, node):
        return list(filter(lambda _: re.search(r'unused\d+', _['key']), self.proxy.nodes(node).qemu(vm_id).pending.get())) if self.proxy else False
        # return self.proxy.nodes(node).qemu(vmid).pending.get() if self.proxy else False

    def get_vm_boot(self, vm_id, node):
        return list(filter(lambda _: _['key'] == 'boot', self.proxy.nodes(node).qemu(vm_id).pending.get()))[0]['value'] if self.proxy else False

    def get_nextid(self):
        return self.proxy.cluster.nextid.get() if self.proxy else False

    def create_vms(self, node, data):
        # print(f'/api2/extjs/nodes/{node}/qemu', data)
        return self.proxy.post(f'/api2/extjs/nodes/{node}/qemu', **data) if self.proxy else False

    def mount_vm_disk(self, vm_id, node, data):
        # print(f'/api2/extjs/nodes/{node}/qemu/{vm_id}/config', data)
        return self.proxy.post(f'/api2/extjs/nodes/{node}/qemu/{vm_id}/config', **data) if self.proxy else False

    def set_vm_boot_order(self, vm_id, node, data):
        return self.proxy.post(f'/api2/extjs/nodes/{node}/qemu/{vm_id}/config', **data) if self.proxy else False
