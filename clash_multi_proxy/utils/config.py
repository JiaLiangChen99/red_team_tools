import os
import platform


def setting_clash_core():
    if platform.system() == 'Windows':
        return os.path.join(SETTING_PATH, 'clash-windows-x86.exe')
    else:
        return os.path.join(SETTING_PATH, 'clash-linux-arm64')
    

USING_CLASH_CONF = '1728142073051.yml'
PROJECT_PATH = os.getcwd()
CACHE_PATH = os.path.join(PROJECT_PATH, 'cache')
SETTING_PATH = os.path.join(PROJECT_PATH,'setting')
CLASH_CORE_PATH = setting_clash_core()
USING_CLASH_CONF_PATH = os.path.join(SETTING_PATH, USING_CLASH_CONF)
TEMPLATE_CLASH_CONF_PATH = os.path.join(SETTING_PATH, 'template.yml')