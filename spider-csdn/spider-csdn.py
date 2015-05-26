#! /usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'He Tao'

'''
CSDN blog spider.
'''

import gzip
import json
import re
from http.client import HTTPConnection
from html.parser import HTMLParser

## http://www.zhihu.com/topic/19776749

spider = {
    ## config.
    'user': {
        'email': 'buaahetao@163.com',
        'password': '299792458',
    },
    'headers': {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        ## my cookie.
        'Cookie': 'uuid_tt_dd=7650435221304658604_20141228; __gads=ID=7982685e35023a81:T=1419820464:S=ALNI_MbWeVaemEUmni0afzOVIsJJHVgkIw; CloudGuest=38F6kt7d7rIRQXKulZsiYmuOvox0QEeJYhgnV2o2veuLAEGtOkPVuZDULFLDpIGmmDIVA50n0wiI+TbGMkJMZwcuFd8tQvu8dmSJE2V53nOBMF2CHXhmq+T7n+/7IIAcDqybD/lyBSYMs14xB12RbT7/waSk2Z5LUcbRjBYwR6/gj/l8uGjeo+jmL9r1ZXLU; _JQCMT_ifcookie=1; _JQCMT_browser=dc5c07adc0fab2b526866bddcb7cae86; bdshare_firstime=1431702442644; lzstat_uv=3916385736429315443|2955225@3547632@3475730@2819552@2737459@2671462@2754945@2673176; UserName=u012288867; UserInfo=UWu7ppOxhFUsNdb%2F5Ial9%2FOW5sS7r%2BzYbdCJF7szd%2BFitOnxWCFWJNEs%2F%2F%2F60MQcLB4q1hzcyEzzwXfqFfm9i4P2lZ80P3gRNj%2BwEkMlpMQ6MrwIV%2BuyncLkoA9OoOsx%2FfaGGHPWsupjRPXD8J7pkQ%3D%3D; UserNick=bhht; AU=DC5; UN=u012288867; UE="buaahetao@163.com"; access-token=964f8fce-12ee-4671-9947-6f0b1dfd1c3c; __utma=17226283.2015908350.1431389080.1432651074.1432659188.77; __utmb=17226283.8.10.1432659188; __utmc=17226283; __utmz=17226283.1432659188.77.68.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; dc_tos=noyvcj; dc_session_id=1432659663636'
    },
    'follow': {
        'host': 'my.csdn.net',
        'index': '/my/follow',
    },
    'blog': {
        'host': 'blog.csdn.net',
        'path': '/article/list/',
    }
}

def get_follow():
    ''' get my follower's list. need cookie in headers.'''
    class CountParser(HTMLParser):
        ## <a href="/my/follow" class="on">我的关注（150）</a>
        def __init__(self):
            HTMLParser.__init__(self)
            self.count = -1
        def handle_starttag(self, tag, attrs):
            if tag == 'a' and dict(attrs).get('href') == '/my/follow' and dict(attrs).get('class') == 'on':
                self.count = 0
        def handle_data(self, data):
            if self.count == 0:
                self.count = int(re.search(r'\d+', data).group(0))

    class FollowParser(HTMLParser):
        ## <a href="/yuanlin2008" target="_blank" id="li_username_8807257" title="yuanlin2008" class="user_name">yuanlin2008</a>
        def __init__(self):
            HTMLParser.__init__(self)
            self.flag = 0
            self.follows = []
        def handle_starttag(self, tag, attrs):
            if tag == 'div':
                if dict(attrs).get('class') == 'list row':
                    self.flag += 1
                elif self.flag > 0:
                    self.flag += 1
            if self.flag > 0 and tag == 'a' and dict(attrs).get('class') == 'user_name':
                self.follows.append(dict(attrs).get('title'))
        def handle_endtag(self, tag):
            if self.flag > 0 and tag == 'div':
                self.flag -= 1

    conn = HTTPConnection(spider['follow']['host'])
    conn.request('GET', spider['follow']['index'], headers = spider['headers'])
    text = gzip.decompress(conn.getresponse().read()).decode('utf-8')
    hp = CountParser()
    hp.feed(text)
    hp.close()
    count, follows = hp.count, []
    for i in range(1, count//20+2):
        conn.request('GET', spider['follow']['index']+'/%d'%(i), headers = spider['headers'])
        text = gzip.decompress(conn.getresponse().read()).decode('utf-8')
        hp = FollowParser()
        hp.feed(text)
        hp.close()
        follows += hp.follows
    return follows

def get_contents(user):
    '''
    得到目录的方法：首先，根据首页的信息可以知道目录一共有多少页，然后构造页数
    大于实际页数的URL，便可以直接得到所有博客的目录列表，省去了很多麻烦。
    此处直接取一个较大的值，比如 100000
    don't need cookie in headers.
    '''
    class ContentsParser(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.contents = {}
            self.flag = False
            self.link = ''
        def handle_starttag(self, tag, attrs):
            if tag == 'span' and dict(attrs).get('class') == 'link_title':
                self.flag = True
            if self.flag and tag == 'a':
                self.link = dict(attrs).get('href')
        def handle_endtag(self, tag):
            self.flag = False
        def handle_data(self, data):
            if self.flag:
                self.contents[self.link] = data.strip()

    conn = HTTPConnection(spider['blog']['host'])
    conn.request('GET', '/'+user+spider['blog']['path']+'10000', headers = spider['headers'])
    text = gzip.decompress(conn.getresponse().read()).decode('utf-8')
    hp = ContentsParser()
    hp.feed(text)
    hp.close()
    return hp.contents
    
if __name__ == '__main__':
##    follows = get_follow()
##    with open('follows.txt', 'w', encoding = 'utf-8') as fp:
##        for name in follows:
##            fp.write('%s\n'%name)
##    print('finish get follower\'s list.')

##    contents = get_contents('acm_cxlove')
##    with open('acm_cxlove.txt', 'w', encoding = 'utf-8') as fp:
##        for k, v in contents.items():
##            fp.write('%s\t%s\n'%(k, v))
##    print('finish get contents.')

