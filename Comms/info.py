import bot
from discord import option
import Comms.information as information
import discord
import random
import time
import init

client = bot.client


def setup(client):
    info = client.create_group("info", "Information Commands")

    @info.command(name="tell", description="Sends the information about the topic")
    @option("topic", description="The topic to get information about")
    async def tell(ctx, topic: str):
        for x in information.get_data()["name"]:
            if topic.lower() == x:
                await ctx.respond(
                    information.get_data()["values"][
                        information.get_data()["name"].index(x)
                    ],
                )

                return
        await ctx.respond(
            "Topic not found! Use `/info list` to list available topics. ",
            ephemeral=True,
        )
        return

    @client.slash_command(
        name="add", description="Adds a topic to the information system"
    )
    @option("topic", description="The topic to add")
    @option("file", description="The content to add")
    @discord.default_permissions(create_public_threads=True)
    async def info_add(ctx, topic: str, file: discord.Attachment):
        if ctx.guild_id is None:
            await ctx.respond("This command cannot be used in a DM.", ephemeral=True)
            return
        if not file.filename.endswith(".txt"):
            await ctx.send("Invalid file type. Please upload a text file.")
        if (
            ctx.guild.get_role(init.supporter_role_id) not in ctx.author.roles
            and ctx.guild.get_role(init.staff_role_id) not in ctx.author.roles
        ):
            await ctx.respond(
                "You do not have permission to use this command!", ephemeral=True
            )

        topic = topic.strip().lower()

        if topic in information.get_data()["name"]:
            await ctx.respond("This topic already exists!", ephemeral=True)
            return
        elif topic == "list" or topic == "add":
            await ctx.respond("Forbidden topic name!", ephemeral=True)
            return

        # Read the content of the file
        content = await file.read()
        content = content.decode()
        if len(content) > 2000:
            await ctx.respond(
                "The content exceeds the maximum limit of 2000 characters!",
                ephemeral=True,
            )
            return
        await ctx.respond("Please wait, Processing the file system for new data...")
        time.sleep(random.randint(7, 15))

        information.add_data(topic, content)
        await ctx.respond("Topic added!")
        return

    @client.slash_command(
        name="remove", description="Removes a topic from the information system"
    )
    @option("topic", description="The topic to remove")
    @discord.default_permissions(kick_members=True)
    async def info_remove(ctx, topic: str):
        if ctx.guild.get_role(init.staff_role_id) not in ctx.author.roles:
            await ctx.respond(
                "You do not have permission to use this command!", ephemeral=True
            )
            return
        topic = topic.strip().lower()
        if topic not in information.get_data()["name"]:
            await ctx.respond("This topic does not exist!", ephemeral=True)
            return
        elif topic == "list" or topic == "add":
            await ctx.respond("Forbidden topic name!", ephemeral=True)
            return

        information.remove_data(topic)
        await ctx.respond(f"Topic {topic} removed!")
        return

    @info.command(name="list", description="Lists all topics")
    async def info_list(ctx):
        await ctx.respond(
            "Available topics are: "
            + ", ".join([name.capitalize() for name in information.get_data()["name"]]),
            ephemeral=True,
        )
        return
