from emoji import emojize
from glob import glob
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from random import choice, randint

import settings

logging.basicConfig(filename="bot.log", level=logging.INFO)

PROXY = {'proxy_url': settings.PROXY_URL,
    'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}

def greet_user(update, context):
    smile = get_smile()
    print("Вызван /start")
    update.message.reply_text(f'{smile}Здравствуй, пользователь!')

def talk_to_me(update, context):
    smile = get_smile()
    text = update.message.text
    update.message.reply_text(f'{text} {smile}')

def get_smile():
    smile = choice(settings.USER_EMOJI)
    smile = emojize(smile)
    return smile

def play_random_numbers(user_number):
    bot_number = randint(user_number - 10, user_number + 10)
    if user_number > bot_number:
        message = f"Ваше число {user_number}, мое число{bot_number}, вы выйграли!"
    elif user_number == bot_number:
        message = f"Ваше число {user_number}, мое число{bot_number}, ничья!"
    else:
        message = f"Ваше число {user_number}, мое число{bot_number}, вы проиграли!"
    return message

def guess_number(update, context):
    print(context.args)
    if context.args:
        try:
            user_number = int(context.args[0])
            message = play_random_numbers(user_number)
        except (ValueError, TypeError):
            message = 'Введите челое число'
    else:
        message = 'Ввидите число'
    update.message.reply_text(message)

def send_cat_picture(update, context):
    cat_photos_list = glob('images/dog*.jp*g')
    cat_pic_filename = choice(cat_photos_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_pic_filename, 'rb'))
    

def main():
    mybot = Updater(settings.API_KEY, use_context=True) #request_kwargs=PROXY

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler('guess', guess_number))
    dp.add_handler(CommandHandler('cat', send_cat_picture))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info("Бот стартовал")
    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
    main()