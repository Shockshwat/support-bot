from discord.ext import commands
import bot
import asyncio
import init

client = bot.client


class CloseCommand(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(name="close", description="Closes a support thread")
    async def close(self, ctx):
        """
        Closes the thread. This will be resolved to the moderator if you wish to reopen it. You can only close public threads

        @param ctx - discord. Context object

        Usage: ^close
        """
        # This thread is now closed.
        if ctx.channel.parent.name == "support":
            # solution_channel = client.get_channel(1099385787654619197)
            if (
                ctx.guild.get_role(init.supporter_role_id) in ctx.author.roles
                or ctx.guild.get_role(init.staff_role_id) in ctx.author.roles
                or ctx.author == ctx.channel.owner
            ):
                await ctx.respond(
                    "This thread is now closed. Please contact a moderator if you wish to reopen it."
                )
                await ctx.channel.edit(
                    locked=True,
                    archived=True,
                )

                # await ctx.channel.add_tags(Resolved)

                await asyncio.sleep(3600)
                await ctx.channel.delete()
        else:
            await ctx.respond("Sorry this command can only be used in help threads.")


def setup(client):
    client.add_cog(CloseCommand(client))
