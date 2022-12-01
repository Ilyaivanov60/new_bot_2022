# Проект DogBot

DogBot - это бот для Telegram, который присылает пользователю собачек.

## Установка

1. Клонируйте репозиторий с GitHub 
`git clone https://github.com/Ilyaivanov60/new_bot_2022.git`
2. Создайте виртальное окружение
3. Установите зависимости  
`pip install -r requirements.txt`
4. Создайте файл `settings.py`
5. Впишите в `settings.py` преременые:
```
API_KEY = 'API-ключ бота'
PROXY_URL = 'Адрес прокси'
PROXY_USERNAME = 'Логин на прокси'
PROXY_PASSWORD ='Пароль на прокси'
USER_EMOJI =[':dog:', ':speedboat:', ':sunrise:', ':factory:', ':rowboat:']
```
6. Запустите бота командой `python bot.py`