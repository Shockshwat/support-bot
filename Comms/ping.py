import bot
from discord.ext import commands

client = bot.client


class PingCommand(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(name="ping", description="Shows the bot's latency")
    async def ping(self, ctx):
        """
        Shows the bot's ping.

        @param ctx - discord. Message with information about the command
        """
        await ctx.respond(f"Pong! {round(client.latency * 1000)}ms")


def setup(client):
    client.add_cog(PingCommand(client))
