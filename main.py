import telebot
from extensions import APIException, Convertor
from Currency_telebot_config import TOKEN, exchanges
import traceback

currency_telebot = telebot.TeleBot(TOKEN)

# обработчик команд /start И /help
@currency_telebot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = 'Для работы введите команду в формате:\n<Название валюты> \
<В какую валюты перевести> <Количество переводимой валюты>.\n\
Для вывода доступных валют: /values'
    currency_telebot.send_message(message.chat.id, text)


# обработчик команды /values
@currency_telebot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for cur_name in exchanges.keys():  # проходимся по словарю с валютами и формируем текст ответа
        text = '\n'.join((text, cur_name))
    currency_telebot.reply_to(message, text)


# обработчик текстового сообщения - запроса на конвертацию
@currency_telebot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split(' ')  # выделяем параметры команды
    try:
        if len(values) != 3:  # количество параметров должно быть 3, иначе исключение и вывод ошибки
            raise APIException('Неверное количество параметров!')

        answer = Convertor.get_price(*values)  # статический метод класса для получения ответа
    except APIException as e:
        currency_telebot.reply_to(message, f"Ошибка в команде:\n{e}")
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        currency_telebot.reply_to(message, f"Неизвестная ошибка:\n{e}")
    else:
        currency_telebot.reply_to(message, answer)

currency_telebot.polling() #запустили бота
