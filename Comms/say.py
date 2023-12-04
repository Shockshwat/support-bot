import discord
import bot
from discord import option

client = bot.client


def setup(client):
    @client.slash_command(name="say", description="Says a message")
    @discord.default_permissions(kick_members=True)
    @option("channel", description="The channel to send the message to")
    @option("message", description="The message to send")
    async def sendmsg(
        ctx,
        channel: discord.TextChannel,
        msg: str,
    ):
        """
        Sends a message to the specified channel.

        @param ctx - discord. Message with information about the command
        @param channel - discord. Channel to send the message to
        @param msg - string. Message to send
        """
        await channel.send(msg)
        await ctx.respond("Message sent.", ephemeral=True)
