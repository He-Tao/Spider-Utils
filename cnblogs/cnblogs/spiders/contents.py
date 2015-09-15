#! /usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'He Tao'

'''
CNBLOGS blog spider
===================

contents.py
----------

Get the contents of specified category.

'''

import os
import json

import scrapy
from scrapy.selector import Selector

class ContentsSpider(scrapy.Spider):

    name = 'contents'  # csdn article spider
    allowed_domains = ["www.cnblogs.com"]
    
    category = 'cpp'

    start_urls = ['http://www.cnblogs.com/cate/%s/%d' % (category, p) for p in range(1, 31)]

    def parse(self, response):
        article_links = Selector(response).xpath('//div[@class="post_item_body"]/h3/a/@href').extract()
        with open('root/%s.content'%(self.category), 'ab') as fp:
            fp.write('\n'.join(article_links + ['']))

