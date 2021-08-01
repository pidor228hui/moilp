from vkbottle.api import UserApi
from vkbottle.framework.framework.rule import FromMe
from vkbottle.user import Blueprint, Message

from logger import logger_decorator
from objects import Database
from objects.trusted_user import TrustedUser
from rules import TrustedRule
from utils import get_ids_by_message, edit_message, get_full_name_by_member_id

user = Blueprint(
    name='repeat_blueprint'
)


@user.on.message_handler(TrustedRule(), text='<signal:repeater_word>')
@logger_decorator
async def repeat_wrapper(message: Message, signal: str, **kwargs):
    db = Database.get_current()
    if not db.repeater_active:
        return
    return signal


@user.on.message_handler(FromMe(), text='<prefix:service_prefix> +пвт')
@logger_decorator
async def repeat_wrapper(message: Message, **kwargs):
    db = Database.get_current()
    db.repeater_active = True
    db.save()
    await edit_message(message, "Повторялочка включена😊")


@user.on.message_handler(FromMe(), text='<prefix:service_prefix> -пвт')
@logger_decorator
async def repeat_wrapper(message: Message, **kwargs):
    db = Database.get_current()
    db.repeater_active = False
    db.save()
    await edit_message(message, "Повторялочка выключена😉")


@user.on.message_handler(FromMe(), text='<prefix:service_prefix> пвт <text>')
@logger_decorator
async def repeat_wrapper(message: Message, text: str, **kwargs):
    db = Database.get_current()
    db.repeater_word = text
    db.save()
    await edit_message(message, f"Теперь префикс пвт: <<{text}>>")
