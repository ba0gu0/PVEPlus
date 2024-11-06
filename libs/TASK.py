#!coding=utf-8
import json
import os.path
import re
import threading
import time
import subprocess


# 定义导出任务
class ExportTask(threading.Thread):
    def __init__(self, vm_disk_value, diskinfo, diskinfo_file_path):
        super().__init__()
        self.vm_disk_value = vm_disk_value
        self.diskinfo = diskinfo
        self.diskinfo_file_path = diskinfo_file_path
        self._progress = 0
        self._start_time = time.time()
        self.stop_event = threading.Event()

    def run(self):
        # 模拟导出资源的过程

        cmd = ['pvesm', 'path', self.vm_disk_value]
        convert_input_path = subprocess.check_output(cmd, shell=False, stderr=subprocess.STDOUT).decode('utf-8').strip()

        convert_out_path = os.path.abspath(os.path.join(os.path.dirname(self.diskinfo_file_path), self.diskinfo['uuid']))
        cmd = ['qemu-img', 'convert', '-p', '-c', '-O', self.diskinfo['type'], convert_input_path, convert_out_path]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

        progress_regex = re.compile(r'\((.*?)/100%\)')

        while not self.stop_event.is_set() and process.poll() is None:
            output = process.stdout.readline()
            progress_match = progress_regex.search(output)
            if progress_match:
                progress = float(progress_match.group(1))
                # print(f'导出进度: {progress}')
                self._progress = progress

        process.wait()

        with open(self.diskinfo_file_path, 'r') as file:
            files = json.load(file)
        files.append(self.diskinfo)
        with open(self.diskinfo_file_path, 'w') as file:
            json.dump(files, file)

    def stop(self):
        # 停止任务
        self.stop_event.set()

    def get_progress(self):
        return self._progress

    def get_start_time(self):
        return self._start_time


# 定义导入任务
class ImportTask(threading.Thread):
    def __init__(self, vm_id, import_disk_file_path, storage_id):
        super().__init__()
        self.vm_id = vm_id
        self.import_disk_file_path = import_disk_file_path
        self.storage_id = storage_id
        self._progress = 0
        self._start_time = time.time()
        self.stop_event = threading.Event()

    def run(self):
        cmd = ['qm', 'disk', 'import', str(self.vm_id), os.path.abspath(self.import_disk_file_path), self.storage_id]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

        # progress_regex = re.compile(r'\((.*?)%\)')

        while not self.stop_event.is_set() and process.poll() is None:
            output = process.stdout.readline()

            if 'created' in output:
                self._progress = 10

            if 'Successfully' in output:
                self._progress = 100
            # print(f'导出进度: {self._progress}')
            # progress_match = progress_regex.search(output)
            # if progress_match:
            #     progress = float(progress_match.group(1))
            #     # print(f'导出进度: {progress}')
            #     self.progress = progress

        process.wait()

        return process.returncode

    def stop(self):
        # 停止任务
        self.stop_event.set()

    def get_progress(self):
        return self._progress

    def get_start_time(self):
        return self._start_time
