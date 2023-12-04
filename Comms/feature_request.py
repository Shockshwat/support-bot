from discord import option
import bot
import discord
import init

client = bot.client


def setup(client):
    @client.slash_command(
        name="request_feature", description="Request a feature for the bot"
    )
    @option("feature", description="The feature you want to request")
    async def request_feature(
        ctx,
        feature: str,
    ):
        """
        Request a feature for the bot.
        """
        await ctx.respond(
            "To make a feature request, click [here](https://github.com/Shockshwat/support-bot/issues/)",
            ephemeral=True,
        )
