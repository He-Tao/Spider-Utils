#! /usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'He Tao'

'''
This script is used to fetch the picture of bing's mainpage.

Author: He Tao, hetao@mail.com

Date: December 13, 2014
'''

import http.client
import re
from datetime import date

def get_bing_pic():
    conn = http.client.HTTPConnection('cn.bing.com')
    conn.request(method = 'GET', url = '/')
    mainpage = str(conn.getresponse().read())
    pattern = re.compile(r's.cn.bing.net/az/hprichbg/rb/\S*.jpg')
    image_url = re.search(pattern, mainpage).group(0)
    image_path = image_url[29:image_url.__len__()]
    conn = http.client.HTTPConnection(image_url[0:13])
    print('start fetching %s ...' %(image_url))
    conn.request(method = 'GET', url = '/az/hprichbg/rb/%s' %(image_path))
    img = open('bing\\%s-%s' %(date.today().__str__(), image_path), 'w')
    img.close()
    with open('bing\\%s-%s' %(date.today().__str__(), image_path), 'wb') as img:
        img.write(conn.getresponse().read())
    print('saving picture to %s ...' % ('bing\\%s-%s' %(date.today().__str__(), image_path)))
    print('fetch successfully !')

if __name__ == '__main__':
    get_bing_pic()
