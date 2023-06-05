import logging
import os
import sys
import time
from http import HTTPStatus

import requests
import telegram
from dotenv import load_dotenv

from exceptions import BotSendRequestException,\
    YandexServerUnavailableException, YandexTelegramBotException

load_dotenv()

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}

HOMEWORK_VERDICTS = {
    'approved': 'Review done: No points to fix',
    'reviewing': 'Task was taken to review.',
    'rejected': 'Review done: There are some points to fix.'
}


def check_tokens():
    """Проверка токенов."""
    logging.debug("Проверка наличия токенов..")
    token_ok = True
    for token in (PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID):
        if not token:
            token_ok = False
    return token_ok


def send_message(bot, message):
    """Отправка сообщения в телеграм бот."""
    logging.debug('Отправка сообщения в чат телеграмм бота..')
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    except telegram.error.TelegramError as e:
        message = f'Ошибка отправки телеграм сообщения: {e}'
        logging.error(message)
        raise BotSendRequestException(message)
    except Exception as e:
        message = f'Неожиданная ошибка во время отправки сообщения: {e}'
        logging.exception(message)
        raise BotSendRequestException(message)
    else:
        logging.debug('Сообщение отправлено в чат')


def get_api_answer(timestamp):
    """Запрос на сервер Яндекса."""
    logging.info('Запрос информации с сервера Яндекса..')
    params = {'from_date': timestamp}
    try:
        response = requests.get(ENDPOINT, headers=HEADERS, params=params)
        if response.status_code != HTTPStatus.OK:
            response.raise_for_status()
        logging.info(f'Ответ получен: {response.json()}')
        return response.json()
    except requests.exceptions.RequestException as e:
        raise YandexServerUnavailableException(
            f'Ошибка при запросе на сервер Яндекса: {e}')


def check_response(response):
    """Проверка ответа сервера Яндекса."""
    logging.debug('Проверка синтаксиса ответа..')
    if not isinstance(response, dict):
        raise TypeError(
            f'Возвращаемый тип не соответствует словарю: {type(response)}')

    homeworks = response.get('homeworks')
    if not isinstance(homeworks, list):
        raise TypeError(
            f'Возвращаемый тип не соответствует списку: {homeworks}')
    logging.debug('Проверка успешно закончена')
    return homeworks


def parse_status(homework):
    """Проверка статуса задачи."""
    if 'homework_name' not in homework:
        raise KeyError('В ответе нет ключа homework_name')

    homework_name = homework.get('homework_name')
    logging.info(f'Получение статуса задачи {homework_name}')
    homework_status = homework.get('status')

    if homework_status not in HOMEWORK_VERDICTS:
        raise Exception(f"Неизвестный статус: {homework_status}")

    verdict = HOMEWORK_VERDICTS.get(homework_status)
    logging.info(f'Вердикт по задаче: {verdict}')
    return {f'Изменился статус проверки работы "'
            f'{homework_name}". {verdict}'}


def main():
    """Основная программа."""
    if not check_tokens():
        message = 'Не все токены установлены, работа бота прекращена'
        logging.critical(message)
        sys.exit(message)
    logging.debug('Все токены установлены, старт бота..')
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    timestamp = int(time.time())
    while True:
        try:
            response_result = get_api_answer(timestamp)
            homeworks = check_response(response_result)
            timestamp = response_result['current_date']
            if len(homeworks) > 0:
                send_message(bot, parse_status(homeworks[0]))
            else:
                logging.info("Новые задания не найдены")
        except YandexTelegramBotException as e:
            logging.exception(f'Сбой в работе бота: {e}')
        except Exception as e:
            message = f'Неизвестный сбой в работе программы: {e}'
            logging.exception(message)
            send_message(bot, message)
        finally:
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s [%(levelname)s] %(message)s',
        level=logging.DEBUG)

    main()
