import telebot
from config import keys, TOKEN
from extensions import APIException, CryptoConverter



bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands = ['start', 'help'])
def echo_test(message: telebot.types.Message):
    text = 'Чтобы начать работу введите комманду боту в следующем формате:\n<имя валюты> \
<в какую валюту перевести> \
<колличество переводимой валюты>\nУвидеть список всех доступных валют: /values'
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands = ['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types = ['text',])
def convert(message: telebot.types.Message):
    values = message.text.split(' ')

    if len(values) != 3:
        raise APIException('Слишком много параметров.')

    quote, base, amount = values
    total_base = CryptoConverter.get_price(quote, base, amount)

    text = f'Цена {amount} {quote} в {base} - {total_base}'
    bot.send_message(message.chat.id, text)

bot.polling()