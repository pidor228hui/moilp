from vkbottle.rule import ChatActionRule, FromMe
from vkbottle.user import Blueprint, Message

from logger import logger_decorator
from objects import Database
from utils import edit_message

user = Blueprint(
    name='auto_exit_from_chat_blueprint'
)


async def set_auto_exit(
        db: Database,
        auto_exit: bool = None,
        delete_chat: bool = None,
        black_list: bool = None
):
    db.auto_exit_from_chat = auto_exit if auto_exit is not None else db.auto_exit_from_chat
    db.auto_exit_from_chat_delete_chat = delete_chat if delete_chat is not None else db.auto_exit_from_chat_delete_chat
    db.auto_exit_from_chat_add_to_black_list = (
        black_list if black_list is not None else db.auto_exit_from_chat_add_to_black_list
    )
    db.save()


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> +ав")
@logger_decorator
async def auto_exit_setting_on_exit_wrapper(message: Message, **kwargs):
    db = Database.get_current()
    await set_auto_exit(db, True, False)
    await edit_message(message, "Включил автовыход из бесед😼")


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> -ав")
@logger_decorator
async def auto_exit_setting_on_exit_wrapper(message: Message, **kwargs):
    db = Database.get_current()
    await set_auto_exit(db, False, False)
    await edit_message(message, "Выключил автовыход из бесед😼")


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> ав +чс")
@logger_decorator
async def auto_exit_setting_on_exit_wrapper(message: Message, **kwargs):
    db = Database.get_current()
    await set_auto_exit(db, black_list=True)
    await edit_message(message, "Автовыход с бесед с добавлением в ЧС пригласившего включен😽")


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> ав -чс")
@logger_decorator
async def auto_exit_setting_on_exit_wrapper(message: Message, **kwargs):
    db = Database.get_current()
    await set_auto_exit(db, black_list=False)
    await edit_message(message, "Автовыход с бесед с добавлением в ЧС пригласившего выключен😽")


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> ав +уд")
@logger_decorator
async def auto_exit_setting_on_exit_wrapper(message: Message, **kwargs):
    db = Database.get_current()
    await set_auto_exit(db, delete_chat=True)
    await edit_message(message, "Теперь я выхожу с беседы в которую меня пригласили, и удаляю чат🙈")


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> ав -уд")
@logger_decorator
async def auto_exit_setting_on_exit_wrapper(message: Message, **kwargs):
    db = Database.get_current()
    await set_auto_exit(db, delete_chat=False)
    await edit_message(message, "Автовыход с удалением чата выключен🙉")


@user.on.chat_message(ChatActionRule("chat_invite_user"))
@user.on.chat_message(ChatActionRule("chat_invite_user_by_link"))
@logger_decorator
async def to_chat_wrapper(message: Message):
    if message.action.member_id == await message.api.user_id:
        db = Database.get_current()
        if message.action.type == "chat_invite_user":
            if db.disable_notifications:
                await user.api.account.set_silence_mode(
                    time=-1,
                    peer_id=message.peer_id,
                    sound=0
                )
            if db.auto_exit_from_chat:
                await message.api.messages.remove_chat_user(chat_id=message.chat_id, member_id=await message.api.user_id)
            if db.auto_exit_from_chat_delete_chat:
                await message.api.messages.delete_conversation(peer_id=message.peer_id)
            if db.auto_exit_from_chat_add_to_black_list:
                await message.api.account.ban(owner_id=message.from_id)
        else:
            if db.disable_notifications:
                await user.api.account.set_silence_mode(
                    time=-1,
                    peer_id=message.peer_id,
                    sound=0
                )
