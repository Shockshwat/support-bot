import bot

client = bot.client
from discord import Embed
from discord import option
from currency_converter import CurrencyConverter


def setup(client):
    @client.slash_command(
        name="convert",
        description="Converts a given amount from one currency to another",
    )
    @option("amount", description="The amount to convert")
    @option("from_currency", description="The currency to convert from")
    @option("to_currency", description="The currency to convert to")
    async def convert(ctx, amount: float, from_currency: str, to_currency: str):
        """
         Converts a given amount from one currency to another. This is useful for converting money from one currency to another.

        * @param ctx - discord. Context object containing the user's request
        * @param amount - amount in the currency to convert from one currency to another
        * @param from_currency - name of the currency you want to convert from
        * @param str
        * @param to_currency

        Usage: ^convert <amount> <from_currency> to <to_currency>
        """
        c = CurrencyConverter()
        try:
            result = "{:,.2f}".format(
                int(c.convert(amount, from_currency.upper(), to_currency.upper()))
            )
            amount = "{:,}".format(amount)
            await ctx.respond(
                f"{amount} {from_currency.upper()} is equal to {result} {to_currency.upper()}"
            )
        except Exception as e:
            print(e)
            await ctx.respond(
                f"Invalid currency: {from_currency.upper()} or {to_currency.upper()}",
                ephemeral=True,
            )
