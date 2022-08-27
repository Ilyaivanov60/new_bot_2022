import logging
import ephem
import datetime
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import settings
"""'москва', 'архангелск', 'курск', 'копенгаген',
 'нижний новгород', 'донецк'"""
cities = []

logging.basicConfig(filename='bot.log', level=logging.INFO)

PROXY = {'proxy_url': settings.PROXY_URL,
    'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}

def greet_user(update, context):
    update.message.reply_text('Здравствую, пользователь!')

def tolk_to_me(update, context):
    text = update.message.text
    update.message.reply_text(text)

def get_planet(update, context):
    text = update.message.text.split()
    planet = text[1]
    date = datetime.datetime.now()
    if planet.lower() == 'mars':
        m = ephem.Mars(date)
        update.message.reply_text(ephem.constellation(m))

def word_counter(update, context):
    text = update.message.text.split(' ')
    count_word = len(text)
    if count_word == 1:
        update.message.reply_text(f'Вы не ввели слово')
    else:    
        update.message.reply_text(f'{count_word} слова')

def next_moon(update, context):
    date_sting = datetime.datetime.strptime(update.message.text, '/next_full_moon %Y/%m/%d')
    print(date_sting)
    
def play_cities(update, context):
    if cities == []:
        update.massega.reply_text('Вы победили!')
    else:
        user_city = update.message.text.lower().split()[1]
        letter = user_city[-1]
        cities.remove(user_city)
        for city in cities:
            if city[0] == letter:
                update.message.reply_text(city)
                break
        cities.remove(city)

    print(cities)
    
def calculate (update, context):
    try: 
        text = update.message.text.split()
        text.remove('/Calc')
        for elemet in text:
            for simbol in elemet:
                if simbol == '-':
                    index = elemet.find('-')
                    update.message.reply_text(float(elemet[:index]) - float(elemet[index+1:]))
                elif simbol == '+':
                    index = elemet.find('+')
                    update.message.reply_text(float(elemet[:index]) + float(elemet[index+1:]))
                elif simbol == '*':
                    index = elemet.find('*')
                    update.message.reply_text(float(elemet[:index]) * float(elemet[index+1:]))
                elif simbol == '/':
                    index = elemet.find('/')
                    update.message.reply_text(float(elemet[:index]) / float(elemet[index+1:]))
    except ZeroDivisionError:
        update.message.reply_text('На 0 делить не льзя')
    except (TypeError, ValueError):
        update.message.reply_text('Вы не ввели число')
def main():
    mybot = Updater(settings.API_KEY, use_context=True) #request_kwargs=PROXY

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('wordcount', word_counter))
    dp.add_handler(CommandHandler('planet', get_planet))
    dp.add_handler(CommandHandler('next_full_moon', next_moon))
    dp.add_handler(CommandHandler('cities', play_cities))
    dp.add_handler(CommandHandler('Calc', calculate))
    dp.add_handler(MessageHandler(Filters.text, tolk_to_me))


    logging.info('Бот стартовал')
    mybot.start_polling()
    mybot.idle()

if  __name__ == '__main__':
    main()