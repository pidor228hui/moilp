from typing import Optional

from vkbottle.rule import ChatActionRule, FromMe
from vkbottle.user import Blueprint, Message

from logger import logger_decorator
from objects import Database, ChatEnterModel
from rules import ChatEnterRule
from utils import edit_message

user = Blueprint(
    name='add_to_friends_on_chat_enter'
)


@user.on.chat_message(ChatActionRule(["chat_invite_user", "chat_invite_user_by_link"]), ChatEnterRule())
@logger_decorator
async def chat_enter_wrapper(message: Message):
    db = Database.get_current()
    model = None
    for chat_enter_model in db.add_to_friends_on_chat_enter:
        if chat_enter_model.peer_id == message.peer_id:
            model = chat_enter_model
    try:
        await user.api.friends.add(user_id=message.action.member_id)
    except:
        pass
    return model.hello_text


@user.on.chat_message(FromMe(), text=[
    "<prefix:service_prefix> +дб",
    "<prefix:service_prefix> +дбт <hello_text>"
])
@logger_decorator
async def add_chat_enter_model_wrapper(message: Message, hello_text: Optional[str] = None, **kwargs):
    db = Database.get_current()
    for i in range(len(db.add_to_friends_on_chat_enter)):
        if db.add_to_friends_on_chat_enter[i].peer_id == message.peer_id:
            db.add_to_friends_on_chat_enter[i].hello_text = hello_text
            db.save()
            await edit_message(
                message,
                "Текст приветствия добавлен🍃"
            )
            return
    db.add_to_friends_on_chat_enter.append(
        ChatEnterModel(dict(peer_id=message.peer_id, hello_text=hello_text))
    )
    db.save()
    await edit_message(
        message,
        "Добавление новых участников в чате в друзья теперь активно🕊️"
    )
    return


@user.on.chat_message(FromMe(), text=[
    "<prefix:service_prefix> -дб",
])
@logger_decorator
async def add_chat_enter_model_wrapper(message: Message, **kwargs):
    db = Database.get_current()
    model = None
    for i in range(len(db.add_to_friends_on_chat_enter)):
        if db.add_to_friends_on_chat_enter[i].peer_id == message.peer_id:
            model = db.add_to_friends_on_chat_enter[i]
    if model is None:
        await edit_message(
            message,
            "Текст добавления не настроен☘️"
        )
        return
    db.add_to_friends_on_chat_enter.remove(model)
    db.save()
    await edit_message(
        message,
        "Добавление в друзья новых пользователей теперь не активно🕊️"
    )
    return
