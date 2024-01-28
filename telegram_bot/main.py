import telebot
from config import keys, TOKEN
from extensions import APIException, MoneyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help_handler(message: telebot.types.Message):
    text = (f'{message.chat.username},\n'
            f'чтобы начать работу введите следующую информацию:\n <название изначальной валюты>'
            f' <название валюты для конвертации> <количество конвертируемой валюты>\n'
            f'Увидеть список всех доступных валют: /values')
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def value_handler(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n - '.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Слишком много параметров!')

        quote, base, amount = values
        rate_amount = MoneyConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = f'Цена: {amount} {quote} в {base} - {rate_amount}'
        bot.reply_to(message, text)


bot.polling(none_stop=True)
