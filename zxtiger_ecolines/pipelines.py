# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem

from .utils.rate import Rates


class DuplicatesPipeline(object):

    def __init__(self):
        self.directions_visited = set()

    def process_item(self, item, spider):
        directions = (item['from_city'], item['to_city'])
        if directions in self.directions_visited:
            raise DropItem(
                'Duplicate item found: %s' % directions)
        else:
            self.directions_visited.add(directions)
            return item


class RatesPipeline(object):
    def open_spider(self, spider):
        self.r = Rates()

    def process_item(self, item, spider):
        for currency in ['RUB', 'EUR', 'USD']:
            item['price_in_' + currency.lower()] = self.r.convert(
                item['new_price'], item['currency'], currency)
        return item
