import Comms.command as command, register, bot, init, discord, bot
import Comms.rp as rp
from cogwatch import Watcher

# import slash_commands
client = bot.client
command.init_matcher()

register.register()
client.loop.create_task(Watcher(client, path="Comms", preload=False).start())


@client.event
async def on_ready():
    await client.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="You")
    )
    print("Bot is ready.")


if __name__ == "__main__":
    client.run(init.Token)
