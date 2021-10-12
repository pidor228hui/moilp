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


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> лп")
@logger_decorator
async def info_wrapper(message: Message, **kwargs):
    db = Database.get_current()
    version_rest = requests.get(const.VERSION_REST).json()

    if version_rest['version'] != const.__version__:
        update_text = f"\n\n Обновление у вас\n на глазах📡"  \
                      f"\n"
    else:
        update_text = ""

    text = f"""
    🦊 Drocher228 by {__author__}\n V{__version__}
    
    📌Префикс команд: {' '.join(db.service_prefixes)}
    
    📚Настройки для чатов: чаты
    🔁Настройки повторялки: повторялка
    🖇️Настройки префиксов: префиксы
    
    🛡️Алиасы: {len(db.aliases)}
    
    {update_text}
    """.replace('    ', '')
    await edit_message(
        message,
        text
    )
