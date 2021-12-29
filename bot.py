import telebot
from config import TOKEN
from extensions import CurrencyConvert, ConvertionException


#import pytelegrambotapi
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    text = "Введите команду боту через пробел в следующем формате:\n <Код валюты> <Код валюты для перевода> <количество> \n\nПолучить список доступных валют: /value"

    bot.reply_to(message, f"Добро пожаловать.\n {text}")


@bot.message_handler(commands=['value'])
def handle_value(message):
    text = "Справочник валют:\n <Код> : <Наименование валюты>\n"
    currency = CurrencyConvert().get_currencies()

    for key, value in currency.items():
       text += key + ' : ' + value + '\n'

    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def handle_convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Неверное количество параметров')
        fsym, tsyms, amount = values

        total = CurrencyConvert.convert(fsym.upper(), tsyms.upper(), amount)

    except ConvertionException as e:
        bot.reply_to(message, f'Пользовательская ошибка\n {e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n {e}')
    else:
        text = f'Стоимость {amount} {fsym} в {tsyms} = {total}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)