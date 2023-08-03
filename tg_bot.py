import os

from dotenv import load_dotenv
from google.cloud import dialogflow
from telegram import Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)
from telegram import Bot


def send_telegram_message(token, chat_id, message):
    bot = Bot(token=token)
    bot.send_message(chat_id=chat_id, text=message)


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Здравствуйте!')


def detect_intent_texts(project_id, session_id, text, language_code, update: Update, context: CallbackContext):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    # Отправляем пользователю Telegram ответ бота DialogFlow
    update.message.reply_text(response.query_result.fulfillment_text)


def echo(update: Update, context: CallbackContext) -> None:
    """Эхо функция: отправляет сообщение пользователя в DialogFlow."""
    project_id = os.getenv('DF_PROJECT_ID')
    session_id = str(update.effective_user.id)
    language_code = "ru"
    text = update.message.text
    detect_intent_texts(project_id, session_id, text, language_code, update, context)


def error_callback(update: Update, context: CallbackContext) -> None:
    """Обработчик ошибок: отправляет сообщение об ошибке в Telegram."""
    logger_tg_token = os.getenv('LOGGER_TG_TOKEN')
    telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')

    error_message = f"Произошла ошибка во время работы Телеграм бота:\n{context.error}"
    send_telegram_message(logger_tg_token, telegram_chat_id, error_message)


def main() -> None:
    load_dotenv()
    tg_token = os.getenv('TG_TOKEN')

    updater = Updater(tg_token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Регистрируем обработчик ошибок
    dispatcher.add_error_handler(error_callback)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
