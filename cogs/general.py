""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 5.5.0
"""

import platform
import random
import pickle
import requests
import re
from num2words import num2words

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks


class General(commands.Cog, name="general"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="help",
        description="List all commands the bot has loaded."
    )
    @checks.not_blacklisted()
    async def help(self, context: Context) -> None:
        prefix = self.bot.config["prefix"]
        embed = discord.Embed(
            title="Help", description="List of available commands:", color=0x9C84EF)
        for i in self.bot.cogs:
            cog = self.bot.get_cog(i.lower())
            commands = cog.get_commands()
            data = []
            for command in commands:
                description = command.description.partition('\n')[0]
                if command.aliases:
                    data.append(f"{prefix}{command.name} ({command.aliases[0]}) - {description}")
                else:
                    data.append(f"{prefix}{command.name} - {description}")
            help_text = "\n".join(data)
            embed.add_field(name=i.capitalize(),
                            value=f'```{help_text}```', inline=False)
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="botinfo",
        description="Get some useful (or not) information about the bot.",
    )
    @checks.not_blacklisted()
    async def botinfo(self, context: Context) -> None:
        """
        Get some useful (or not) information about the bot.

        :param context: The hybrid command context.
        """
        embed = discord.Embed(
            description="Made with ♥ by SlyPrey",
            color=0x9C84EF
        )
        embed.set_author(
            name="Bot Information"
        )
        embed.add_field(
            name="Owner:",
            value="SlyPrey#6688",
            inline=True
        )
        embed.add_field(
            name="Python Version:",
            value=f"{platform.python_version()}",
            inline=True
        )
        embed.add_field(
            name="Prefix:",
            value=f"/ (Slash Commands) or {self.bot.config['prefix']} for normal commands",
            inline=False
        )
        embed.set_footer(
            text=f"Requested by {context.author}"
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="serverinfo",
        description="Get some useful (or not) information about the server.",
    )
    @checks.not_blacklisted()
    async def serverinfo(self, context: Context) -> None:
        """
        Get some useful (or not) information about the server.

        :param context: The hybrid command context.
        """
        roles = [role.name for role in context.guild.roles]
        if len(roles) > 50:
            roles = roles[:50]
            roles.append(f">>>> Displaying[50/{len(roles)}] Roles")
        roles = ", ".join(roles)

        embed = discord.Embed(
            title="**Server Name:**",
            description=f"{context.guild}",
            color=0x9C84EF
        )
        if context.guild.icon is not None:
            embed.set_thumbnail(
                url=context.guild.icon.url
            )
        embed.add_field(
            name="Server ID",
            value=context.guild.id
        )
        embed.add_field(
            name="Member Count",
            value=context.guild.member_count
        )
        embed.add_field(
            name="Text/Voice Channels",
            value=f"{len(context.guild.channels)}"
        )
        embed.add_field(
            name=f"Roles ({len(context.guild.roles)})",
            value=roles
        )
        embed.set_footer(
            text=f"Created at: {context.guild.created_at}"
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="ping",
        description="Check if the bot is alive.",
    )
    @checks.not_blacklisted()
    async def ping(self, context: Context) -> None:
        """
        Check if the bot is alive.

        :param context: The hybrid command context.
        """
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"The bot latency is {round(self.bot.latency * 1000)}ms.",
            color=0x9C84EF
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="invite",
        description="Get the invite link of the bot to be able to invite it.",
    )
    @checks.not_blacklisted()
    async def invite(self, context: Context) -> None:
        """
        Get the invite link of the bot to be able to invite it.

        :param context: The hybrid command context.
        """
        embed = discord.Embed(
            description=f"Invite me by clicking [here](https://discordapp.com/oauth2/authorize?&client_id={self.bot.config['application_id']}&scope=bot+applications.commands&permissions={self.bot.config['permissions']}).",
            color=0xD75BF4
        )
        try:
            # To know what permissions to give to your bot, please see here: https://discordapi.com/permissions.html and remember to not give Administrator permissions.
            await context.author.send(embed=embed)
            await context.send("I sent you a private message!")
        except discord.Forbidden:
            await context.send(embed=embed)

    @commands.hybrid_command(
        name="8ball",
        description="Ask any question to the bot.",
        aliases=["8b"]
    )
    @checks.not_blacklisted()
    @app_commands.describe(question="The question you want to ask.")
    async def eight_ball(self, context: Context, *, question: str) -> None:
        """
        Ask any question to the bot.

        :param context: The hybrid command context.
        :param question: The question that should be asked by the user.
        """
        answers = ["It is certain.", "It is decidedly so.", "You may rely on it.", "Without a doubt.",
                   "Yes - definitely.", "As I see, yes.", "Most likely.", "Outlook good.", "Yes.",
                   "Signs point to yes.", "Reply hazy, try again.", "Ask again later.", "Better not tell you now.",
                   "Cannot predict now.", "Concentrate and ask again later.", "Don't count on it.", "My reply is no.",
                   "My sources say no.", "Outlook not so good.", "Very doubtful.","F off.", "Maybe your maternal figure."]
        embed = discord.Embed(
            title="**My Answer:**",
            description=f"{random.choice(answers)}",
            color=0x9C84EF
        )
        embed.set_footer(
            text=f"The question was: {question}"
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="bitcoin",
        description="Get the current price of bitcoin.",
    )
    @checks.not_blacklisted()
    async def bitcoin(self, context: Context) -> None:
        """
        Get the current price of bitcoin.

        :param context: The hybrid command context.
        """
        # This will prevent your bot from stopping everything when doing a web request - see: https://discordpy.readthedocs.io/en/stable/faq.html#how-do-i-make-a-web-request
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.coindesk.com/v1/bpi/currentprice/BTC.json") as request:
                if request.status == 200:
                    data = await request.json(
                        content_type="application/javascript")  # For some reason the returned content is of type JavaScript
                    embed = discord.Embed(
                        title="Bitcoin price",
                        description=f"The current price is {data['bpi']['USD']['rate']} :dollar:",
                        color=0x9C84EF
                    )
                else:
                    embed = discord.Embed(
                        title="Error!",
                        description="There is something wrong with the API, please try again later",
                        color=0xE02B2B
                    )
                await context.send(embed=embed)

    @commands.hybrid_command(
        name="change_server_logo",
        description="Change the logo of the server.",
        aliases=["csl"]
    )
    @checks.not_blacklisted()
    async def change_server_logo(self, context=Context) -> None:
        """
        Get the status of the attachments.

        :param context: The hybrid command context.
        :param message: The message
        """
        if len(context.message.attachments) == 1:
                img = context.message.attachments[0] # get the first attachment element from a lit of attachements
                
                '''if attachment is not a png, jpg, or jpeg image type, ignore'''
                if img.filename.endswith(('.jpg','.png','.jpeg')):
                    img_url = img.url

                    '''use aiohttp Clientsession to asynchronously scrape the attachment url and read the data to a variable'''
                    async with aiohttp.ClientSession() as session:
                        async with session.get(img_url) as response:

                            '''if site response, read the response data into img_data'''
                            if response.status == 200:
                                img_data = await response.read()

                    '''update the guild icon with the data stored in img_data'''
                    await context.message.guild.edit(icon=img_data)
    
    @commands.hybrid_command(
        name="todo",
        description="Manage To-Dos.",
    )
    @checks.not_blacklisted()
    async def todo(self, context=Context, *, task: str = None) -> None:
        """
        List, enlist, delist to-dos.

        :param context: The hybrid command context.
        :param task: The task to be done.
        """
        if task is None:
            embed = discord.Embed(
                description="You need to specify a subcommand.\n\n**Subcommands:**\n`<taskname>` - Add a task to your list.\n`list` - View your task list.\n`delete` - Remove a task from your list.\n`clear` - Clear your task list.",
                color=0xE02B2B
            )
            await context.send(embed=embed)
        if task == "list" and task != None:
            with open(r"database\todos.dat", "rb") as tdl:
                n_list = []
                user_id = context.author.id
                try:
                    while True:
                        data = pickle.load(tdl)
                        if user_id in data:
                            n_list.append(data)
                        else:
                            continue
                except EOFError:
                    pass
            embed = discord.Embed(
                description=f"List of {context.author.name}'s To-Dos.\n",
                color=0x9C84EF
            )
            embed.set_author(
                name="To-Do List"
            )
            if len(n_list) != 0:
                for each in n_list:
                    embed.add_field(
                        name=f"__Task {each[0]}__",
                        value=f"{each[2]}",
                        inline=False
                    )
            else:
                embed.add_field(
                    name="Make some to-dos!",
                    value="",
                    inline=False
                )
            embed.set_footer(
                text=f"Requested by {context.author}"
            )
            await context.send(embed=embed)
        if task.split(" ")[0] ==  "delete" and task != None:
            n_list = []
            with open(r"database\todos.dat",'rb') as f:
                user_id = int(context.author.id)
                task_d = int(str(context.message.content).split(" ")[2])
                try:
                    while True:
                        data = pickle.load(f)
                        if user_id in data and task_d in data:
                            continue
                        else:
                            n_list.append(data)
                except EOFError:
                    pass
            with open(r"database\todos.dat", "wb") as f1:
                for each in n_list:
                    pickle.dump(each, f1)
                embed = discord.Embed(
                    description=f"Successfully deleted task {task_d}.",
                    color=0x9C84EF
                )
                await context.send(embed=embed)
        if task == "clear" and task != None:
            n_list = []
            with open(r"database\todos.dat",'rb') as f:
                user_id = int(context.author.id)
                try:
                    while True:
                        data = pickle.load(f)
                        if user_id in data:
                            continue
                        else:
                            n_list.append(data)
                except EOFError:
                    pass
            with open(r"database\todos.dat", "wb") as f1:
                for each in n_list:
                    pickle.dump(each, f1)
                embed = discord.Embed(
                    description=f"Successfully cleared your task list.",
                    color=0x9C84EF
                )
                await context.send(embed=embed)
        elif task.split(" ")[0] not in ["list", "delete", "clear", None]:
            n_list = rec = []
            count = 0
            user_id = context.author.id
            with open(r"database\todos.dat",'rb') as f1:
                try:
                    while True:
                        data = pickle.load(f1)
                        n_list.append(data)
                except EOFError:
                    pass
            for each in n_list:
                count += each.count(user_id)
            tl = [count+1, context.author.id, task]
            with open(r"database\todos.dat", "ab") as tdl:
                pickle.dump(tl, tdl)
            embed = discord.Embed(
                description=f"Successfully added the task **{task}**.",
                color=0x9C84EF
            )
            await context.send(embed=embed)

    @commands.hybrid_command(
        name="poll",
        description="Create a poll.",
    )
    @checks.not_blacklisted()
    async def poll(self, context: Context) -> None:
        """
        Create a poll.

        :param context: The hybrid command context.
        """
        poll_options = re.findall('"([^"]*)"', context.message.content)
        poll_question = context.message.content.partition("\"")[0].split("*poll")[1]
        embed = discord.Embed(
            description=f"{context.author.name}'s Poll",
            color=0x9C84EF
        )
        embed.set_author(
            name=f"{poll_question}"
        )
        if len(poll_options) != 0:
            for each in poll_options:
                opt_num = num2words(poll_options.index(each) + 1)
                embed.add_field(
                    name=f":{opt_num}: {each}",
                    value="",
                    inline=False
                )
        else:
            embed.add_field(
                name="Poll options are empty!",
                value="",
                inline=False
            )
        embed.set_footer(
            text=f"Requested by {context.author}"
        )
        purge = await context.channel.purge(limit=1)
        poll_embed = await context.send(embed=embed)
        for num in range(1, len(poll_options)+1):
            emojiname = str(num) + '\ufe0f\u20e3'
            await poll_embed.add_reaction(emojiname)


async def setup(bot):
    await bot.add_cog(General(bot))
