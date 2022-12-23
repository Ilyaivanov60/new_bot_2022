import pytest
from unittest.mock import Mock
from telegram import User, Bot, Message, Chat, Update
from telegram.ext import Updater
from telegram.ext.callbackcontext import CallbackContext
from datetime import datetime


@pytest.fixture
def effective_user():
    return User(id=123, first_name='Gramm', is_bot=False, last_name='Chapmen',
                username='king_arthur')


@pytest.fixture
def updater():
    bot = Bot(token="123")
    return Updater(bot=bot, use_context=True)


def make_message(text, user, bot):
    message = Message(
        message_id=1,
        from_user=user,
        date=datetime.now(),
        chat=Chat(id=1, type='private'),
        text=text,
        bot=bot
    )
    message.reply_text = Mock(return_value=None)
    return message


def call_handler(updater, handler, message):
    update = Update(update_id=1, message=message)
    context = CallbackContext.from_update(update, updater.dispathcer)
    return handler(update, context)
