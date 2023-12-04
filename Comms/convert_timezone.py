import bot
import pytz
import datetime
from discord import option

client = bot.client


def setup(client):
    @client.slash_command(name="convert_timezone", description="Converts timezones")
    @option("time", description="The time to convert")
    @option("from_timezone", description="The timezone to convert from")
    @option("to_timezone", description="The timezone to convert to")
    async def convert_timezone(time_str: str, from_tz: str, to_tz: str):
        # # Parse the time string into a datetime object
        # time_obj = datetime.strptime(time_str, "%I:%M %p")

        # # Set the timezone of the datetime object to the source timezone
        # from_timezone = pytz.timezone(from_tz)
        # time_obj = from_timezone.localize(time_obj)

        # # Convert the datetime object to the target timezone
        # to_timezone = pytz.timezone(to_tz)
        # converted_time = time_obj.astimezone(to_timezone)

        # # Format the converted time as a string
        # return converted_time.strftime("%I:%M %p")
        await client.respond(
            "This command is currently being reworked.", ephemeral=True
        )
