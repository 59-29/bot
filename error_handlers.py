"""
N-Word Counter - A simple-to-use Discord bot that counts how many times each user has said the N-word
Written in 2019 by NinjaSnail1080 (Discord user: @NinjaSnail1080#8581)

To the extent possible under law, the author has dedicated all copyright and related and neighboring rights to this software to the public domain worldwide. This software is distributed without any warranty.
You should have received a copy of the CC0 Public Domain Dedication along with this software. If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
"""

from discord.ext import commands
import discord


class Error_Handlers(commands.Cog):
    """Error Handlers for commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, exception):
        exc = exception
        if isinstance(exc, commands.NotOwner):
            return await ctx.send(f"Only my owner, {self.bot.app_info.owner}, can use that command")

        elif isinstance(exc, commands.NoPrivateMessage):
            return

        elif isinstance(exc, commands.BadArgument):
            return

        elif isinstance(exc, discord.Forbidden):
            return

        elif isinstance(exc, discord.NotFound):
            return

        elif "Missing Permissions" in str(exc):
            return await ctx.send("I don't have the proper perms to complete this command. "
                                  "Giving me the admin perm should fix this issue")

        else:
            return await ctx.send(
                f"```Command: {ctx.command.qualified_name}\n{exc}```An unknown error occured "
                "and I wasn't able to complete that command. Sorry!")


def setup(bot):
    bot.add_cog(Error_Handlers(bot))
