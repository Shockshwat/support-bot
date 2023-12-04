import discord
from discord import option
import bot
import init

client = bot.client


def setup(client):
    @client.slash_command(name="ban", description="Bans a member")
    @discord.default_permissions(ban_members=True)
    @option("member", description="The member to ban")
    @option(
        "reason", description="The reason for the ban", default="Reason not specified"
    )
    async def ban(
        ctx,
        member: discord.Member,
        reason: str,
    ):
        """
        Bans a member from the server. This will remove the member from the server but if the member has higher role it will be banned as well

        @param ctx - discord. Message object representing the command
        @param member - discord. Member object representing the user to ban
        @param reason - string explaining why the user is banned

        Usage: ^ban @user reason
        """
        if ctx.author == member:
            await ctx.respond("You can't ban yourself, dummy", ephemeral=True)
        elif member.top_role >= ctx.author.top_role:
            await ctx.respond(
                f"Sorry {ctx.author.mention}, you can't ban someone with higher or equal role.",
                ephemeral=True,
            )
        elif init.staff_role in [role.name for role in member.roles]:
            await ctx.respond(
                f"Sorry {ctx.author.mention}, I can't ban a Staff member. Please do it manually.",
                ephemeral=True,
            )

        else:
            try:
                await member.ban(reason="None Specified" if reason == None else reason)
            except:
                await ctx.respond("Member does not exist.")
                return
            try:
                await member.send(
                    f"You have been banned from {ctx.guild.name} for {reason}"
                )
            except:
                pass
            finally:
                await ctx.respond(
                    embed=discord.Embed(
                        title="Member Banned",
                        description=f"{member.mention} has been banned from the server for reason: {reason}.",
                    )
                )
