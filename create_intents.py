import argparse
import json
from google.cloud import dialogflow


def create_intent(
        project_id,
        display_name,
        training_phrases_parts,
        message_texts):
    """Create an intent of the given intent type."""
    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(
            text=training_phrases_part
        )
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print("Intent created: {}".format(response))


def create_intents_from_file(project_id, file):
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for intent_name, intent_data in data.items():
        create_intent(
            project_id,
            intent_name,
            intent_data['questions'],
            [intent_data['answer']]
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--project-id", help="Project/agent id.  Required.", required=True
    )
    parser.add_argument(
        "--file", help="Path to the intents file. Required.", required=True
    )

    args = parser.parse_args()
    create_intents_from_file(args.project_id, args.file)
