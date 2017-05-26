# encoding: utf-8
from __future__ import unicode_literals

from decimal import Decimal

from .data import pt as PATTERN


class Extractor(object):
    """
    Base class that search and validate extracted data

    :param wrapper: Any scrapy selector as wrapper
    :param selector: String representing selector that needs to be
    found in wrapper
    :type wrapper: :class:`scrapy.selector.unified.Selector`
    :type selector: str
    """

    def __init__(self, wrapper, selector):
        self.raw_value = wrapper.css(selector).extract()
        if self._non_empty:
            self._process_data()

    @property
    def _non_empty(self):
        """
        Validates that raw_value is a list and have values

        :rtype: bool
        """
        return (
            isinstance(self.raw_value, list)
            and len(self.raw_value) > 0)


class Price(Extractor):
    "Validates and converts raw price data"

    def __init__(self, wrapper, selector):
        self._value = 0
        self.currency = '-'
        Extractor.__init__(self, wrapper, selector)

    def __str__(self):
        return 'Price({}, {})'.format(self.value, self.currency)

    @property
    def value(self):
        "Formats value to decimal representation"
        return Decimal(
            self._value).quantize(Decimal('.00'))

    def _process_data(self):
        _ = self.raw_value[0].split(' ')
        self._value = ''.join(_[0:-1])
        self.currency = _[-1]


class Directions(Extractor):
    "Extracts and clean up from and to directions"

    def __init__(self, wrapper, selector):
        self.from_city = '-'
        self.to_city = '-'
        Extractor.__init__(self, wrapper, selector)

    def __str__(self):
        return 'Directions({}, {})'.format(
            self.from_city, self.to_city)

    @staticmethod
    def _normalize_city(city_value):
        city_value = city_value.replace('→', '').strip()
        return PATTERN.get(city_value) or city_value

    def _process_data(self):
        if len(self.raw_value) != 3:
            return
        _, raw_from_city, raw_to_city = self.raw_value
        self.from_city = self._normalize_city(raw_from_city)
        self.to_city = self._normalize_city(raw_to_city)


class Dates(Extractor):
    "Extract and convers start and end dates"

    def __init__(self, wrapper, selector):
        self.start_date = None
        self.end_date = None
        Extractor.__init__(self, wrapper, selector)

    def __str__(self):
        return 'Dates({}, {})'.format(
            self.start_date, self.end_date)

    def _process_data(self):
        self.start_date = self.raw_value[1]
        self.end_date = self.raw_value[3]
