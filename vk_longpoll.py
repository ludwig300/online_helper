import os

import vk_api
from dotenv import load_dotenv
from google.cloud import dialogflow
from vk_api.longpoll import VkEventType, VkLongPoll


def detect_intent_text(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(
        text=text,
        language_code=language_code
    )

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={
            "session": session,
            "query_input": query_input
        }
    )

    return response.query_result.fulfillment_text


def main():
    load_dotenv()
    vk_api_token = os.getenv('VK_API_TOKEN')
    vk_session = vk_api.VkApi(token=vk_api_token)

    longpoll = VkLongPoll(vk_session)

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    project_id = os.getenv('DF_PROJECT_ID')
    dialogflow_language_code = 'ru'

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

            vk_session.method('messages.send', {
                'user_id': user_id,
                'message': dialogflow_response,
                'random_id': 0
            })


if __name__ == '__main__':
    main()
