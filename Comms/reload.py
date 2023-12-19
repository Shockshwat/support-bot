import bot
import discord
from discord import option
from discord.ext import commands

client = bot.client


class ReloadCommand(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(name="reload", description="Reloads a command")
    @discord.default_permissions(kick_members=True)
    @option("command", description="The command to reload")
    async def reload(self, ctx, command: str):
        """
        Reloads a command.

        @param ctx - discord. Message with information about the command
        @param command - string. The command to reload
        """
        if ctx.guild_id is None:
            await ctx.respond("This command cannot be used in a DM.", ephemeral=True)
            return
        try:
            client.reload_extension(f"Comms.{command}")
            await ctx.respond(f"Reloaded {command}.", ephemeral=True)
        except discord.ExtensionNotLoaded:
            await ctx.respond(f"Could not reload {command}.", ephemeral=True)


def setup(client):
    if not any(isinstance(c, ReloadCommand) for c in client.cogs.values()):
        client.add_cog(ReloadCommand(client))
