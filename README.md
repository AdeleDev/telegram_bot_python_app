# Telegram Api Bot
Api Bot implementation for Telegram. 
Bot accesses YandexPracticum test service API 
and finds out the status of homework: 
* whether homework was reviewed; 
* whether it was checked, and if it was checked; 
* then the reviewer accepted it or returned it for revision.

What bot does:
* requests test service API every 10 minutes and checks the status of the homework submitted for review;
* when updating the status, analyzes the API response and send a corresponding notification in Telegram;
* notifies about important issues with a message in Telegram.


### Built With

* [![Python][Python.io]][Python-url]
* [![Telegram][Telegram.io]][Telegram-url]

## Pre-installations

#### Clone the repo:

```sh
git clone https://github.com/AdeleDev/telegram_bot_python_app.git
```

#### Start and activate virtual environment:

```sh
python3 -m venv env
```

```sh
source env/bin/activate
```

#### Setup dependencies from requirements.txt file:

```sh
python3 -m pip install --upgrade pip
```

```sh
pip install -r requirements.txt
```

## Usage

#### Run project:

```sh
python .\bot.py 
```

## API addresses:

Get token request: 
```
https://oauth.yandex.ru/authorize?response_type=token&client_id=id
```
Get statuses request:

```
https://practicum.yandex.ru/api/user_api/homework_statuses/
```


<!-- MARKDOWN LINKS & IMAGES -->

[Python.io]: https://img.shields.io/badge/-Python-yellow?style=for-the-badge&logo=python

[Python-url]: https://www.python.org/

[Telegram.io]: https://img.shields.io/badge/-Telegram-white?style=for-the-badge&logo=telegram

[Telegram-url]: https://github.com/python-telegram-bot/python-telegram-bot
