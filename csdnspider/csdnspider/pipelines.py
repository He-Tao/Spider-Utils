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
        return os.sep.join(request.url[7:].split('/'))

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        if not [x['url'] for ok, x in results if ok]:
            raise DropItem("Item contains no images")
        return item
