# -*- coding:utf-8 -*-
import os,platform,subprocess,threading,time
import mitmproxy

# 启动mitmproxy服务
def start_wqrfproxy(port='8000',client_certs=''):
    # 判断系统
    if 'arwin' in platform.system() or 'inux' in platform.system():
        if client_certs=='':
            cmd='mitmweb -p %s'%port
        else:
            cmd='mitmweb -p %s  --set client_certs=%s'%(port,client_certs)
    else: #windows
        if client_certs == '':
            cmd = ''
        else:
            cmd = ''
    subprocess.Popen(cmd, shell=True)
    time.sleep(5)


# 杀掉mitmproxy服务
def stop_wqrfproxy():
    # 判断系统
    if 'arwin' in platform.system() or 'inux' in platform.system():
        ...
    else:  # windows
        ...
