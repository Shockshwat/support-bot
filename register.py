import bot, events
from cogwatch import Watcher

client = bot.client


def register():
    commands = [
        "Comms.warn",
        "Comms.info",
        "Comms.kick",
        "Comms.purge",
        "Comms.ban",
        "Comms.help",
        "Comms.report",
        "Comms.feature_request",
        "Comms.get_warns",
        "Comms.convert",
        "Comms.rp",
        "Comms.convert_timezone",
        "Comms.rp_moderation",
        "Comms.say",
        "Comms.ping",
        "Comms.easter_egg",
        "Comms.bug_report",
        "Comms.close",
        "Comms.reload",
    ]
    for cmd in commands:
        client.load_extension(cmd)
    client.event(events.on_member_join)
    client.event(events.on_message)
    client.event(events.on_slash_command_error)
    client.event(events.on_thread_create)

