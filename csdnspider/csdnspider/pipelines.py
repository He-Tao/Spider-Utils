# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import scrapy

from scrapy.selector import Selector
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

class CSDNImagesPipeline(ImagesPipeline):

    def file_path(self, request, response = None, info = None):
        # handle such image(with watermark) url: 
        #    http://img.blog.csdn.net/20140917165912117?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvaWFpdGk=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast
        return os.sep.join((lambda x: x if '?' not in x else x.split('?')[0]+'.png')(request.url)[7:].split('/'))

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        if not [x['url'] for ok, x in results if ok]:
            raise DropItem("Item contains no images")
        return item
