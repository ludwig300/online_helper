
# Online Helper Bot

Это проект бота, который может отвечать на сообщения пользователя в VK используя DialogFlow для понимания намерений пользователя.

## Установка

1. Клонируйте репозиторий:

   ```
   git clone https://github.com/<your_username>/online_helper.git
   cd online_helper
   ```
2. Установите зависимости:

   ```
   pip install -r requirements.txt
   ```
3. Создайте файл `.env` в корневой директории проекта и установите следующие переменные окружения:

   ```
   VK_API_TOKEN=<your_vk_api_token>

   GOOGLE_APPLICATION_CREDENTIALS=<path_to_your_google_application_credentials.json>

   DF_PROJECT_ID=<your_dialogflow_project_id>

   TG_TOKEN=<your_telegram_token>
   ```

## Запуск

Выполните следующую команду для запуска бота

- Vk bot: `python vk_longpoll.py`
- Telegram bot: `python tg_bot.py`



## Создание намерений DialogFlow

Чтобы создать намерения (intents) для DialogFlow, вы можете использовать скрипт `create_intents.py`.

Пример использования:

```
python create_intents.py --project-id <your_project_id> --file <path_to_your_intents_file>
```


Замените `<your_project_id>` на идентификатор вашего проекта DialogFlow и `<path_to_your_intents_file>` на путь к файлу JSON, который содержит ваши намерения.

Структура файла с намерениями должна быть следующей:

```json
{
    "IntentName1": {
        "questions": [
            "question1",
            "question2",
            ...
        ],
        "answer": "answer1"
    },
    "IntentName2": {
        "questions": [
            "question3",
            "question4",
            ...
        ],
        "answer": "answer2"
    },
    ...
}
```
