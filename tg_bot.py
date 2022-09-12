import telebot
from environs import Env
from google.cloud import dialogflow
from custom_handler import TelegramHandler
import logging

logger = logging.getLogger(__file__)

env = Env()
env.read_env()
tg_token = env('TG_TOKEN')
bot = telebot.TeleBot(tg_token)


@bot.message_handler(commands=['start'])
def process_start_command(message):
    bot.send_message(message.chat.id, text='Здравствуйте, я бот и только учусь')


@bot.message_handler(content_types=['text'])
def send_user_text(message, project_id=env('PROJECT_ID'), session_id=env('TG_CHAT_ID')):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=message.text, language_code='ru')
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    if response.query_result.intent.is_fallback:
        logger.info('Нет ответа на вопрос,разберись сам')
        return None
    else:
        text = response.query_result.fulfillment_text
        bot.send_message(message.chat.id, text)


if __name__ == '__main__':
    chat_id = env('TG_CHAT_ID')
    log_bot = telebot.TeleBot(tg_token)
    logger.addHandler(TelegramHandler(log_bot,chat_id))
    logger.setLevel('INFO')
    bot.infinity_polling()
