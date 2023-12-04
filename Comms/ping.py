import bot

client = bot.client


def setup(client):
    @client.slash_command(name="ping", description="Shows the bot's latency")
    async def ping(ctx):
        """
        Shows the bot's ping.

        @param ctx - discord. Message with information about the command
        """
        await ctx.respond(f"Pong! {round(client.latency * 1000)}ms")
