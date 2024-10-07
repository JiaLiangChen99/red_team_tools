import socket
import os
import subprocess

from utils.config import CLASH_CORE_PATH

import psutil

def find_all_free_ports(start_port=22000, end_port=23000, timeout=0.05, get_ports_num=200):
    free_ports = []
    for port in range(start_port, end_port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)  # 设置超时时间
            if s.connect_ex(('localhost', port)) != 0:  # 端口未被占用
                free_ports.append(port)
            if len(free_ports) > get_ports_num:
                break
    return free_ports


def open_the_clash(con_path) -> int:
    """返回clash的进程号"""
    process = subprocess.Popen([CLASH_CORE_PATH, "-f", con_path])
    pid = process.pid
    return pid

def kill_pid_process(pid: list[int] | int):
    """杀死进程"""
    if isinstance(pid, int):
        process = psutil.Process(pid)
        process.kill()
    else:
        for p in pid:
            process = psutil.Process(p)
            process.kill()

