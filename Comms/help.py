import bot
import discord
from discord import option
import init

client = bot.client

hidden = [
    ("info tell", "Sends the information about the topic."),
    ("info list", "Lists all available topics."),
    ("rp check", "RP of a user, if no user is specified, it will show your RP."),
    ("rp give", "Gives a specified amount of RP to a user."),
    ("rp leaderboard", "Shows the RP leaderboard."),
]
hidden_staff = [
    ("rp remove", "Removes RP from a user."),
    ("rp add", "Adds RP to a user."),
    ("info remove", "Removes a topic from the information system."),
]
hidden_support = [
    ("info add", "Adds a topic to the information system."),
]


async def helpembed(support=False, staff=False, for_code=False):
    if staff:
        support = True
    commands = [
        ("help", "Shows this message."),
        (
            "report",
            "Reports a user to the mods. Usage: `/report <@user> [reason]`",
        ),
        (
            "request_feature",
            "Request a feature for the bot. Usage: `/request_feature <feature>`",
        ),
        (
            "convert",
            "Converts a given amount from one currency to another. Usage: `^convert <amount> <from_currency> <to_currency>`",
        ),
        ("ping", "Returns the bot's latency. Usage: `/ping`"),
        (
            "info",
            f"Sub commands: `list`, `tell`{' ,`add`' if support or staff else ''}{' ,`remove`' if staff else ''}. Usage: `/info [subcommand] <topic>`",
        ),
        (
            "rp",
            f"Sub commands: `check`, `give`, `leaderboard`{' ,`add`' if support else ''}{' ,`remove`' if staff else ''}. Usage: `/rp [subcommand] <@user> [amount]`",
        ),
        (
            "bug_report",
            "Report a bug. Usage: `/bug_report <bug_description> <expected_behaviour> <actual_behaviour>`",
        ),
    ]
    if support:
        commands.append(
            (
                "close",
                "Closes a support thread (locks the channel and deletes the post after 1h). Usage: `/close`",
            )
        )
    if staff:
        commands.extend(
            [
                ("warn", "Warns a user. Usage: `/warn <@user> <reason>`"),
                ("kick", "Kicks a user. Usage: `/kick <@user> [reason]`"),
                ("ban", "Bans a user. Usage: `/ban <@user> [reason]`"),
                (
                    "get_warns",
                    "Returns a list of warns for a given user. Usage: `/get_warns <user>`",
                ),
                (
                    "purge",
                    "Purges a given amount of messages. Usage: `/purge <amount>`",
                ),
                (
                    "say",
                    "Sends a message to a channel. Usage: `/say <channel> <message>`",
                ),
                (
                    "rp_add, rp_remove",
                    "RP moderation commands. Usage: `/rp_<subcommand> <username> <int>`",
                ),
            ]
        )

    help_embed = discord.Embed(
        title="Here are the available commands:",
        description="Prefix for all commands is `/`",
        color=discord.Color.blue(),
    )
    for name, value in commands:
        help_embed.add_field(name=name, value=value, inline=False)
    if for_code:
        return commands

    return help_embed


def setup(client):
    @client.slash_command(name="help", description="Shows help")
    @option(
        name="Command",
        description="Shows documentation for a specific command",
        required=False,
    )
    async def help(ctx, command: str = None):
        """
        Shows help.

        @param ctx - discord. Message with information about the command
        """
        # Make this function accept an argument which takes a command name and returns the help embed for that command
        if command is not None:
            if ctx.guild.get_role(init.staff_role_id) in ctx.author.roles:
                commands = await helpembed(staff=True, for_code=True)
            elif ctx.guild.get_role(init.supporter_role_id) in ctx.author.roles:
                commands = await helpembed(support=True, for_code=True)
            else:
                commands = await helpembed(for_code=True)

            for i in commands:
                if i[0] == command.strip().lower():
                    await ctx.respond(
                        embed=discord.Embed(
                            title=command, description=i[1], color=discord.Color.blue()
                        )
                    )
                    return
            for i in hidden:
                if i[0] == command.strip().lower():
                    await ctx.respond(
                        embed=discord.Embed(
                            title=command, description=i[1], color=discord.Color.blue()
                        )
                    )
                    return
            if ctx.guild.get_role(init.staff_role_id) in ctx.author.roles:
                for i in hidden_staff:
                    if i[0] == command.strip().lower():
                        await ctx.respond(
                            embed=discord.Embed(
                                title=command,
                                description=i[1],
                                color=discord.Color.blue(),
                            )
                        )
                        return
            if (
                ctx.guild.get_role(init.supporter_role_id) in ctx.author.roles
                or ctx.guild.get_role(init.staff_role_id) in ctx.author.roles
            ):
                for i in hidden_support:
                    if i[0] == command.strip().lower():
                        await ctx.respond(
                            embed=discord.Embed(
                                title=command,
                                description=i[1],
                                color=discord.Color.blue(),
                            )
                        )
                        return
            await ctx.respond("Command not found!", ephemeral=True)
        else:
            if ctx.guild.get_role(init.staff_role_id) in ctx.author.roles:
                await ctx.respond(embed=await helpembed(support=True, staff=True))
                return
            if ctx.guild.get_role(init.supporter_role_id) in ctx.author.roles:
                await ctx.respond(embed=await helpembed(support=True))
                return
            else:
                await ctx.respond(embed=await helpembed())
