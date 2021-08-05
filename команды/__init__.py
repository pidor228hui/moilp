from commands import (
    add_to_friends_on_chat_enter,
    aliases,
    aliases_manager,
    auto_exit_from_chat,
    bio_wars,
    delete_messages,
    delete_messages_vks,
    delete_notify,
    disable_notifications,
    duty_signal,
    info,
    members_manager,
    ping,
    prefixes,
    regex_deleter,
    repeat,
    role_play_commands,
    run_eval,
    self_signal,
    set_secret_code,
    sloumo
)

commands_bp = (
    add_to_friends_on_chat_enter.user,
    aliases.user,
    aliases_manager.user,
    auto_exit_from_chat.user,
    bio_wars.user,
    delete_messages.user,
    delete_messages_vks.user,
    delete_notify.user,
    disable_notifications.user,
    duty_signal.user,
    run_eval.user,
    ping.user,
    info.user,
    prefixes.user,
    regex_deleter.user,
    repeat.user,
    role_play_commands.user,
    self_signal.user,
    set_secret_code.user,
    sloumo.user,

    *members_manager.users_bp,
)
