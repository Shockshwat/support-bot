from discord import option
import bot
from discord.ext import commands

client = bot.client


class FeatureRequestCommand(commands.Cog):
    def __init__(self, client):
        self.client = client

    @client.slash_command(
        name="request_feature", description="Request a feature for the bot"
    )
    async def request_feature(self, ctx):
        """
        Request a feature for the bot.
        """
        await ctx.respond(
            "To make a feature request, click [here](https://github.com/Shockshwat/support-bot/issues/).",
            ephemeral=True,
        )


def setup(client):
    if not any(isinstance(c, FeatureRequestCommand) for c in client.cogs.values()):
        client.add_cog(FeatureRequestCommand(client))
