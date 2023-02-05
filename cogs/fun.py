""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 5.5.0
"""

import random

import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks


class Fun(commands.Cog, name="fun"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="randomfact",
        description="Get a random fact.",
        aliases=["rf"]
    )
    @checks.not_blacklisted()
    async def randomfact(self, context: Context) -> None:
        """
        Get a random fact.

        :param context: The hybrid command context.
        """
        # This will prevent your bot from stopping everything when doing a web request - see: https://discordpy.readthedocs.io/en/stable/faq.html#how-do-i-make-a-web-request
        async with aiohttp.ClientSession() as session:
            async with session.get("https://uselessfacts.jsph.pl/random.json?language=en") as request:
                if request.status == 200:
                    data = await request.json()
                    embed = discord.Embed(
                        description=data["text"],
                        color=0xD75BF4
                    )
                else:
                    embed = discord.Embed(
                        title="Error!",
                        description="There is something wrong with the API, please try again later",
                        color=0xE02B2B
                    )
                await context.send(embed=embed)

    @commands.hybrid_command(
        name="coinflip",
        description="Make a coin flip.",
        aliases=["cf"]
    )
    @checks.not_blacklisted()
    async def coinflip(self, context: Context) -> None:
        """
        Make a coin flip.

        :param context: The hybrid command context.
        """
        result = random.choice(["heads", "tails"])
        coin = "<a:coin1:959392316710338630>"
        embed = discord.Embed(
                description=f"{coin} **{context.author.name}** chose **{result}**! {coin}",
                color=0x9C84EF
            )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="rock_paper_scissors",
        description="Play the rock paper scissors game.",
        aliases=["rps"]
    )
    @checks.not_blacklisted()
    async def rock_paper_scissors(self, context: Context) -> None:
        """
        Play the rock paper scissors game.

        :param context: The hybrid command context.
        """
        choices = {"Rock": [":rock:", 0xFFFFFF], "Paper":[":roll_of_paper:", 0xC4C3D0], "Scissors":[":scissors:", 0xFB4D46]}
        result = random.choice([x for x in choices])
        embed = discord.Embed(
                description=f" **{choices[result][0]} {context.author.name}** chose **{result}**! {choices[result][0]}",
                color=choices[result][1]
            )
        await context.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Fun(bot))
