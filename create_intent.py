import json
from google.cloud import dialogflow
from environs import Env


def create_intent(project_id):
    """Create an intent of the given intent type."""
    with open('training_phrases.json', 'r') as file:
        phrases = file.read()
    training_phrases_parts = json.loads(phrases)
    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)


    for training_phrases_part, phrase_item in training_phrases_parts.items():
        training_phrases = []
        response_messages = []
        for item in phrase_item['questions']:

            part = dialogflow.Intent.TrainingPhrase.Part(text=item)
            training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
            training_phrases.append(training_phrase)
        text = dialogflow.Intent.Message.Text(text=[phrase_item['answer']])
        message = dialogflow.Intent.Message(text=text)
        response_messages.append(message)
        display_name = f'{training_phrases_part}'
        intent = dialogflow.Intent(
            display_name=display_name, training_phrases=training_phrases, messages=response_messages
        )
        response = intents_client.create_intent(
            request={"parent": parent, "intent": intent}
        )
        print("Intent created: {}".format(response))


if __name__ == '__main__':
    env = Env()
    env.read_env()
    project_id = env('PROJECT_ID')
    create_intent(project_id)
