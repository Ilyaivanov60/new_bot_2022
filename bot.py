import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from handlers import check_users_photo, greet_user, guess_number, send_cat_picture, talk_to_me, user_locetion

import settings

logging.basicConfig(filename="bot.log", level=logging.INFO)

PROXY = {'proxy_url': settings.PROXY_URL,
    'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}

def main():
    mybot = Updater(settings.API_KEY, use_context=True) #request_kwargs=PROXY

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler('guess', guess_number))
    dp.add_handler(CommandHandler('cat', send_cat_picture))
    dp.add_handler(MessageHandler(Filters.regex('^(Прислать собачку)$'), send_cat_picture))
    dp.add_handler(MessageHandler(Filters.photo, check_users_photo))
    dp.add_handler(MessageHandler(Filters.location, user_locetion))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me)) 

    logging.info("Бот стартовал")
    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
    main()