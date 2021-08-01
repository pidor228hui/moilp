from vkbottle.rule import FromMe
from vkbottle.user import Blueprint, Message

from logger import logger_decorator
from objects import Database
from utils import edit_message

user = Blueprint(
    name='prefixes_blueprint'
)


def show_self_prefixes(database: Database) -> str:
    index = 1
    message = 'Префиксы для сигнала себе:\n'
    for prefix in database.self_prefixes:
        message += f'{index}. {prefix}\n'
        index += 1
    return message


def show_duty_prefixes(database: Database) -> str:
    index = 1
    message = 'Префиксы для сигнала Дежурному:\n'
    for prefix in database.duty_prefixes:
        message += f'{index}. {prefix}\n'
        index += 1
    return message


def add_self_prefix(database: Database, prefix: str) -> None:
    database.self_prefixes.append(prefix)
    database.save()


def add_duty_prefix(database: Database, prefix: str) -> None:
    database.duty_prefixes.append(prefix)
    database.save()


def remove_self_prefix(database: Database, prefix: str) -> None:
    database.self_prefixes.remove(prefix)
    database.save()


def remove_duty_prefix(database: Database, prefix: str) -> None:
    database.duty_prefixes.remove(prefix)
    database.save()


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> префиксы свои")
@logger_decorator
async def show_self_prefixes_wrapper(message: Message, **kwargs):
    db = Database.get_current()
    await edit_message(
        message,
        show_self_prefixes(db)
    )


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> префиксы дежурный")
@logger_decorator
async def show_duty_prefixes_wrapper(message: Message, **kwargs):
    db = Database.get_current()
    await edit_message(
        message,
        show_duty_prefixes(db)
    )


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> +префикс свой <new_prefix>")
@logger_decorator
async def add_self_prefix_wrapper(message: Message, new_prefix: str, **kwargs):
    db = Database.get_current()
    new_prefix = new_prefix.replace(' ', '')
    if new_prefix in db.self_prefixes:
        await edit_message(
            message,
            f'⚠ Префикс <<{new_prefix}>> уже существует'
        )
        return
    add_self_prefix(db, new_prefix)
    await edit_message(
        message,
        f'✅ Новый префикс <<{new_prefix}>> создан'
    )


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> +префикс дежурный <new_prefix>")
@logger_decorator
async def add_duty_prefix_wrapper(message: Message, new_prefix: str, **kwargs):
    db = Database.get_current()
    new_prefix = new_prefix.replace(' ', '')
    if new_prefix in db.duty_prefixes:
        await edit_message(
            message,
            f'⚠ Префикс <<{new_prefix}>> уже существует'
        )
        return
    add_duty_prefix(db, new_prefix)
    await edit_message(
        message,
        f'✅ Новый префикс <<{new_prefix}>> создан'
    )


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> -префикс свой <old_prefix>")
@logger_decorator
async def remove_self_prefix_wrapper(message: Message, old_prefix: str, **kwargs):
    db = Database.get_current()
    old_prefix = old_prefix.replace(' ', '')
    if old_prefix not in db.self_prefixes:
        await edit_message(
            message,
            f'⚠ Префикса <<{old_prefix}>> не существует'
        )
        return
    remove_self_prefix(db, old_prefix)
    await edit_message(
        message,
        f'✅ Префикс <<{old_prefix}>> удален'
    )


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> -префикс дежурный <old_prefix>")
@logger_decorator
async def remove_duty_prefix_wrapper(message: Message, old_prefix: str, **kwargs):
    db = Database.get_current()
    old_prefix = old_prefix.replace(' ', '')
    if old_prefix not in db.duty_prefixes:
        await edit_message(
            message,
            f'⚠ Префикса <<{old_prefix}>> не существует'
        )
        return
    remove_duty_prefix(db, old_prefix)
    await edit_message(
        message,
        f'✅ Префикс <<{old_prefix}>> удален'
    )
