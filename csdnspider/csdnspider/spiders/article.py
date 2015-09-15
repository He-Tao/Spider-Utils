#! /usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'He Tao'

'''
CSDN blog spider
================

article.py
----------

Get the text of article and it's picture.

'''

import os

import scrapy
from scrapy.selector import Selector

from csdnspider.items import ArticleItem

class ArticleSpider(scrapy.Spider):

    name = 'article'  # csdn article spider
    allowed_domains = ["blog.csdn.net"]

    html_start = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">'
    <title></title>
</head>
<body>
'''
    html_end = '''
</body>
</html>
'''

    start_urls = []
    with open('root/cpp.content', 'r') as fp:
        start_urls = fp.read().split('\n')[:-1]

    def parse(self, response):
        dirname = os.sep.join(['root'] + response.url.split('/')[2:-1])
        filename = os.sep.join([dirname, response.url.split('/')[-1] + '.html'])
        article_text = Selector(response).xpath('//div[@id="article_details"]').extract()[0]
        
        article_text = article_text.replace('http://static.blog.csdn.net/css/blog_detail.css', '/static.blog.csdn.net/css/blog_detail.css')

        item = ArticleItem()
        item['image_urls'] = [x for x in Selector(text = article_text).xpath('//img/@src').extract()]
        item['image_names'] = [x.split('/')[-1] for x in item['image_urls']]

        # process image links.
        for url in item['image_urls']:
            article_text = article_text.replace(url, url[6:])

        if not os.path.exists(dirname):
            os.makedirs(dirname)
        with open(filename, 'wb') as fp:
            fp.write(self.html_start + article_text.encode('utf-8', 'ignore') + self.html_end)

        return item
