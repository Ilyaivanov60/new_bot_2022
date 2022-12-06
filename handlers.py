from glob import glob
import os
from random import choice
from utils import get_smile, play_random_numbers, main_keyboard, has_object_on_image


def greet_user(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    print("Вызван /start")
    update.message.reply_text(
        f"{context.user_data['emoji']}Здравствуй, пользователь!",
        reply_markup=main_keyboard()
        )

def talk_to_me(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    text = update.message.text
    update.message.reply_text(f"{text} {context.user_data['emoji']}", reply_markup=main_keyboard())

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
    update.message.reply_text(message, reply_markup=main_keyboard())

def send_cat_picture(update, context):
    cat_photos_list = glob('images/dog*.jp*g')
    cat_pic_filename = choice(cat_photos_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_pic_filename, 'rb'), reply_markup=main_keyboard())

def user_locetion(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    coords = update.message.location
    update.message.reply_text(f"Ваши координаты{coords} {context.user_data['emoji']}", reply_markup=main_keyboard())

def check_users_photo(upadte, context):
    upadte.message.reply_text('Обрабатываем фото')
    os.makedirs('downloads', exist_ok=True)
    photo_file = context.bot.getFile(upadte.message.photo[-1].file_id)
    file_name = os.path.join("downloads", f"{upadte.message.photo[-1].file_id}.jpg")
    photo_file.download(file_name)
    upadte.message.reply_text('Файл сохранен')
    if has_object_on_image(file_name, 'dog'):
        upadte.message.reply_text('Обноружена собачка, сохраняю в библиотеку')
        new_file_name = os.path.join('images', f'cat_{photo_file.file_id}.jpg')
        os.rename(file_name, new_file_name)
    else:
        os.remove(file_name)
        upadte.message.reply_text('Тревога собачка не обнаружена')
