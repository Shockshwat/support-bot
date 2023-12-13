import bot
from discord import option
import discord

client = bot.client


def setup(client):
    @client.slash_command(
        name="purge", description="Deletes a specified amount of messages"
    )
    @discord.default_permissions(kick_members=True)
    @option("amount", description="The amount of messages to delete")
    async def purge(
        ctx,
        amount: int,
    ):
        """
        Deletes a specified amount of messages from the channel. This will delete the message from the channel but not the message itself

        @param ctx - discord. Message object representing the command
        @param amount - number of messages to delete

        Usage: ^purge <amount>
        """
        if ctx.guild_id is None:
            await ctx.respond("This command cannot be used in a DM.", ephemeral=True)
            return
        await ctx.respond(
            f"Purged {amount} messages", ephemeral=True
        )  # delete the command message

        # Send a positive number to the server.
        if amount < 1:
            await ctx.respond("Please provide a positive number.")
            return

        await ctx.channel.purge(limit=amount)
