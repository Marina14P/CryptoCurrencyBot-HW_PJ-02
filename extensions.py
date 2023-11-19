import requests
import json

class APIException(Exception):
    def __init__(self, message):
        self.message = message

class CurrencyConverter:
    @staticmethod
    def get_price(base, quote, amount):
        api_key = '226a58f9094156ad516a1f591894c96f684ecf49a73a70588e41265193d8871b'

        url = f'https://min-api.cryptocompare.com/data/price?fsym={base}&tsyms={quote}&api_key={api_key}'

        try:
            response = requests.get(url)
            data = response.json()

            if quote not in data:
                raise APIException(f"Данные по валюте {quote} отсутствуют в ответе API")

            conversion_rate = data[quote]

            result = float(amount) * conversion_rate
            return result

        except Exception as e:
            raise APIException(f"Ошибка при получении данных: {str(e)}")