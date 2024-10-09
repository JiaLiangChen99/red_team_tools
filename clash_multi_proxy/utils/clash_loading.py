import uuid
import os

from utils.config import USING_CLASH_CONF_PATH, TEMPLATE_CLASH_CONF_PATH, CACHE_PATH
from utils.system import find_all_free_ports
from utils.db import clash_proxies, Proxy

import yaml

with open(USING_CLASH_CONF_PATH, 'r', encoding='utf-8') as f:
    using_conf = yaml.load(f, Loader=yaml.FullLoader)

with open(TEMPLATE_CLASH_CONF_PATH, 'r', encoding='utf-8') as f:
    tem_conf = yaml.load(f, Loader=yaml.FullLoader)


def save_clash_conf(yaml_conf: dict):
    filename = uuid.uuid4().hex + '.yaml'
    clash_conf_path = os.path.join(CACHE_PATH, filename)
    with open(clash_conf_path, 'w', encoding='utf-8') as f:
        yaml.dump(yaml_conf, f, allow_unicode=True)
    return clash_conf_path


def create_clash_conf(proxies: dict, clash_template_conf: dict, free_port: int) -> dict:
    new_clash_conf = clash_template_conf.copy()
    proxies_name = proxies['name']
    new_clash_conf['mixed-port'] = free_port
    new_clash_conf['proxy-groups'][0]['proxies'] = [proxies_name]
    new_clash_conf["proxies"] = [proxies]
    return new_clash_conf



def load_clash_conf() -> list[Proxy]:
    free_ports = find_all_free_ports(get_ports_num=len(using_conf['proxies']))
    for index, proxy in enumerate(using_conf['proxies']):
        proxies_name = proxy['name']
        new_clash_conf = create_clash_conf(proxy, tem_conf, free_ports[index])
        clash_conf_path = save_clash_conf(new_clash_conf)
        clash_proxies.append(Proxy(port=free_ports[index], clash_conf_path=clash_conf_path, server_name=proxies_name))
    return clash_proxies

