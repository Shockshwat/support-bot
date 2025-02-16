# sus easter egg
import bot
from discord.ext import commands

client = bot.client


class EasterEggCommand(commands.Cog):
    def __init__(self, client):
        self.client = client

    @client.slash_command(name="egg", description="sends an egg")
    async def egg(self, ctx):
        """
        Susses the bot.

        @param ctx - discord. Message with information about the sus
        """
        await ctx.respond(
            "https://cdn.discordapp.com/attachments/968504682387492885/1173287629077368832/84taso.gif?ex=65636841&is=6550f341&hm=e3547af4a4218a868655cfddf5b82c35f0a0d710c4231f4409b10b5a6b561d9e&"
        )


def setup(client):
    if not any(isinstance(c, EasterEggCommand) for c in client.cogs.values()):
        client.add_cog(EasterEggCommand(client))
