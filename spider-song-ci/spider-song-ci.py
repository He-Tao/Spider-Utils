#! /usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'He Tao'

'''
This script is used to fetch all Song Ci from http://www.gushiwen.org/gushi/quansong.aspx

Author: He Tao, hetao@mail.com

Date: 2015-05-11
'''

import http.client
import re
from html.parser import HTMLParser

site = {
    'host': 'www.gushiwen.org',
    'url': '/gushi/quansong.aspx',
}

def get_authors():
    conn = http.client.HTTPConnection(site['host'])
    conn.request(method = 'GET', url = site['url'])
    response_data = str(conn.getresponse().read(), encoding='utf-8')
    url_pattern = re.compile(r'<a\shref="(?P<url>/wen_[0-9]{4}.aspx)"\starget="_blank">(?P<name>[\u4e00-\u9fa5]+)</a>')
    return re.findall(url_pattern, response_data)

def get_text(url):
    pass

if __name__ == '__main__':
    result = {}
    for url, name in get_authors():
        result[name] = get_text(url)
