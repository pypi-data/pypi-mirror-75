# -*- coding:utf-8 -*-
import os,platform,subprocess,threading,time,socket,json
import mitmproxy

# 启动mitmproxy服务
def start_wqrfproxy(port='8000',client_certs=''):
    # 判断系统
    if 'arwin' in platform.system() or 'inux' in platform.system():
        now_path = os.getcwd()
        if client_certs=='':
            cmd='mitmweb -p %s -s %s/mitm_catch.py >mitm_log.txt'%(port,now_path)
        else:
            cmd='mitmweb -p %s -s %s/mitm_catch.py --set client_certs=%s >mitm_log.txt'%(port,now_path,client_certs)
    else: #windows
        if client_certs == '':
            cmd = ''
        else:
            cmd = ''
    subprocess.Popen(cmd, shell=True)
    print(u"*** 抓包断言服务已启动！mitmserver has been started! ***")
    with open('log.txt','w') as fp:
        fp.write('{}')
    with open('mitm_log.txt','w') as fp:
        fp.write('')
    print(u"*** 请把你的设备http代理设置成 %s:%s please configure your device's Http proxy on %s:%s ***" % (get_ip(), port,get_ip(), port))
    print(u"*** 你可以用 assert_proxy(目标url,预期字符串) 方法来断言设备发出的请求 you can use assert_proxy(your url,your reuqest content) to assert the http ***")
    print(u"*** url必须是http(s)://xxxxx.... 这样，并且只能填入 '?' 之前的部分 the url must like http(s)://xxxxx.... which piece befor '?' ***")
    print(u"*** 这个预期字符串将会在url参数部分和请求体中进行查找 the request content will be found in url's params and request's body ***")
    print(u"*** 你最好在你的脚本结尾写上 stop_wqrfproxy() 函数用来关闭服务 you'd better write stop_wqrfproxy() in your script's end to close the server ***")
    print('*** -------------------------------------------------------------------- ***')
    time.sleep(3)

#  获取服务器ip：
def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


# 杀掉mitmproxy服务
def stop_wqrfproxy():
    # 判断系统
    if 'arwin' in platform.system() or 'inux' in platform.system():
        subprocess.call("ps -ef | grep mitm | grep -v grep | awk '{print $2}' | xargs kill -9",shell=True)
    else:  # windows
        ...
    print(u"*** 抓包断言服务已停止！mitmserver has been stoped! ***")

# 存放抓包数据
def catch_api(url,request_body):
    with open('log.txt','r') as fp:
        requests_log = json.loads(fp.readlines()[0])

    with open('log.txt','w') as fp:
        try:
            requests_log[url].append(request_body)
        except:
            requests_log[url] = [request_body]
        fp.write(json.dumps(requests_log))

# 断言监控语句
def assert_proxy(url='',content=''):
    with open('log.txt','r') as fp:
        requests_log = json.loads(fp.readlines()[0])
    with open('log.txt','w') as fp:
        try:
            tmp = requests_log[url]
            for i in requests_log[url]:
                if content in i:
                    requests_log[url].remove(i)
                    print(u"*** 成功找到url和其中的预期字符串！ Successfully found the url and the request body! ***")
                    if requests_log[url] == []:
                        del requests_log[url]
                    fp.write(json.dumps(requests_log))
                    break
            else:
                fp.write(json.dumps(requests_log))
                raise AssertionError(u"*** 只找到url但未发现预期字符串！ It has been found the url,but can't find the reuqest body! ***")
        except KeyError as e:
            fp.write(json.dumps(requests_log))
            raise AssertionError(u"*** 未找到url！ Can't find the url you set! ***")
