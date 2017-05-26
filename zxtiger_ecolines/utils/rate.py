from __future__ import unicode_literals

import requests

from decimal import Decimal

BYN_TO_RUB = 0.03
BYN_TO_EUR = BYN_TO_USD = 1.86
UAH_TO_RUB = 0.46
UAH_TO_EUR = 29.46
UAH_TO_USD = 26.37

API_URL = 'http://api.fixer.io/latest?base='


class Rates(object):
    "Get rates from free api and converts to other currencies"

    def __init__(self):
        self.rates = {}
        for currency in ['RUB', 'EUR', 'USD']:
            self.rates[currency] = self._get_rates(currency)

        self.rates['RUB'].update({
            'UAH': UAH_TO_RUB, 'BYN': BYN_TO_RUB})
        self.rates['EUR'].update({
            'UAH': UAH_TO_EUR, 'BYN': BYN_TO_EUR})
        self.rates['USD'].update({
            'UAH': UAH_TO_USD, 'BYN': BYN_TO_USD})

    @staticmethod
    def _get_rates(currency):
        """
        Get rates from opensource fixer.io api

        :param currency: Base currency
        :type currency: str
        :rtype: dict
        """
        res = requests.get(API_URL + currency)
        return res.json()['rates']

    @staticmethod
    def _pretty(value):
        return Decimal(value).quantize(Decimal('.00'))

    def convert(self, value, from_currency, to_currency):
        if from_currency == to_currency:
            return self._pretty(value)
        local_rates = self.rates.get(to_currency)
        if not local_rates:
            return self._pretty(0)
        rate = local_rates.get(from_currency)
        if not rate:
            return self._pretty(0)
        return self._pretty(value / Decimal(rate))
