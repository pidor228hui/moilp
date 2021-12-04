import time

from vkbottle.rule import FromMe
from vkbottle.user import Blueprint, Message

from logger import logger_decorator
from utils import edit_message

user = Blueprint(
    name='ping_blueprint'
)


async def get_ping(message: Message, answer: str) -> str:
    delta = round(time.time() - message.date, 2)

    
    if delta < 0:
        delta = "666"

    return f"{answer} Собираю информацию по пингу...\n" \
           f"♻️Обменялся с сервером за -> {delta}ms\n" \
           f"Vk² дал ответ через -> {delta}ms\n" \
           f"📡На всё про всё ушло -> (±{delta}ms/s) "


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> пинг")
@logger_decorator
async def ping_wrapper(message: Message, **kwargs):
    await edit_message(
        message,
        await get_ping(message, "📚detailed ping")
    )
