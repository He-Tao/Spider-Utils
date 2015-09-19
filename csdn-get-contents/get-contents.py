#! /usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'He Tao'

'''
CSDN blog spider
================

get-contents.py
---------------

Get the blog contents of a specified user.

'''

import gzip
import json
import re
import os
from http.client import HTTPConnection
from html.parser import HTMLParser

## http://www.zhihu.com/topic/19776749

spider = {
    ## config.
    'headers': {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    },
    'blog': {
        'host': 'blog.csdn.net',
        'path': '/article/list/',
    }
}

def get_contents(user):
    '''
    得到目录的方法：首先，根据首页的信息可以知道目录一共有多少页，然后构造页数
    大于实际页数的URL，便可以直接得到所有博客的目录列表，省去了很多麻烦。
    此处直接取一个较大的值，比如 100000.

    DO NOT need the cookie in headers.
    '''
    class ContentsParser(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.contents = {}
            self.flag = 0
            self.link = ''
        def handle_starttag(self, tag, attrs):
            if tag == 'span' and dict(attrs).get('class') == 'link_title':
                self.flag = 1
            if self.flag > 0:
                self.flag += 1
                if tag == 'a':
                    self.link = dict(attrs).get('href')
        def handle_endtag(self, tag):
            self.flag -= 1
        def handle_data(self, data):
            if self.flag == 3:
                self.contents[self.link] = data.strip()

    conn = HTTPConnection(spider['blog']['host'])
    conn.request('GET', '/'+user+spider['blog']['path']+'10000', headers = spider['headers'])
    text = gzip.decompress(conn.getresponse().read()).decode('utf-8')
    hp = ContentsParser()
    hp.feed(text)
    hp.close()
    return hp.contents

if __name__ == '__main__':
    user_name = 'abcjennifer'
    contents = get_contents(user_name)


