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
import os

site = {
    'host': 'www.gushiwen.org',
    'url': '/gushi/quansong.aspx',
    'prefix': 'result',
    'authors': 'authors.txt',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    # 'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Langugae': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Connection': 'keep-alive',
    'Host': site['host'],
    'User-Agent': "Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36",
}

def get_authors():
    conn = http.client.HTTPConnection(site['host'])
    conn.request(method = 'GET', url = site['url'], headers = headers)
    response_data = str(conn.getresponse().read(), encoding='utf-8')
    url_pattern = re.compile(r'<a\shref="(?P<url>/wen_[0-9]{4}.aspx)"\starget="_blank">'
                             '(?P<name>[\u4e00-\u9fa5]+)</a>')
    with open('%s/%s'%(site['prefix'],site['authors']), 'w', encoding='utf-8') as fp:
        for link, author in re.findall(url_pattern, response_data):
            fp.write('%s\t%s\n'%(link, author))

def get_text(conn, url, author):

    class Parser(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.pattern = re.compile(r'[\u4e00-\u9fa5]+')
            self.handle = False
            self.cnt = 0
            self.data = []
        def handle_starttag(self, tag, attrs):
            if tag == 'div' and dict(attrs).get('class') == 'authorShow':
                self.handle = True
            if self.handle == True and tag == 'div':
                self.cnt += 1
        def handle_endtag(self, tag):
            if self.handle == True and tag == 'div':
                self.cnt -= 1
            if self.cnt == 0:
                self.handle = False
        def handle_data(self, data):
            if self.handle == True and self.cnt == 1 and re.match(self.pattern, data) != None:
                self.data.append(data)
    conn.request(method = 'GET', url = url, headers = headers)
    response_data = str(conn.getresponse().read(), encoding='utf-8')
    hp = Parser()
    hp.feed(response_data)
    hp.close
    return '\n'.join(hp.data)

if __name__ == '__main__':

    print('begin getting authors list ...')
    get_authors()
    authors = {}
    with open('%s/%s'%(site['prefix'],site['authors']),'r', encoding='utf-8') as fp:
        for line in fp:
            if len(line) > 0:
                link, author = line[:-1].split('\t')
                authors[author] = link
    print('finish getting authors list')

    conn = http.client.HTTPConnection(site['host'])
    for author, link in authors.items():
        dirname = '%s/%s'%(site['prefix'], author)
        try:
            os.mkdir(dirname)
        except:
            print('dir %s already exists!'%(dirname))
        with open('%s/%s/%s.txt'%(site['prefix'], author, author), 'w', encoding='utf-8') as fp:
            fp.write(get_text(conn, link, author))
    
    print('finish all works')
