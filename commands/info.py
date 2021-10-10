import requests
from vkbottle.rule import FromMe
from vkbottle.user import Blueprint, Message

import const
from const import __version__, __author__
from logger import logger_decorator
from objects import Database
from utils import edit_message

user = Blueprint(
    name='info_blueprint'
)


@user.on.message_handler(FromMe(), text="{service_prefix} лп")
@logger_decorator
async def info_wrapper(message: Message, **kwargs):
    db = Database.get_current()
    version_rest = requests.get(const.VERSION_REST).json()

    if version_rest['version'] != const.__version__:
        update_text = f"\n\n🖇️Обновы будут тогда \n Когда выучу Python"  \
                      f"\n"
    else:
        update_text = ""

    text = f"""
    🦊 Drocher228 \n by{__author__} Version:({__version__})
    [https://vk.com/wall-206192128_5|Команды этого LP тут]
    🔎Updates:{update_text}
  
    """.replace('    ', '')
    await edit_message(
        message,
        text
    )
