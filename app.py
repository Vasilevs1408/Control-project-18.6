import telebot
from config import keys, TOKEN
from extencion import CryptoConverter, APIException


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands = ['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу, введите команду боту в следующем формате:\n<имя валюты> \
<в какую валюту перевести> \
<колличество переведённой валюты>\nУвидеть список всех доступных валют: /values'
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
            raise APIException('Слишком много параметров.')

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
         bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        a = total_base * float(amount)
        text = f'Цена {amount} {quote} в {base} = {a}'
        bot.send_message(message.chat.id, text)


bot.polling()
