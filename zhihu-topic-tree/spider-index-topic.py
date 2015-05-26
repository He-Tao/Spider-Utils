#! /usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'He Tao'

'''
Zhihu Spider.

获取知乎首页 www.zhihu.com 上的所有话题以及其链接。
'''

import re
from http.client import HTTPConnection
from html.parser import HTMLParser

spider = {
    ## config.
    'host': 'www.zhihu.com',
    'topic': {
        'online': '/',
        'offline': 'www.zhihu.com.2015-05-25.html',
    },
    'pattern': 'http://www.zhihu.com/topic/\d{8}/questions',
}

def get_topic(use_offline):
    class TopicParser(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.pattern = re.compile(spider['pattern'])
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
    topics = get_topic(use_offline = True) # if use offline resource.
    print('topics size in index page: %d'%(len(topics)))
    with open('index-topics.txt', 'w', encoding = 'utf-8') as fp:
        for t, l in sorted(topics.items(), key = lambda x: x[1]):
            fp.write('%s\t%s\n'%(l, t))
    print('all topics in index page have been stored in index-topics.txt')

