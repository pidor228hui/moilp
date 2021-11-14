import requests
from vkbottle.rule import FromMe
from vkbottle.user import Blueprint, Message

import const
from const import __version__, __author__, __commands__
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
        update_text = f"\n\n [https://vk.com/lislp|Запись в группе про обновление 1.1.7]"  \
                      f"\n"
    else:
        update_text = ""

    text = f"""
    [id471721271|🦊]Спиженный лп IDM V{__version__} 
    
    ❣️Prefix: <<{' '.join(db.service_prefixes)}>>
    
    ⚙️Функции:
    
    🔕Удаление Аллов:  {"&#9989;" if db.delete_all_notify else "&#10060;"}
    🔔Уведы:  {"&#9989;" if db.disable_notifications else "&#10060;"}
    🚫Автовыход:  {"&#9989;" if db.auto_exit_from_chat else "&#10060;"} +del {"&#9989;" if db.auto_exit_from_chat_delete_chat else "&#10060;"} 
    ㊙️Автовыход+ЧС:  {"&#9989;" if db.auto_exit_from_chat_add_to_black_list else "&#10060;"}
    🔄Повторялка:
    
    🦎Повторялка:  {"on&#9989;" if db.repeater_active else "off&#10060;"}
    💠Префикс:  {db.repeater_word}
    
    📌Префиксы:
    
    🚫DD:  {db.dd_prefix}
    🤖IDM:  {' '.join(db.self_prefixes) if db.self_prefixes else ''}
    🐺IDM repeat:  {' '.join(db.duty_prefixes) if db.duty_prefixes else ''}
    
    📵Игнорируемых(чат):  {len(db.ignored_members)}  GL:  {len(db.ignored_global_members)}
    
    🐍Довов:  {db.trusted}
    
    💊Otvetka:
    
    ☣️Infected: {"&#9989;" if db.bio_reply else "&#10060;"}
    
            
    """.replace('    ', '')
    await edit_message(
        message,
        text
)
