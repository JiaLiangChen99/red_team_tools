from multiprocessing import Process
import random
import os
import sys
sys.path.append(os.getcwd())

from utils.clash_loading import load_clash_conf
from utils.system import open_the_clash, kill_pid_process
from utils.config import CACHE_PATH

import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

# 记录所有进程的 PID
pids = []
global_proxies = None

def start_proxies():
    clean_cache()
    global pids, global_proxies
    global_proxies = load_clash_conf()
    for proxy in global_proxies:
        """ open_the_clash 是一个后台任务，他会后台运行一个 clash 程序，"""
        clash_conf = proxy.clash_conf_path
        p = Process(target=open_the_clash, args=(clash_conf,))
        p.start()
        pids.append(p)


def clean_cache():
    for filename in os.listdir(CACHE_PATH):
        os.remove(os.path.join(CACHE_PATH, filename))

app = FastAPI()

@app.on_event("startup")
def startup_event():
    start_proxies()

@app.get('/proxy')
def get_proxy():
    result = random.choice(global_proxies)
    return {'proxy_name': result.server_name, 'proxy': {'http': f'http://127.0.0.1:{result.port}', 'https': f'http://127.0.0.1:{result.port}'}}

@app.get("/")
def read_root():
    # 跳转到文档页面
    return RedirectResponse(url="/docs")

@app.on_event("shutdown")
def shutdown_event():
    for p in pids:
        p.terminate()  # 终止每个进程
        p.join()  # 等待进程结束
    print("所有clash进程已终止")
    clean_cache()

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
