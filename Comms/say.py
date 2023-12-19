import discord
import bot
from discord import option
from discord.ext import commands

client = bot.client


class SayCommand(commands.Cog):
    def __init__(self, client):
        self.client = client

    say = discord.SlashCommandGroup("say", "Says a message")

    @say.command(name="channel", description="Says a message")
    @discord.default_permissions(kick_members=True)
    @option("channel", description="The channel to send the message to")
    @option("message", description="The message to send")
    async def sendmsgchannel(
        self,
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
        if ctx.guild_id is None:
            await ctx.respond("This command cannot be used in a DM.", ephemeral=True)
            return
        await channel.send(msg)
        await ctx.respond("Message sent.", ephemeral=True)

    @say.command(name="user", description="Says a message")
    @discord.default_permissions(kick_members=True)
    @option("user", description="The user to send the message to")
    @option("message", description="The message to send")
    async def sendmsguser(
        self,
        ctx,
        user: discord.Member,
        msg: str,
    ):
        """
        Sends a message to the specified user.

        @param ctx - discord. Message with information about the command
        @param user - discord. User to send the message to
        @param msg - string. Message to send
        """
        if ctx.guild_id is None:
            await ctx.respond("This command cannot be used in a DM.", ephemeral=True)
            return
        await user.send(msg)
        await ctx.respond("Message sent.", ephemeral=True)


def setup(client):
    client.add_cog(SayCommand(client))
