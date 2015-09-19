#! /usr/bin/env python
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
    
    category = ['cpp']

    start_urls = ['http://www.cnblogs.com/cate/%s/%d' % (category[0], p) for p in range(1, 31)]

    def parse(self, response):
        if response.status != 200:
            yield Request(response.url)
        else:
            article_links = Selector(response).xpath('//div[@class="post_item_body"]/h3/a/@href').extract()
            with open('root/cnblogs.%s.content'%(self.category[0]), 'ab') as fp:
                fp.write('\n'.join(article_links + ['']))

