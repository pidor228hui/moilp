import re

from vkbottle.framework.framework.rule import FromMe
from vkbottle.user import Blueprint, Message

from logger import logger_decorator
from objects import Database, RegexDeleter
from rules import RegexDeleter as RegexDeleterRule
from utils import edit_message

user = Blueprint(
    name='repeat_blueprint'
)


@user.on.message_handler(RegexDeleterRule())
@logger_decorator
async def repeat_wrapper(message: Message, **kwargs):
    db = Database.get_current()
    for regex_del in db.regex_deleter:
        if regex_del.chat_id == message.peer_id:
            if re.findall(regex_del.regex, message.text):
                await message.api.messages.delete(message_ids=[message.id], delete_for_all=regex_del.for_all)


@user.on.message_handler(
    FromMe(),
    text=[
        '<prefix:service_prefix> +regex <name> <regex> <for_all:yes_or_no>',
        '<prefix:service_prefix> +regex <name> <regex>',
    ]
)
@logger_decorator
async def repeat_wrapper(message: Message, name: str, regex: str, for_all: bool = False, **kwargs):
    db = Database.get_current()

    if name in [regex_del.name for regex_del in db.regex_deleter]:
        await edit_message(message, "Такой шаблон удаления уже есть.🤔")
        return
    db.regex_deleter.append(RegexDeleter(name=name, regex=regex, for_all=for_all, chat_id=message.peer_id))
    db.save()
    await edit_message(message, "Шаблон created🤗")


@user.on.message_handler(FromMe(), text='<prefix:service_prefix> -regex <name>')
@logger_decorator
async def repeat_wrapper(message: Message,  name: str, **kwargs):
    db = Database.get_current()
    deleter = None
    for regex_del in db.regex_deleter:
        if regex_del.name == name:
            deleter = regex_del
    if deleter is None:
        await edit_message(message, "Такого шаблона удаления нет.🤔")
        return
    db.regex_deleter.remove(deleter)
    db.save()
    await edit_message(message, "Шаблон deleted🙂")


@user.on.message_handler(FromMe(), text='<prefix:service_prefix> regex')
@logger_decorator
async def repeat_wrapper(message: Message, **kwargs):
    db = Database.get_current()
    text = "✴️Шаблончики для удаления:\n"
    index = 1
    for regex_del in db.regex_deleter:
        text += f"{index}. {regex_del.name} | {regex_del.regex} | {regex_del.chat_id}\n"
        index += 1
    await edit_message(message, text)
