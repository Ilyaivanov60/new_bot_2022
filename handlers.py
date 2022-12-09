from glob import glob
import os
from random import choice
from db import db, get_or_create_user, subscribe_user, unsubscribe_user
from utils import play_random_numbers, main_keyboard, has_object_on_image


def greet_user(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    print("Вызван /start")
    update.message.reply_text(
        f"{user['emoji']}Здравствуй, пользователь!",
        reply_markup=main_keyboard()
        )


def talk_to_me(update, context):
    user = get_or_create_user(db, update.effective_user,
                              update.message.chat.id)
    text = update.message.text
    update.message.reply_text(f"{text} {user['emoji']}",
                              reply_markup=main_keyboard())


def guess_number(update, context):
    user = get_or_create_user(db, update.effective_user,
                              update.message.chat.id)
    print(context.args)
    if context.args:
        try:
            user_number = int(context.args[0])
            message = play_random_numbers(user_number)
        except (ValueError, TypeError):
            message = 'Введите челое число'
    else:
        message = 'Ввидите число'
    update.message.reply_text(message, reply_markup=main_keyboard())


def send_cat_picture(update, context):
    user = get_or_create_user(db, update.effective_user,
                              update.message.chat.id)
    cat_photos_list = glob('images/dog*.jp*g')
    cat_pic_filename = choice(cat_photos_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_pic_filename, 'rb'),
                           reply_markup=main_keyboard())


def user_locetion(update, context):
    user = get_or_create_user(db, update.effective_user,
                              update.message.chat.id)
    coords = update.message.location
    update.message.reply_text(f"Ваши координаты{coords} {user['emoji']}",
                              reply_markup=main_keyboard())


def check_users_photo(update, context):
    user = get_or_create_user(db, update.effective_user,
                              update.message.chat.id)
    update.message.reply_text('Обрабатываем фото')
    os.makedirs('downloads', exist_ok=True)
    photo_file = context.bot.getFile(update.message.photo[-1].file_id)
    file_name = os.path.join("downloads",
                             f"{update.message.photo[-1].file_id}.jpg")
    photo_file.download(file_name)
    update.message.reply_text('Файл сохранен')
    if has_object_on_image(file_name, 'dog'):
        update.message.reply_text('Обноружена собачка, сохраняю в библиотеку')
        new_file_name = os.path.join('images', f'cat_{photo_file.file_id}.jpg')
        os.rename(file_name, new_file_name)
    else:
        os.remove(file_name)
        update.message.reply_text('Тревога собачка не обнаружена')


def subscribe(update, context):
    user = get_or_create_user(db, update.effective_user,
                              update.message.chat.id)
    subscribe_user(db, user)
    update.message.reply_text('Вы успешно подписались!')


def unsubscribe(update, context):
    user = get_or_create_user(db, update.effective_user,
                              update.message.chat.id)
    unsubscribe_user(db, user)
    update.message.reply_text('Вы успешно отписались!')
