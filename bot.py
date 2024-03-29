from datetime import time
import logging
import pytz

from telegram.bot import Bot
from telegram.ext import Updater, ConversationHandler, CommandHandler,\
                         MessageHandler, Filters, CallbackQueryHandler
from telegram.ext import messagequeue as mq
from telegram.utils.request import Request

from anketa import anketa_start, anketa_name, anketa_rating, anketa_skip,\
                   anketa_comment, anketa_dontknow
from handlers import check_users_photo, greet_user, guess_number,\
                     send_cat_picture, talk_to_me, user_locetion, subscribe,\
                     unsubscribe, set_alarm, cat_picture_rating
from jobs import send_updates

import settings

logging.basicConfig(filename="bot.log", level=logging.INFO)

PROXY = {'proxy_url': settings.PROXY_URL,
         'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME,
                                  'password': settings.PROXY_PASSWORD}}


class MQBot(Bot):
    def __init__(self, *args, is_queued_def=True, msg_queue=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._is_messages_queued_default = is_queued_def
        self._msg_queue = msg_queue or mq.MessageQueue()

    def __del__(self):
        try:
            self._msg_queue.stop()
        except:
            pass

    @mq.queuedmessage
    def send_message(self, *args, **kwargs):
        return super().send_message(*args, **kwargs)


def main():
    "initialize bot, db, updater and handlers"
    request = Request(
        con_pool_size=8
    )
    bot = MQBot(settings.API_KEY, request=request)
    mybot = Updater(bot=bot, use_context=True)

    jq = mybot.job_queue
    target_time = time(12, 0, tzinfo=pytz.timezone('US/Eastern'))
    jq.run_daily(send_updates, target_time)

    dp = mybot.dispatcher
    anketa = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('^(Заполнить анкету)$'), anketa_start)
        ],
        states={
            "name": [MessageHandler(Filters.text, anketa_name)],
            "rating": [MessageHandler(Filters.regex("^(1|2|3|4|5)$"),
                       anketa_rating)],
            "comment": [CommandHandler('skip', anketa_skip),
                        MessageHandler(Filters.text, anketa_comment)]
        },
        fallbacks=[
            MessageHandler(Filters.text | Filters.photo | Filters.video |
                           Filters.document | Filters.location, anketa_dontknow
                           )
        ]
    )
    dp.add_handler(anketa)
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler('guess', guess_number))
    dp.add_handler(CommandHandler('cat', send_cat_picture))
    dp.add_handler(CommandHandler('subscribe', subscribe))
    dp.add_handler(CommandHandler('unsubscribe', unsubscribe))
    dp.add_handler(CommandHandler('alarm', set_alarm))
    dp.add_handler(CallbackQueryHandler(cat_picture_rating, pattern="^(rate|)"))
    dp.add_handler(MessageHandler(Filters.regex('^(Прислать собачку)$'),
                   send_cat_picture))
    dp.add_handler(MessageHandler(Filters.photo, check_users_photo))
    dp.add_handler(MessageHandler(Filters.location, user_locetion))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info("Бот стартовал")
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
