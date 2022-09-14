import telebot
from environs import Env
from google.cloud import dialogflow
from custom_handler import TelegramHandler
import logging
from define_intent import define_intent
logger = logging.getLogger(__file__)

env = Env()
env.read_env()
tg_token = env('TG_TOKEN')
bot = telebot.TeleBot(tg_token)


@bot.message_handler(commands=['start'])
def process_start_command(message):
    bot.send_message(message.chat.id, text='Здравствуйте, я бот и только учусь')


@bot.message_handler(content_types=['text'])
def send_text_tg(message):
    fallback,text = define_intent(message.text)
    bot.send_message(message.chat.id, text)


if __name__ == '__main__':
    chat_id = env('TG_CHAT_ID')
    log_bot = telebot.TeleBot(tg_token)
    logger.addHandler(TelegramHandler(log_bot, chat_id))
    logger.setLevel('INFO')
    bot.infinity_polling()
