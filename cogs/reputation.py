import discord
from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks, db_manager


class Reputation(commands.Cog, name="reputation"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="reputation",
        description="View current reputation count of a user.",
        aliases=["rep", "viewrep"],
    )
    @checks.not_blacklisted()
    async def reputation(self, context: Context, user: discord.User = None) -> None:
        """
        View current reputation count of a user.

        :param context: The hybrid command context.
        :param user: The Discord user whose reputation is to be viewed.
        """
        if user:
            user_id = user.id
        else:
            user = context.author
            user_id = context.author.id
        rep_view_result = await db_manager.get_user_rep(user_id)
        if rep_view_result == None:
            rep_view = 0
            rank = "~"
        else:
            rep_view = rep_view_result[1][1]
            rank = rep_view_result[0]
        embed = discord.Embed(
            description=f"**{user.name}**: **{rep_view}** Rep (#{rank})",
            color=0x9C84EF,
        )
        embed.set_footer(text=f"Requested by {context.author}")
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="give_rep",
        description="Add reputation points to a user.",
        aliases=["giverep", "gr"],
    )
    @checks.not_blacklisted()
    @checks.is_moderator()
    async def give_rep(
        self, context: Context, user: discord.User, rep_count: int = 1
    ) -> None:
        """
        Add reputation points to a user.

        :param context: The hybrid command context.
        :param user: The Discord user whose reputation is to be incremented.
        :param rep_count: The amount of reputation to add.
        """
        try:
            assert 1 <= rep_count <= 10
            if user:
                if user.id != context.author.id:
                    user_id = user.id
                    await db_manager.add_rep(user_id, rep_count)
                    rep_view_result = await db_manager.get_user_rep(user_id)
                    rep_view = rep_view_result[1][1]
                    rank = rep_view_result[0]
                    embed = discord.Embed(
                        description=f"Gave `{rep_count}` to **{user.name}** (**{rep_view}** Rep #{rank})",
                        color=0x9C84EF,
                    )
                    embed.set_footer(text=f"Requested by {context.author}")
                    await context.send(embed=embed)
                else:
                    await context.send("You can't add reputation to yourself!")
        except AssertionError:
            await context.send("You can't give more than 10 rep points at a time!")

    @commands.hybrid_command(
        name="del_rep",
        description="Delete reputation points from a user.",
        aliases=["takerep", "tr"],
    )
    @checks.not_blacklisted()
    @checks.is_moderator()
    async def del_rep(
        self, context: Context, user: discord.User, rep_count: int = 1
    ) -> None:
        """
        Delete reputation points from a user.

        :param context: The hybrid command context.
        :param user: The Discord user whose reputation is to be incremented.
        :param rep_count: The amount of reputation to delete.
        """
        try:
            assert 1 <= rep_count <= 10
            if user:
                if user.id != context.author.id:
                    user_id = user.id
                    await db_manager.del_rep(user_id, rep_count)
                    rep_view_result = await db_manager.get_user_rep(user_id)
                    rep_view = rep_view_result[1][1]
                    rank = rep_view_result[0]
                    embed = discord.Embed(
                        description=f"Took `{rep_count}` from **{user.name}** (**{rep_view}** Rep #{rank})",
                        color=0x9C84EF,
                    )
                    embed.set_footer(text=f"Requested by {context.author}")
                    await context.send(embed=embed)
                else:
                    await context.send("You can't take reputation from yourself!")
        except AssertionError:
            await context.send("You can't take more than 10 rep points at a time!")

    @commands.hybrid_command(
        name="clear_rep",
        description="Clears the reputation of all users.",
        aliases=["clearrep"],
    )
    @checks.not_blacklisted()
    @checks.is_owner()
    async def clear_rep(self, context: Context) -> None:
        """
        Clear the reputation of all users.

        :param context: The hybrid command context.
        """
        await db_manager.clear_rep()
        embed = discord.Embed(
            description=f":boom: Cleared all reputation points and the leaderboard! :boom:",
            color=0x9C84EF,
        )
        embed.set_footer(text=f"Requested by {context.author}")
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="leaderboard",
        description="Show leaderboard of reputation.",
        aliases=["lb", "toprep"],
    )
    @checks.not_blacklisted()
    async def leaderboard(self, context: Context) -> None:
        """
        Show the leaderbaord of reputation points.

        :param context: The hybrid command context.
        """
        rep_data = await db_manager.get_all_rep()
        embed = discord.Embed(
            description=f"**REPUTATION LEADERBOARD**",
            color=0x9C84EF,
        )
        data, embed_str = [], ""
        data.append("# -- Points -- User")
        for each in rep_data:
            mem = context.guild.get_member(int(each[1]))
            data.append("#{:<3d} - {:^5d}-  {:30s}".format(each[0], each[2], str(mem)))
        embed_str = "\n".join(data)
        embed.add_field(name="", value=f"```{embed_str}```", inline=True)
        embed.set_footer(text=f"Requested by {context.author}")
        await context.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Reputation(bot))
