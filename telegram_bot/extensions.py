import requests
from config import APP_ID, keys


class APIException(Exception):
    pass


class MoneyConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты {quote}!')
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}!')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}!')
        try:
            amount = float(amount)
        except KeyError:
            raise APIException(f'Не удалось обработать количество {amount}!')

        r = requests.get(
            f'https://openexchangerates.org/api/latest.json?app_id={APP_ID}&base={quote_ticker}&symbols={base_ticker}'
        )

        oxr_latest = r.json()
        exchange_rate = oxr_latest['rates'][keys[base]]
        rate_amount = exchange_rate * amount

        return rate_amount
