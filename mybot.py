from telegram.ext import Updater, CommandHandler

PROXY = {'proxy_url': 'socks5://t2.learn.python.ru:1080',
    'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'}}

def greet_user(update, context):
    print('Вызван /start')
    print(update)
    update.message.reply_text('Здравствую, пользователь!')

def main():
    mybot = Updater('5369400699:AAHiX9bTulpUaAc8PHB0CAqr0In5ZxP6jP8', use_context=True) #request_kwargs=PROXY

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))

    mybot.start_polling()
    mybot.idle()

main()