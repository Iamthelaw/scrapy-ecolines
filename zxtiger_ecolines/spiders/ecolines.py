# encoding: utf-8
from __future__ import unicode_literals

import scrapy

from ..items import ZxtigerEcolinesItem

from ..utils.base import Price
from ..utils.base import Directions
from ..utils.base import Dates

DOMAIN = 'https://ecolines.net'
LOCAL_URLS = (
    '/ru/ru/predlozhenie/mezhdunarodnie',
    '/ua/ru/predlozhenie/mezhdunarodnie',
    '/by/ru/predlozhenie/mezhdunarodnie',
    '/bg/bg/akcii/v-chuzhbina',
    '/lv/en/offers/abroad',
    '/ee/en/offers/abroad',
    '/lt/en/offers/abroad',
    '/de/en/offers/abroad',
    '/pl/en/offers/abroad',
    '/international/en/offers/abroad'
)

OFFER_WRP = '.offer-wrapper'
OFFER_FROM_TO = '.offer-title ::text'
OFFER_NEW_PRICE = '.label.label-primary.pull-right ::text'
OFFER_OLD_PRICE = 'h2 .pull-left ::text'
OFFER_DATES = '.offer-period-dates ::text'
OFFER_URL = 'a ::attr(href)'


class EcolinesSpider(scrapy.Spider):
    name = 'ecolines'
    allowed_domains = ['ecolines.net']
    start_urls = tuple(DOMAIN + _ for _ in LOCAL_URLS)

    def parse(self, response):
        for wrapper in response.css(OFFER_WRP):
            directions = Directions(wrapper, OFFER_FROM_TO)
            new_price = Price(wrapper, OFFER_NEW_PRICE)
            old_price = Price(wrapper, OFFER_OLD_PRICE)
            offer_dates = Dates(wrapper, OFFER_DATES)
            link = wrapper.css(OFFER_URL)[0].extract()
            yield ZxtigerEcolinesItem(
                from_city=directions.from_city,
                to_city=directions.to_city,
                old_price=old_price.value,
                new_price=new_price.value,
                currency=new_price.currency,
                start_date=offer_dates.start_date,
                end_date=offer_dates.end_date,
                link=link)
