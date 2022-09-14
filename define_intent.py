from google.cloud import dialogflow
from environs import Env

env = Env()
env.read_env()


def define_intent(text):
    project_id = env('PROJECT_ID')
    session_id = env('SESSION_ID')
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code='ru')
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    return (
        response.query_result.intent.is_fallback,
        response.query_result.fulfillment_text
    )

