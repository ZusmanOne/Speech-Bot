import random
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from environs import Env
import logging
import telebot
from custom_handler import TelegramHandler
from define_intent import define_intent

logger = logging.getLogger(__file__)


def send_text_vk(event, vk_api, project_id, session_id):
    fallback, message = define_intent(event.text, project_id, session_id)
    if fallback:
        logger.info('Бот не понимает вопроса пользователя,помоги ему')
        return None
    else:
        text = message
        vk_api.messages.send(user_id=event.user_id, message=text, random_id=random.randint(1, 1000))


if __name__ == '__main__':
    env = Env()
    env.read_env()
    project_id = env('PROJECT_ID')
    tg_token = env('TG_TOKEN')
    log_bot = telebot.TeleBot(tg_token)
    session_id = env('SESSION_ID')
    logger.addHandler(TelegramHandler(log_bot, session_id))
    logger.setLevel('INFO')
    vk_session = vk.VkApi(token=env('VK_TOKEN'))
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            send_text_vk(event, vk_api, project_id, session_id)
