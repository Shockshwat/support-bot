import discord
import bot
from discord import option
import init

client = bot.client


def setup(client):
    @client.slash_command(name="report", description="Reports a user")
    @option("member", description="The member to report")
    @option("reason", description="The reason for the report")
    @option(
        "message", description="The message to report", default="Message not specified"
    )
    async def report(
        ctx,
        member: discord.Member,
        reason: str,
        message: str,
    ):
        """
        Reports a user to the moderators. Reports will be sent to 1029830182187581560 so you don't have to worry about it

        @param ctx - discord. Context The context of the command
        @param member - discord. Member The member that reported the message
        @param reason - str The reason for the report.
        @param message - str The message to report ( can be empty )

        Usage: ^report @user reason message
        """
        report_channel = client.get_channel(init.report_channel_id)
        report_embed = discord.Embed(
            title="Report",
            description=f"{ctx.author.mention} has reported {member.mention} for: {reason}",
            color=discord.Color.red(),
        )
        report_embed.set_author(
            name=f"{ctx.author.name}",
            icon_url=ctx.author.avatar.url,
        )
        report_embed.add_field(
            name="Message",
            value=message,
        )
        await report_channel.send(embed=report_embed)
        await ctx.respond(
            "Thank you for your report, the moderators have been notified.",
            ephemeral=True,
        )
