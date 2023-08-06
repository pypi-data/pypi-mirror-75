# -*- coding:utf-8 -*-
import sys
import json, copy, time, os
from urllib import parse

from wqrfproxy import *
# 此文档务必用PY3来书写
def request(flow):
    try:
        content = parse.unquote(flow.request.text)
    except:
        print('error')
        content = ''
    url = flow.request.url.split('?')[0]
    try:
        params = flow.request.url.split('?')[1]
    except:
        params = ''
    content += params
    catch_api(url,content)
