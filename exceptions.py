class YandexTelegramBotException(Exception):
    pass


class TokenNotFoundException(YandexTelegramBotException):
    pass


class BotSendRequestException(YandexTelegramBotException):
    pass


class YandexServerUnavailableException(YandexTelegramBotException):
    pass
