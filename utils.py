from random import randint

from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2

from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
import settings


def get_bot_number(user_number):
    return randint(user_number - 10, user_number + 10)


def play_random_numbers(user_number, bot_number):
    if user_number > bot_number:
        message = f"Ваше число {user_number}, мое {bot_number}, вы выйграли!"
    elif user_number == bot_number:
        message = f"Ваше число {user_number}, мое {bot_number}, ничья!"
    else:
        message = f"Ваше число {user_number}, мое {bot_number}, вы проиграли!"
    return message


def main_keyboard():
    return ReplyKeyboardMarkup([['Прислать собачку', KeyboardButton(
        "Мои координаты", request_location=True), 'Заполнить анкету']])


def has_object_on_image(file_name, object_name):
    channel = ClarifaiChannel.get_grpc_channel()
    app = service_pb2_grpc.V2Stub(channel)
    metadata = (('authorization', f'Key {settings.CLARIFAI_API_KEY}'),)

    with open(file_name, 'rb') as f:
        file_data = f.read()
        image = resources_pb2.Image(base64=file_data)

    request = service_pb2.PostModelOutputsRequest(
        model_id='aaa03c23b3724a16a56b629203edc62c',
        inputs=[
            resources_pb2.Input(data=resources_pb2.Data(image=image))
        ])

    response = app.PostModelOutputs(request, metadata=metadata)
    return check_responce_for_obkect(response, object_name)


def check_responce_for_obkect(response, object_name):
    if response.status.code == status_code_pb2.SUCCESS:
        for concept in response.outputs[0].data.concepts:
            if concept.name == object_name and concept.value >= 0.85:
                return True
    else:
        print(f"Ошибка распознавания: {response.outputs[0].status.details}")

    return False


def cat_rating_inline_keyboard(image_name):
    callback_text = f"rate|{image_name}|"
    inlinekeyboard = [
        [
            InlineKeyboardButton("Нравится", callback_data=callback_text + '1'),
            InlineKeyboardButton("Не нравится", callback_data=callback_text +'-1')
        ]
    ]
    return InlineKeyboardMarkup(inlinekeyboard)


if __name__ == '__main__':
    print(has_object_on_image('images/cat.jpeg', 'dog'))
    print(has_object_on_image('images/dog1.jpeg', 'dog'))
