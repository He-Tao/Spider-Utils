#! /usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'He Tao'

'''
CSDN blog spider
================

contents.py
----------

Get the contents of specified tag.

'''

import os
import json

import scrapy
from scrapy.selector import Selector

class ContentsSpider(scrapy.Spider):

    name = 'contents'  # csdn article spider
    allowed_domains = ["blog.csdn.net"]
    
    tag = 'cpp'

    start_urls = ['http://blog.csdn.net/tag/details.html?tag=%s&page=%d' % (tag, p) for p in range(1, 31)]

    def parse(self, response):
        print(response.url)
        links_data = Selector(response).xpath('//script[contains(., "var data = ")]/text()').extract()[0]
        l, r = links_data.find('{'), links_data.rfind('}')
        article_links = [item['url'] for item in json.loads(links_data[l:(r+1)].encode('utf-8', 'ignore'))['result']]
        with open('root/%s.content'%(self.tag), 'ab') as fp:
            fp.write('\n'.join(article_links + ['']))

