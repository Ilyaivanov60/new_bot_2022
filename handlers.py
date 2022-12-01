from glob import glob
from random import choice
from utils import get_smile, play_random_numbers, main_keyboard 


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