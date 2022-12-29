# Проект DogBot

DogBot - это тестовый бот для Telegram, с функцие распознования на фото собак, который по запросу присылает пользователю собачек. Так же в боте реализованы функция подписки-отписки пользователя, рейтинг фотографии, угадывание чилса пользователя, функция эхо-бот, заполнение анкеты, добавление коментириев к фото.

## Установка

1. Клонируйте репозиторий с GitHub 
`git clone https://github.com/Ilyaivanov60/new_bot_2022.git`
2. Создайте виртальное окружение
3. Установите зависимости  
`pip install -r requirements.txt`
4. Создайте файл `settings.py`
5. Впишите в `settings.py` преременые:
```
API_KEY = 'API-ключ BotFather'
PROXY_URL = 'Адрес прокси'
PROXY_USERNAME = 'Логин на прокси'
PROXY_PASSWORD ='Пароль на прокси'
USER_EMOJI =[':dog:', ':speedboat:', ':sunrise:', ':factory:', ':rowboat:']
MONGO_LINK = 'укажите путь к базе данных MongoDB'
```
6. [Кодеровку для emoji можно взять тут](https://www.webfx.com/tools/emoji-cheat-sheet/)

7. Запустите бота командой `python bot.py`