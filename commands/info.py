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


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> инфо")
@logger_decorator
async def info_wrapper(message: Message, **kwargs):
    db = Database.get_current()
    version_rest = requests.get(const.VERSION_REST).json()

    if version_rest['version'] != const.__version__:
        update_text = f"\n\n⚠ Доступно обновление {version_rest['version']}\n" \
                      f"{version_rest['description']}\n"
    else:
        update_text = ""

    text = f"""
    🦊 Test LP v{__version__} by {__author__}

    ▶ рукаптча: {"&#9989;" if db.ru_captcha_key else "&#10060;"}
    ▶ Удаление уведов: {"&#9989;" if db.delete_all_notify else "&#10060;"}
    ▶ Выключение уведомлений: {"&#9989;" if db.disable_notifications else "&#10060;"}

    ▶ В игноре: {len(db.ignored_members)}
    ▶ В глобальном игноре: {len(db.ignored_global_members)}
    ▶ В муте: {len(db.muted_members)}
    ▶ Довы: {len(db.trusted)}
    ▶ Алиасов: {len(db.aliases)}
    ▶ Шаблонов для удаления: {len(db.regex_deleter)}

    ▶ Выходить из бесед: {"&#9989;" if db.auto_exit_from_chat else "&#10060;"}
    ▶ Удалять диалог: {"&#9989;" if db.auto_exit_from_chat_delete_chat else "&#10060;"}
    ▶ Добавлять пригласившего в ЧС: {"&#9989;" if db.auto_exit_from_chat_add_to_black_list else "&#10060;"}
    
    ▶ Повторялка: {"&#9989;" if db.repeater_active else "&#10060;"}
    ▶ Триггер на повторялку: {db.repeater_word}

    ▶ Заражалка: {"&#9989;" if db.bio_reply else "&#10060;"}
        
    ▶ Префикс ДД: {db.dd_prefix}
    ▶ Сервисные префиксы: {' '.join(db.service_prefixes)}
    ▶ Мои префиксы: {' '.join(db.self_prefixes) if db.self_prefixes else ''}
    ▶ Префиксы ИДМ: {' '.join(db.duty_prefixes) if db.duty_prefixes else ''}{update_text}
    """.replace('    ', '')
    await edit_message(
        message,
        text
    )
