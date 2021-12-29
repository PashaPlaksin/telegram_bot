import json
import requests
from config import APIKEY

class ConvertionException(Exception):
    pass

class CurrencyConvert:
    @staticmethod
    def convert(fsym: str, tsyms: str, amount: str):

        currency = CurrencyConvert.get_currencies()

        if fsym == tsyms:
            raise ConvertionException("Указана одинаковая валюта")

        if (fsym in currency) == False:
            raise ConvertionException(f'Указаннная валюта {fsym} не найдена')

        if (tsyms in currency) == False:
            raise ConvertionException(f'Указаннная валюта {tsyms} не найдена')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}')
        cur = '_'.join([fsym, tsyms])

        r = requests.get(f'https://free.currconv.com/api/v7/convert?q={cur}&compact=ultra&apiKey={APIKEY}')
        total = json.loads(r.content)
        total = list(total.values())[0] * amount

        return total

    @staticmethod
    def get_currencies():
        r = requests.get(f'https://free.currconv.com/api/v7/currencies?apiKey={APIKEY}')
        currency = json.loads(r.content)
        currencies = {}

        for key, value in currency['results'].items():
            currencyName = value.get('currencyName')
            currencies[currencyName] = key

        sorted_tuples = sorted(currencies.items(), key=lambda item: item[1])
        sorted_dict = {v: k for k, v in sorted_tuples}

        return sorted_dict