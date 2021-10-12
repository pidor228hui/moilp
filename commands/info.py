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
    
   [https://vk.com/wall-206192128_5|commands]
    
    {update_text}
    """.replace('    ', '')
    await edit_message(
        message,
        text
    )


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> чаты")
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
    
    ⚙️Команды связанные с чатами:
    
    🔕Удаление уведомлений:{"on&#9989;" if db.delete_all_notify else "off&#10060;"}
    🔔Вкл/Выкл уведомлений:{"on&#9989;" if db.disable_notifications else "off&#10060;"}
    🚶Автовыход с бесед:{"on&#9989;" if db.auto_exit_from_chat else "off&#10060;"}
    🏃Автовыход\n и удаление:{"on&#9989;" if db.auto_exit_from_chat_delete_chat else "off&#10060;"}
    📃Добавлять\n пригласившего в ЧС:{"on&#9989;" if db.auto_exit_from_chat_add_to_black_list else "off&#10060;"}
    🤗 Ответка в ебало:{"on&#9989;" if db.bio_reply else "off&#10060;"}
    
    """.replace('    ', '')
    await edit_message(
        message,
        text
    )
