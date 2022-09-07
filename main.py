import telebot
from environs import Env
from google.cloud import dialogflow


env = Env()
env.read_env()
tg_token = env('TG_TOKEN')
bot = telebot.TeleBot(tg_token)


@bot.message_handler(commands=['start'])
def process_start_command(message):
    bot.send_message(message.chat.id, text='Здравствуйте, я бот и только учусь')


@bot.message_handler(content_types=['text'])
def send_user_text(message, project_id=env('PROJECT_ID')):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, message.chat.id)
    text_input = dialogflow.TextInput(text=message.text, language_code='ru')
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    texts = response.query_result.fulfillment_text
    bot.send_message(message.chat.id, texts)


if __name__ == '__main__':
    bot.infinity_polling()