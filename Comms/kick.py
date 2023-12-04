import bot
from discord import option
import discord
import init

client = bot.client


def setup(client):
    @client.slash_command(name="kick", description="Kicks a member")
    @discord.default_permissions(kick_members=True)
    @option("member", description="The member to kick")
    @option(
        "reason", description="The reason for the kick", default="Reason not specified"
    )
    async def kick(
        ctx,
        member: discord.Member,
        reason: str,
    ):
        """
        Kicks a member from the server. This will only kick members with higher or equal role. If you are a moderator the reason is ignored

        @param ctx - discord. Message object representing the command
        @param member - discord. Member object representing the member to kick
        @param reason - string explaining why the member is being kick

        Usage: ^kick <member> <reason>
        """
        if member.top_role >= ctx.author.top_role:
            await ctx.respond(
                f"Sorry {ctx.author.mention}, you can't kick someone with higher or equal role.",
                ephemeral=True,
            )
        elif ctx.guild.get_role(init.staff_role_id) in member.roles:
            await ctx.respond(
                f"Sorry {ctx.author.mention}, I can't kick a Staff member. Please do it manually.",
                ephemeral=True,
            )
        else:
            try:
                await member.kick(reason="None Specified" if reason == None else reason)
            except:
                await ctx.respond("Member does not exist.")
                return
            try:
                await member.send(
                    f"You have been kicked from {ctx.guild.name} for {reason}"
                )
            except:
                pass
            finally:
                await ctx.respond(
                    embed=discord.Embed(
                        title="Member kicked",
                        description=f"{member.mention} has been banned from the server for reason: {reason}.",
                    )
                )
