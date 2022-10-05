import json
import requests
from Currency_telebot_config import exchanges, API_KEY

#свой класс исключений
class APIException(Exception):
    pass

headers = {"apikey": API_KEY} #API-key для сервиса

class Convertor:

    @staticmethod
    def get_price(base: str, qoute: str, amount: str):
        try:
            base_key = exchanges[base.lower()]
        except KeyError: #исключение, если не найдена запись по ключу
            raise APIException(f"Валюта {base} не найдена!")

        try:
            sym_key = exchanges[qoute.lower()]
        except KeyError: #исключение, если не найдена запись по ключу
            raise APIException(f"Валюта {qoute} не найдена!")

        if base_key == sym_key: #проверка на неодинаковость валют
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            amount = float(amount)
        except ValueError:#исключение, если не удалось преобразовать из строки в число
            raise APIException(f'Не удалось обработать количество {amount}!')

        r = requests.get(f"https://api.apilayer.com/fixer/latest?symbols={sym_key}&base={base_key}", headers=headers)

        if (r.status_code//100) != 2:
            raise APIException(f"Ошибка получения данных с сервера, попробуйте позднее.")

        resp = json.loads(r.content)

        new_price = resp['rates'][sym_key] * amount
        new_price = round(new_price, 3)
        message = f"Цена {amount} {base} в {qoute} : {new_price}"
        return message