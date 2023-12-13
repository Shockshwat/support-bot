import discord
import bot
from discord import option

client = bot.client


def setup(client):
    @client.slash_command(name="warn", description="Warns a member")
    @discord.default_permissions(kick_members=True)
    @option("member", description="The member to warn")
    @option(
        "reason",
        description="The reason for the warning",
        default="Reason not specified",
    )
    async def warn(
        ctx,
        member: discord.Member,
        reason=discord.Option(str, name="Reason", required=False),
    ):
        """
        Warns a member and uploads a warning to the spreadsheet. This will be sent to the channel or if the member has higher role warns the user.

        @param ctx - Discord request context with the guild and channel
        @param member - The member to warn. Must be a member of the guild
        @param reason - The reason for the warning

        Usage: ^warn <member> <reason>
        """
        # Send warning message to the channel
        # If member. top_role is greater than or equal role send a warning about someone with higher or equal role.
        if ctx.guild_id is None:
            await ctx.respond("This command cannot be used in a DM.", ephemeral=True)
            return
        if member == discord.User:
            await ctx.respond(
                f"Sorry {ctx.author.mention}, you can't warn someone who is not in the server.",
                ephemeral=True,
            )
            return
        if member.top_role >= ctx.author.top_role:
            await ctx.respond(
                f"Sorry {ctx.author.mention}, you can't warn someone with higher or equal role.",
                ephemeral=True,
            )
            return
        import aiosqlite
        from datetime import datetime

        # Log the warning in the database
        async with aiosqlite.connect("Data/warns.db") as db:
            # Insert the warning
            await db.execute(
                """
                INSERT INTO warnings (username, userid, warn_date, reason)
                VALUES (?, ?, ?, ?)
            """,
                (
                    member.name,
                    member.id,
                    datetime.now().date().isoformat(),
                    reason,
                ),
            )
            await db.commit()
        await ctx.respond(
            embed=discord.Embed(
                title="Warning Issued",
                description=f"{member.mention} has been warned for {reason}",
                color=discord.Color.red(),
            )
        )

        # Send DM to the warned member
        try:
            await member.send(
                f"You've been warned in {ctx.guild.name} for {reason}. Please take note of this warning."
            )
        except:
            await ctx.send(
                f"Failed to send DM to {member.mention}. They may have DMs blocked."
            )
