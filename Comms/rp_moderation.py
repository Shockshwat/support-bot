import discord
import bot
from discord import option
import aiosqlite as sqlite3
import init

client = bot.client


def setup(client):
    @client.slash_command(
        name="rp_add", description="Adds a specified amount of RP to a user"
    )
    @discord.default_permissions(kick_members=True)
    @option("member", description="The member to add RP to")
    @option("amount", description="The amount of RP to add", min_value=1)
    async def RP_add(ctx, member: discord.Member, amount: int):
        """
        Adds a specified amount of RP to a user

        Usage: ^RP_add @user <amount>
        """
        if member is None:
            await ctx.respond("Please specify a user to add RP to.", ephemeral=True)
            return
        conn = await sqlite3.connect("Data/RP.db")
        c = await conn.cursor()
        await c.execute("SELECT RP_received FROM RP WHERE id = ?", (member.id,))
        result = await c.fetchone()
        if result is None:
            await c.execute(
                "INSERT INTO RP (id, RP_given, RP_received) VALUES (?, ?, ?)",
                (member.id, 1, amount),
            )
            member_rp_received = amount
        else:
            member_rp_received = result[0] + amount
            await c.execute(
                "UPDATE RP SET RP_received = ? WHERE id = ?",
                (member_rp_received, member.id),
            )
        await conn.commit()
        await ctx.respond(
            f"{ctx.author.mention} has added {amount} RP to {member.mention}. They now have {member_rp_received} RP"
        )
        if member_rp_received >= 50:
            role = ctx.guild.get_role(init.supporter_role_id)
            await member.add_roles(role)
            await ctx.send(
                f"{role.name} Role has been added to {member.mention}. They now have access to the Supporter channel."
            )

        await c.close()
        await conn.close()

    @client.slash_command(
        name="rp_remove", description="Removes a specified amount of RP from a user"
    )
    @discord.default_permissions(kick_members=True)
    @option("member", description="The member to remove RP from")
    @option("amount", description="The amount of RP to remove", min_value=1)
    async def RP_remove(ctx, member: discord.Member, amount: int):
        """
        Removes a specified amount of RP from a user

        Usage: ^RP_remove @user <amount>
        """
        conn = await sqlite3.connect("Data/RP.db")
        c = await conn.cursor()
        await c.execute("SELECT RP_received FROM RP WHERE id = ?", (member.id,))
        result = await c.fetchone()
        if result is None or result[0] < amount:
            await ctx.respond(
                "The user does not have enough RP to remove.", ephemeral=True
            )
            return
        member_rp_received = result[0] - amount
        await c.execute(
            "UPDATE RP SET RP_received = ? WHERE id = ?",
            (member_rp_received, member.id),
        )
        await conn.commit()
        await ctx.respond(
            f"{ctx.author.mention} has removed {amount} RP from {member.mention}. They now have {member_rp_received} RP"
        )
        if result[0] >= 50 and member_rp_received <= 50:
            role = ctx.guild.get_role(init.supporter_role_id)
            await member.remove_roles(role)
            await ctx.send(f"{role.name} Role has been removed from{member.mention}.")

        await c.close()
        await conn.close()
