
import os
import random

import vk_api
from dotenv import load_dotenv
from vk_api.longpoll import VkEventType, VkLongPoll


def echo(event, vk_api):
    vk_api.messages.send(
        user_id=event.user_id,
        message=event.text,
        random_id=random.randint(1, 1000)
    )


if __name__ == "__main__":
    load_dotenv()
    vk_api_token = os.getenv('VK_API_TOKEN')
    vk_session = vk_api.VkApi(token=vk_api_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api)
