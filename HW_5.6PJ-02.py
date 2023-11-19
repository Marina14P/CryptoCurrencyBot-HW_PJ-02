import telebot
from extensions import CurrencyConverter, APIException
from config import keys, TOKEN


bot = telebot.TeleBot(TOKEN)



@bot.message_handler(commands=['start', 'help'])
def send_instructions(message):
    instructions = ("Привет! Чтобы узнать цену на валюту, отправьте сообщение в формате:\n"
                    "<имя валюты, цену которой хотите узнать> "
                    "<имя валюты, в которой надо узнать цену первой валюты> "
                    "<количество первой валюты>\n"
                    "Для просмотра доступных валют введите /values")
    bot.send_message(message.chat.id, instructions)

@bot.message_handler(commands=['values'])
def show_available_currencies(message):
    available_currencies = "Доступные валюты: " + ', '.join(keys.keys())
    bot.send_message(message.chat.id, available_currencies)

@bot.message_handler(content_types=['text'])
def get_currency_price(message):
    try:
        user_input = message.text.split()

        if len(user_input) != 3:
            raise APIException("Неправильный формат запроса")

        base, quote, amount = user_input
        base = base.lower()
        quote = quote.lower()

        if base not in keys or quote not in keys:
            raise APIException("Неправильные имена валют")

        converted_amount = CurrencyConverter.get_price(keys[base], keys[quote], amount)
        bot.send_message(message.chat.id, f"{amount} {base.upper()} = {converted_amount} {quote.upper()}")

    except APIException as e:
        bot.send_message(message.chat.id, f"Ошибка: {e.message}")

bot.polling(none_stop=True)