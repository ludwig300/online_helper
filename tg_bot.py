import os

from dotenv import load_dotenv
from telegram import Bot, Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

from dialogflow import detect_intent_text


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Здравствуйте!')


def handle_user_input(update: Update, context: CallbackContext) -> None:
    project_id = os.getenv('DF_PROJECT_ID')
    session_id = str(update.effective_user.id)
    language_code = "ru"
    text = update.message.text
    response_text = detect_intent_text(
        project_id,
        session_id,
        text,
        language_code
    )
    update.message.reply_text(response_text.query_result.fulfillment_text)


def error_callback(update: Update, context: CallbackContext) -> None:
    """Обработчик ошибок: отправляет сообщение об ошибке в Telegram."""
    logger_tg_token = os.getenv('LOGGER_TG_TOKEN')
    telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')

    error_message = f"Произошла ошибка во время работы Телеграм бота:\n{context.error}"
    bot = Bot(token=logger_tg_token)
    bot.send_message(chat_id=telegram_chat_id, text=error_message)


def main() -> None:
    load_dotenv()
    tg_token = os.getenv('TG_TOKEN')

    updater = Updater(tg_token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, handle_user_input)
    )

    # Регистрируем обработчик ошибок
    dispatcher.add_error_handler(error_callback)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
