import discord
import bot
import aiosqlite as sqlite3
from discord import Embed
from discord import option
from discord.ext import tasks
import init

client = bot.client


def setup(client):
    RP = client.create_group("rp", "RP Commands")

    @RP.command(name="check", description="Checks the RP of a user")
    @option("member", description="The member to check RP for", required=False)
    async def RP_check(ctx, member: discord.Member):
        """
        Adds RP to a user, getting to 10 RP will grant the user Supporters Role

        Usage: ^RP @user
        """
        conn = await sqlite3.connect("Data/RP.db")
        c = await conn.cursor()
        if member is None:
            await c.execute("SELECT RP_received FROM RP WHERE id = ?", (ctx.author.id,))
            result = await c.fetchone()
            if result is None:
                await ctx.respond("You don't have any RP yet.")
            else:
                await ctx.respond(f"You have {result[0]} RP.")
            return
        await c.execute("SELECT RP_received FROM RP WHERE id = ?", (member.id,))
        result = await c.fetchone()
        if result is None:
            await ctx.respond(f"{member.mention} has no RP.")
        else:
            await ctx.respond(f"{member.mention} has {result[0]} RP.")
        await c.close()
        await conn.close()

    @RP.command(name="give", description="Gives a specified amount of RP to a user")
    @option("member", description="The member to give RP to")
    @option("amount", description="The amount of RP to give", min_value=1, max_value=10)
    async def RP_give(ctx, member: discord.Member, amount: int):
        if ctx.author == member:
            await ctx.respond("You can't give yourself RP, dummy", ephemeral=True)
            return
        if amount < 1:
            await ctx.respond("You must give at least 1 RP.", ephemeral=True)
            return
        conn = await sqlite3.connect("Data/RP.db")
        c = await conn.cursor()
        await c.execute("SELECT RP_given FROM RP WHERE id = ?", (ctx.author.id,))
        result = await c.fetchone()
        if result is None:
            await c.execute(
                "INSERT INTO RP (id, RP_given, RP_received) VALUES (?, ?, ?)",
                (ctx.author.id, 10, 0),
            )
            author_rp_given = 10
        else:
            author_rp_given = result[0]
        if author_rp_given < amount:
            await ctx.send("You don't have that much RP to give!")
            return
        await c.execute(
            "UPDATE RP SET RP_given = ? WHERE id = ?",
            (author_rp_given - amount, ctx.author.id),
        )
        await c.execute("SELECT RP_received FROM RP WHERE id = ?", (member.id,))
        result = await c.fetchone()
        if result is None:
            await c.execute(
                "INSERT INTO RP (id, RP_given, RP_received) VALUES (?, ?, ?)",
                (member.id, 0, amount),
            )
            member_rp_received = amount
        else:
            member_rp_received = result[0] + amount
            await c.execute(
                "UPDATE RP SET RP_received = ? WHERE id = ?",
                (member_rp_received, member.id),
            )
        await conn.commit()
        if member_rp_received >= 50:
            role = ctx.guild.get_role(init.supporter_role_id)
            await member.add_roles(role)
            await ctx.send(
                f"{member.mention} has been given the {role.name} role. They now have access to the Supporter channel."
            )
        await ctx.respond(
            f"{ctx.author.mention} has given {member.mention} {amount} RP. They now have {member_rp_received} RP"
        )
        rp_log_channel = ctx.guild.get_channel(init.rp_log_channel_id)
        if rp_log_channel is not None:
            await rp_log_channel.send(
                f"{ctx.author.mention} has given {amount} RP to {member.mention} in {ctx.channel.name}."
            )
        await c.close()
        await conn.close()

    @RP.command(name="leaderboard", description="Shows the RP leaderboard")
    async def RP_leaderboard(ctx):
        """
        Displays an embed with the top 10 people with the most RP.

        Usage: ^RP leaderboard
        """
        conn = await sqlite3.connect("Data/RP.db")
        c = await conn.cursor()
        await c.execute("SELECT id, RP_received FROM RP ORDER BY RP_received DESC")
        results = await c.fetchall()

        embed = Embed(
            title="RP Leaderboard",
            description="Top 10 users with the most RP",
            color=0x00FF00,
        )
        rank = 1
        for id, rp in results:
            member = ctx.guild.get_member(id)
            if member is not None:
                embed.add_field(
                    name=f"{rank}. {member.name} with {rp} RP", value="", inline=False
                )
                rank += 1
            if rank > 10:
                break

        await ctx.respond(embed=embed)
        await c.close()
        await conn.close()


@tasks.loop(hours=24)
async def reset_rp():
    conn = await sqlite3.connect("Data/RP.db")
    c = await conn.cursor()
    await c.execute("UPDATE RP SET RP_given = 10")
    await conn.commit()
    await c.close()
    await conn.close()
