import requests
from vkbottle.rule import FromMe
from vkbottle.user import Blueprint, Message

import const
from const import __version__, __author__, __commands__
from logger import logger_decorator
from objects import Database
from utils import edit_message

user = Blueprint(
    name='lpcommands_blueprint'
)


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> команды")
@logger_decorator
async def info_wrapper(message: Message, **kwargs):
    db = Database.get_current()
    version_rest = requests.get(const.VERSION_REST).json()

    if version_rest['version'] != const.__version__:
        update_text = f"\n\n &#13;"  \
                      f"\n"
    else:
        update_text = ""

    text = f"""
    [{__commands__}|Комманды этого замечательного лп тут]🥰
     
    """.replace('    ', '')
    await edit_message(
        message,
        text
    )
