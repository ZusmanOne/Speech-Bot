import telebot
from environs import Env


env = Env()
env.read_env()
tg_token = env('TG_TOKEN')

bot = telebot.TeleBot(tg_token)


@bot.message_handler(commands=['start'])
def process_start_command(message):
    bot.send_message(message.chat.id, text='Здравствуйте')


@bot.message_handler(content_types=['text'])
def send_user_text(message):
    bot.send_message(message.chat.id, message.text)


# # Press the green button in the gutter to run the script.
if __name__ == '__main__':
    bot.infinity_polling()
