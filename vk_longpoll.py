import os

import vk_api
from dotenv import load_dotenv
from telegram import Bot
from vk_api.longpoll import VkEventType, VkLongPoll

from dialogflow_functions import detect_intent_text


def main():
    load_dotenv()
    vk_api_token = os.getenv('VK_API_TOKEN')
    logger_tg_token = os.getenv('LOGGER_TG_TOKEN')
    telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
    vk_session = vk_api.VkApi(token=vk_api_token)

    longpoll = VkLongPoll(vk_session)

    project_id = os.getenv('DF_PROJECT_ID')
    dialogflow_language_code = 'ru'

    try:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                user_text = event.text
                user_id = event.user_id
                dialogflow_session_id = str(user_id)
                dialogflow_response = detect_intent_text(
                    project_id,
                    dialogflow_session_id,
                    user_text,
                    dialogflow_language_code
                )

                if dialogflow_response:
                    vk_session.method('messages.send', {
                        'user_id': user_id,
                        'message': dialogflow_response,
                        'random_id': 0
                    })
    except Exception as e:
        error_message = f"Произошла ошибка во время работы Vk бота::\n{e}"
        bot = Bot(token=logger_tg_token)
        bot.send_message(chat_id=telegram_chat_id, text=error_message)
        raise e


if __name__ == '__main__':
    main()
