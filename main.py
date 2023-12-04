import Comms.command as command, register, bot, init, discord, bot
import Comms.rp as rp

# import slash_commands
client = bot.client
command.init_matcher()

register.register()


@client.event
async def on_connect():
    if not rp.reset_rp.is_running():
        await rp.reset_rp.start()


@client.event
async def on_ready():
    await client.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="You")
    )
    print("Bot is ready.")


if __name__ == "__main__":
    client.run(init.Token)
