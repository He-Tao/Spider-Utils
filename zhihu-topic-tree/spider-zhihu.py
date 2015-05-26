#! /usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'He Tao'

'''
Zhihu Spider.
'''

import gzip
import json
import re
from http.client import HTTPConnection
from html.parser import HTMLParser

## http://www.zhihu.com/topic/19776749

spider = {
    ## config.
    'host': 'www.zhihu.com',
    'user': {
        'email': 'buaahetao@sina.com',
        'password': 'buaa299792458',
    },
    'headers': {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    },
    'topic': {
        'online': '/',
        'offline': 'www.zhihu.com.2015-05-25.html',
    },
}

def login(email, password):
    pass

def get_topic(use_offline):
    class TopicParser(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.pattern = re.compile('http://www.zhihu.com/topic/\d{8}/questions')
            self.links = {}
            self.href = None
        def handle_starttag(self, tag, attrs):
            attrs = dict(attrs)
            if (tag == 'a' and attrs.get('href') and
                    re.match(self.pattern, attrs.get('href'))):
                self.href = attrs.get('href')
        def handle_data(self, data):
            if self.href != None:
                self.links[data] = self.href
                self.href = None
    text = None
    if use_offline:
        with open(spider['topic']['offline'], 'r', encoding = 'utf-8') as fp:
            text = fp.read()
    else:
        conn = HTTPConnection(spider['host'])
        conn.request('GET', spider['topic']['online'])
        text = conn.getresponse().read().decode('utf-8')
    hp = TopicParser()
    hp.feed(text)
    hp.close()
    return hp.links

if __name__ == '__main__':
    # login(config['user']['email'], config['user']['password'])
    topics = get_topic(use_offline = True)
    with open('topics.txt', 'w', encoding = 'utf-8') as fp:
        for t, l in sorted(topics.items(), key = lambda x: x[1]):
            fp.write('%s\t%s\n'%(l, t))

