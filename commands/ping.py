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

    return f"{answer} Checking ping LP...\n" \
           f"Время отклика сервера:{delta}с 👩‍💻"


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> пинг")
@logger_decorator
async def ping_wrapper(message: Message, **kwargs):
    await edit_message(
        message,
        await get_ping(message, "Ping🦁")
    )


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> пиу")
@logger_decorator
async def pau_wrapper(message: Message, **kwargs):
    await edit_message(
        message,
        await get_ping(message, "Piy🔫")
    )


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> кинг")
@logger_decorator
async def king_wrapper(message: Message, **kwargs):
    await edit_message(
        message,
        await get_ping(message, "KING🦍")
    )
