import bot
from discord import option
from discord.ext import commands

client = bot.client


class BugReportCommand(commands.Cog):
    @client.slash_command(
        name="bug_report", description="Report a bug to the developers"
    )
    @option("description", description="The bug to report")
    @option("expected behavior", description="The expected behavior of the bot")
    @option("actual behavior", description="The actual behavior of the bot")
    async def bug_report(
        self, ctx, description: str, expected_behavior: str, actual_behavior: str
    ):
        """
        Report a bug to the developers.
        """

        # Respond to user
        await ctx.respond(
            "Please make an issue [here](https://github.com/Shockshwat/support-bot/issues)",
            ephemeral=True,
        )


def setup(client):
    if not any(isinstance(c, BugReportCommand) for c in client.cogs.values()):
        client.add_cog(BugReportCommand(client))
