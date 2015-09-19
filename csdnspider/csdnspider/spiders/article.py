#! /usr/bin/env python
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

    html_start_l = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>
'''
    html_start_r = '''
</title>
    <link type="text/css" rel="stylesheet" href="/static.blog.csdn.net/scripts/SyntaxHighlighter/styles/default.css" />
    <!--<link type="text/css" rel="stylesheet" href="/static.blog.csdn.net/skin/default/css/style.css" />
    <link type="text/css" rel="stylesheet" href="/static.csdn.net/public/common/toolbar/css/index.css" />-->
</head>
<body>
'''
    html_end = '''
</body>
</html>
'''

    start_urls = []
    with open('root/csdn.cpp.content', 'r') as fp:
        start_urls = fp.read().split('\n')[0:-1]

    def parse(self, response):
        dirname = os.sep.join(['root'] + response.url.split('/')[2:-1])
        filename = os.sep.join([dirname, response.url.split('/')[-1] + '.html'])
        # parse artitle text.
        article_text = Selector(response).xpath('//div[@id="article_details"]').extract()[0]

        parser = Selector(text = article_text)

        # parse artile title.
        article_title = parser.xpath('//span[@class="link_title"]/a/text()').extract()[0]
        article_links = parser.xpath('//a[re:test(@href, "[^/]+/article/details/\d+")]/@href').extract()

        # replace links.
        article_text = article_text.replace('http://static.blog.csdn.net/css/blog_detail.css', '/static.blog.csdn.net/css/blog_detail.css')
        for link in article_links:
            article_text = article_text.replace(link, '/blog.csdn.net' + link + '.html')

        item = ArticleItem()
        item['image_urls'] = [x for x in parser.xpath('//img/@src').extract()]
        # handle such image(with watermark) url: 
        #    http://img.blog.csdn.net/20140917165912117?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvaWFpdGk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast
        item['image_names'] = [(lambda k: k if '?' not in k else k.split('?')[0]+'.png')(x).split('/')[-1] for x in item['image_urls']]

        # process image links.
        for url in item['image_urls']:
            article_text = article_text.replace(url, (lambda k: k if '?' not in k else k.split('?')[0]+'.png')(url)[6:])

        if not os.path.exists(dirname):
            os.makedirs(dirname)
        with open(filename, 'wb') as fp:
            fp.write(self.html_start_l + article_title.encode('utf-8') + self.html_start_r  + article_text.encode('utf-8', 'ignore') + self.html_end)

        return item
