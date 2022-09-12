import random
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from environs import Env
from google.cloud import dialogflow
import logging
import telebot
from custom_handler import TelegramHandler

logger = logging.getLogger(__file__)


def send_user_text(event, vk_api, project_id):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, event.user_id)
    text_input = dialogflow.TextInput(text=event.text, language_code='ru')
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    if response.query_result.intent.is_fallback:
        logger.info('Бот не понимает вопроса пользователя,помоги ему')
        return None
    else:
        text = response.query_result.fulfillment_text
        vk_api.messages.send(user_id=event.user_id, message=text, random_id=random.randint(1, 1000))


if __name__ == '__main__':
    env = Env()
    env.read_env()
    project_id = env('PROJECT_ID')
    tg_token = env('TG_TOKEN')
    log_bot = telebot.TeleBot(tg_token)
    chat_id = env('TG_CHAT_ID')
    logger.addHandler(TelegramHandler(log_bot,chat_id))
    logger.setLevel(logging.INFO)
    vk_session = vk.VkApi(token=env('VK_TOKEN'))
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            send_user_text(event, vk_api, project_id)
