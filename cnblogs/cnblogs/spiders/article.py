#! /usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'He Tao'

'''
CNBLOGS blog spider
================

article.py
----------

Get the text of article and it's picture.

'''

import os

import scrapy
from scrapy.selector import Selector

from cnblogs.items import ArticleItem

class ArticleSpider(scrapy.Spider):

    name = 'article'  # csdn article spider
    allowed_domains = ["www.cnblogs.com"]

    html_start_l = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>
'''
    html_start_r = '''
</title>
</head>
<body>
'''
    html_end = '''
</body>
</html>
'''

    start_urls = []
    with open('root/cnblogs.cpp.content', 'r') as fp:
        start_urls = fp.read().split('\n')[:-1]

    def parse(self, response):
        dirname = os.sep.join(['root'] + response.url.split('/')[2:-1])
        filename = os.sep.join([dirname, response.url.split('/')[-1]])
        article_text = Selector(response).xpath('//div[@class="post"]').extract()[0]

        parser = Selector(text = article_text)

        article_title = parser.xpath('//a[@id="cb_post_title_url"]/text()').extract()[0]
        title_link = parser.xpath('//a[@id="cb_post_title_url"]/@href').extract()[0]

        article_text = article_text.replace(title_link, title_link[6:])

        item = ArticleItem()
        item['image_urls'] = [x for x in parser.xpath('//img/@src').extract()]
        item['image_names'] = [x.split('/')[-1] for x in item['image_urls']]

        # process image links.
        for url in item['image_urls']:
            article_text = article_text.replace(url, url[6:])

        if not os.path.exists(dirname):
            os.makedirs(dirname)
        with open(filename, 'wb') as fp:
            fp.write(self.html_start_l + article_title.encode('utf-8') + self.html_start_r + article_text.encode('utf-8', 'ignore') + self.html_end)

        return item
