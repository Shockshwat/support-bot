import discord
import bot
from discord import option
from discord.ext import commands

client = bot.client


class GetWarnsCommand(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(name="get_warns", description="Gets warns for a user")
    @discord.default_permissions(kick_members=True)
    @option("member", description="The member to get warns for")
    async def get_warns(self, ctx, member: discord.Member):
        """
        Gets warns for a user. This will return a list of tuples ( reason id ). If there are no warnings for the user the function will return an empty list

        @param ctx - discord. Context The context of the command
        @param member - discord. Member The member to get warnings

        Usage: ^get_warns <member>
        """

        # Get warns from database
        import aiosqlite
        from datetime import datetime

        if ctx.guild_id is None:
            await ctx.respond("This command cannot be used in a DM.", ephemeral=True)
            return

        conn = await aiosqlite.connect("Data/warns.db")
        c = await conn.cursor()
        await c.execute("SELECT * FROM warnings WHERE userid = ?", (member.id,))
        result = await c.fetchall()
        await c.close()
        await conn.close()

        # If there are no warnings for the user return an empty list
        if len(result) == 0:
            await ctx.respond(f"{member.mention} has no warnings.", ephemeral=True)
            return

        # Create embed
        embed = discord.Embed(
            title=f"Warnings for User {member.name}",
            description=f"Warnings for {member.mention} are listed below.",
            color=discord.Color.red(),
        )

        # Add warnings to embed
        for warning in result:
            warn_date = datetime.strptime(warning[2], "%Y-%m-%d").strftime("%d-%m-%Y")
            embed.add_field(
                name=f"Warned on {warn_date}",
                value=warning[3],
                inline=False,
            )

        await ctx.respond(embed=embed)


def setup(client):
    client.add_cog(GetWarnsCommand(client))
