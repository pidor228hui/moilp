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
        update_text = f"\n\n⚠ Пока что обновлений нет\n" \
                      f"{version_rest['description']}\n"
    else:
        update_text = ""

    text = f"""
    ⬜🦊 Lisov Lp v{__version__} by {__author__} 
    ⬜
    ⬜⚠️ Удаление уведов: {"on&#9989;" if db.delete_all_notify else "off&#10060;"}
    ⬜🔕 Вкл/Выкл уведы: {"on&#9989;" if db.disable_notifications else "off&#10060;"}
    ⬜
    ⬜❌ ИгнорЛист: {len(db.ignored_members)}
    ⬜❌ Гл.ИгнорЛист: {len(db.ignored_global_members)}
    ⬜🔇 Muted: {len(db.muted_members)}
    ⬜❤️ Dovs: {len(db.trusted)}
    ⬜
    ⬜🚶 Leave chat: {"on&#9989;" if db.auto_exit_from_chat else "off&#10060;"}
    ⬜🔞 Deleted chat: {"on&#9989;" if db.auto_exit_from_chat_delete_chat else "off&#10060;"}
    ⬜🏳️‍🌈 Black list пригласивший: {"on&#9989;" if db.auto_exit_from_chat_add_to_black_list else "off&#10060;"}
    ⬜
    ⬜🗨️ Повторялка: {"on&#9989;" if db.repeater_active else "off&#10060;"}
    ⬜💫 Префикс повторялки: {db.repeater_word}
    ⬜
    ⬜🤗 Ответка в ебало: {"on&#9989;" if db.bio_reply else "off&#10060;"}
    ⬜    
    ⬜⚜️Удалялка: {db.dd_prefix}
    ⬜🔱Префиксы ЛП: {' '.join(db.service_prefixes)}
    ⬜⚕️Мои префиксы: {' '.join(db.self_prefixes) if db.self_prefixes else ''}
    ⬜🔺Префиксы ИДМ: {' '.join(db.duty_prefixes) if db.duty_prefixes else ''}
    ⬜
    ⬜[https://vk.com/wall-206192128_5|Команды этого LP тут]
    
    """.replace('    ', '')
    await edit_message(
        message,
        text
    )
