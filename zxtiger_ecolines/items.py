# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZxtigerEcolinesItem(scrapy.Item):
    from_city = scrapy.Field()
    to_city = scrapy.Field()
    old_price = scrapy.Field()
    new_price = scrapy.Field()
    currency = scrapy.Field()
    start_date = scrapy.Field()
    end_date = scrapy.Field()
    link = scrapy.Field()

    price_in_rub = scrapy.Field()
    price_in_eur = scrapy.Field()
    price_in_usd = scrapy.Field()
