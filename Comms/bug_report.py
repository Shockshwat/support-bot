import bot
import random
from discord import option
import discord
import init

client = bot.client


def setup(client):
    @client.slash_command(
        name="bug_report", description="Report a bug to the developers"
    )
    @option("description", description="The bug to report")
    @option("expected behavior", description="The expected behavior of the bot")
    @option("actual behavior", description="The actual behavior of the bot")
    async def bug_report(
        ctx, description: str, expected_behavior: str, actual_behavior: str
    ):
        """
        Report a bug to the developers.
        """

        # Respond to user
        await ctx.respond(
            "Please make an issue [here](https://github.com/Shockshwat/support-bot/issues)",
            ephemeral=True,
        )
