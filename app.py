import telebot
from config import keys, TOKEN
from extencion import CryptoConverter, APIException


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands = ['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу, введите команду боту в следующем формате:\n<имя валюты, цену которой надо узнать> \
<имя валюты в которой надо узнать цену первой валюты> \
<количество первой валюты>\n<Увидеть список всех доступных валют: /values>\n<Увидеть список доступных возможностей можно при помощи комманд /help и /start'
    bot.reply_to(message, text)


@bot.message_handler(commands = ['values'])
def valuses(message: telebot.types.Message):
    text = 'Доступные валюты'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types = ['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Некорректное число параметров.')

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
         bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
