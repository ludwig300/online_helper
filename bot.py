import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)


def start(update: Update, context: CallbackContext) -> None:
    """Отправляет сообщение при команде /start."""
    update.message.reply_text('Здравствуйте!')


def echo(update: Update, context: CallbackContext) -> None:
    """Эхо функция: повторяет сообщение пользователя."""
    update.message.reply_text(update.message.text)


def main() -> None:
    load_dotenv()
    tg_token = os.getenv('TG_TOKEN')
    """Запуск бота."""
    updater = Updater(tg_token, use_context=True)

    dispatcher = updater.dispatcher

    # обработчик команды /start
    dispatcher.add_handler(CommandHandler('start', start))

    # обработчик всех текстовых сообщений
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, echo)
    )

    # начинаем поиск обновлений
    updater.start_polling()

    # работаем до тех пор, пока бот не будет остановлен
    updater.idle()


if __name__ == '__main__':
    main()
