import os
import random

import aiohttp
import discord
import requests
from discord.ext import commands
from discord.ext.commands import Context
from dotenv import load_dotenv

from helpers import checks

load_dotenv()


class Fun(commands.Cog, name="fun"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="randomfact", description="Get a random fact.", aliases=["rf"]
    )
    @checks.not_blacklisted()
    async def randomfact(self, context: Context) -> None:
        """
        Get a random fact.

        :param context: The hybrid command context.
        """
        # This will prevent your bot from stopping everything when doing a web request - see: https://discordpy.readthedocs.io/en/stable/faq.html#how-do-i-make-a-web-request
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://uselessfacts.jsph.pl/random.json?language=en"
            ) as request:
                if request.status == 200:
                    data = await request.json()
                    embed = discord.Embed(description=data["text"], color=0xD75BF4)
                else:
                    embed = discord.Embed(
                        title="Error!",
                        description="There is something wrong with the API, please try again later",
                        color=0xE02B2B,
                    )
                await context.send(embed=embed)

    @commands.hybrid_command(
        name="coinflip", description="Make a coin flip.", aliases=["cf"]
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
            color=0x9C84EF,
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="rock_paper_scissors",
        description="Play the rock paper scissors game.",
        aliases=["rps"],
    )
    @checks.not_blacklisted()
    async def rock_paper_scissors(self, context: Context) -> None:
        """
        Play the rock paper scissors game.

        :param context: The hybrid command context.
        """
        choices = {
            "Rock": [":rock:", 0xFFFFFF],
            "Paper": [":roll_of_paper:", 0xC4C3D0],
            "Scissors": [":scissors:", 0xFB4D46],
        }
        result = random.choice([x for x in choices])
        embed = discord.Embed(
            description=f" **{choices[result][0]} {context.author.name}** chose **{result}**! {choices[result][0]}",
            color=choices[result][1],
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="roll",
        description="Roll a random number within a given range.",
        aliases=["r"],
    )
    @checks.not_blacklisted()
    async def roll(self, context: Context, max_range: str = "100") -> None:
        """
        Roll a random number within a given range.

        :param context: The hybrid command context.
        :param max_range: The upper end of the range.
        """
        if max_range.isalpha():
            max_range = 100
        result = random.randint(0, int(max_range))
        embed = discord.Embed(
            description=f":game_die: **{context.author.name}** rolls **{result}**! :game_die:",
            color=0x9C84EF,
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="pick",
        description="Pick a choice amongst given choices.",
    )
    @checks.not_blacklisted()
    async def pick(self, context: Context, *, choices: str) -> None:
        """
        Pick a choice amongst given choices.

        :param context: The hybrid command context.
        :param choices: The choices available to pick from.
        """
        choice = random.choice(choices.split(" "))
        await context.send(choice)

    @commands.hybrid_command(
        name="meme",
        description="Show a random meme.",
    )
    @checks.not_blacklisted()
    async def meme(self, context: Context) -> None:
        """
        Show a random meme.

        :param context: The hybrid command context.
        """
        rsa_token = os.getenv("RS_API_TOKEN")
        ra_token = os.getenv("RAPIDAPI_TOKEN")
        url = "https://random-stuff-api.p.rapidapi.com/reddit/RandomMeme"
        querystring = {"searchType": "rising"}
        headers = {
            "authorization": rsa_token,
            "x-rapidapi-host": "random-stuff-api.p.rapidapi.com",
            "x-rapidapi-key": ra_token,
        }

        def get_meme():
            response = requests.request("GET", url, headers=headers, params=querystring)
            global meme_response
            meme_response = response.json()
            if meme_response["image"]:
                meme_response = response.json()
            else:
                get_meme()

        get_meme()
        embed = discord.Embed(
            description=f'**{meme_response["title"]}**', color=0x9C84EF
        )
        embed.set_image(url=meme_response["image"])
        embed.set_footer(text=f"r/{meme_response['subreddit']}")
        await context.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Fun(bot))
