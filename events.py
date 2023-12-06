from discord.ext import commands
import init
from Comms.command import matcher
import bot
import discord
import random
import asyncio
import traceback

client = bot.client


@client.event
async def on_member_join(member):
    """
    Called when a member joins the server. This will send a message to the user and create a DM to the new member.

    @param member - The member that joined the server. It should have a name
    """
    channel_id = init.general_channel
    channel = client.get_channel(channel_id)
    # Send a message to the server.
    if channel is not None:
        message = f"Welcome to the server, {member.mention}!"
        await channel.send(message)

    # Send a DM to the new member
    try:
        dm_channel = await member.create_dm()
        await dm_channel.send(
            f"Welcome to the server, {member.name}! Use <#{init.support_channel}> for support, read the server rules and enjoy your stay."
        )
    except:
        pass


@client.event
async def on_slash_command_error(ctx, error):
    """
    Called when an error occurs while executing a slash command.

    @param ctx - The discord. Context object that the command was executed in.
    @param error - The error that occurred during execution of the command
    """
    # Send an error message to the client.
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(
            content="You are missing one of the required arguments. Here is an empathy Banana for you. :banana:"
        )
    elif isinstance(error, commands.BadArgument):
        await ctx.send(content="Invalid Syntax.")
    elif isinstance(error, commands.CheckFailure):
        await ctx.send(content="Access denied, Are you sudo?")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send(
            content=f"{ctx.invoked_with} is not recognized as an internal or external command, operable program or batch file."
        )
    else:
        await client.get_channel(init.logging_channel).send(error)


@client.event
async def on_message(message):
    """
    Checks if the message is about asking for help and is not in the help channel. if it is not then it redirects the user to the help channel.

    @param message - The message that was received

    @return A boolean indicating if the message was redirected or not based on the regex. This is called by bot
    """
    if message.author == client.user:
        return
    # Check if the message is in the general channel
    if message.channel.id == init.general_channel:
        doc = init.nlp(message.content.lower())
        matches = matcher(doc)
        if matches:
            # Get the channel to redirect to
            redirect_channel = client.get_channel(init.support_channel)
            # Send a message in the redirect channel
            try:
                await message.author.send(
                    f"Hey {message.author.mention}, please ask for help in {redirect_channel.mention}, If this was a false positive then please contact staff. Here is your message content in case you want to copy paste it in {redirect_channel.mention} : \n ```{message.content}```"
                )

            except:
                await message.channel.send(
                    f"Hey, {message.author.mention} looks like your DMs are closed. I want to inform you that please do not ask for support here. Use {redirect_channel.mention} instead. If this was a false positive then please contact staff",
                    delete_after=10.0,
                )
            await client.get_channel(init.logging_channel).send(
                f"{message.author.mention} was redirected. Message : \n ```{message.content}```"
            )
            await message.delete()

    await client.process_commands(message)


@client.event
async def on_thread_create(thread):
    """
    Called when a thread is created. Basic instructions are given.

    @param thread - The thread that was created as a result of the event
    """
    # check if the thread is in the desired channel

    await thread.add_user(client.user)
    if thread.parent is not None:
        if thread.parent.name == "support":
            threads = random.randint(100000, 999999)
            try:
                await thread.edit(
                    name=f"Issue {threads} | {thread.name}", auto_archive_duration=4320
                )

            except:
                pass
            finally:
                await thread.send(
                    f"Greetings {thread.owner.mention},\n\nWe kindly request that you **refrain from mentioning your issue in <#{init.general_channel}>**, and **avoid creating duplicate threads**. We also request that you **patiently wait for a response within this thread for a duration of one hour**. If there is no response within the aforementioned period, kindly **ping {thread.guild.get_role(init.supporter_role_id).name}**. You may refer to <#{init.faq_channel}> to see if your issue has already been addressed.\n\nThank you in advance for your cooperation. When someone helps you with your issue, please use the command **/rp give <username> <1-10>** to reward them with RP. \n\n**Once your issue has been resolved, please use the command /close to close the thread.**"
                )
