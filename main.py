"""
N-Word Counter - A simple-to-use Discord bot that counts how many times each user has said the N-word
Written in 2019 by NinjaSnail1080 (Discord user: @NinjaSnail1080#8581)

To the extent possible under law, the author has dedicated all copyright and related and neighboring rights to this software to the public domain worldwide. This software is distributed without any warranty.
You should have received a copy of the CC0 Public Domain Dedication along with this software. If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
"""

from discord.ext import commands, tasks
import discord
import asyncpg
import asyncio
import psutil

import datetime
import time
import re
import os

import config #! You'll need to define your own credentials in config.py

bot = commands.Bot(
    command_prefix=commands.when_mentioned,
    description="N-Word Counter",
    case_insensitive=True,
    help_command=None,
    status=discord.Status.invisible,
    intents=discord.Intents(members=True),
    fetch_offline_members=True
)

bot.process = psutil.Process(os.getpid())
bot.ready_for_commands = False
bot.load_extension("commands")
bot.load_extension("error_handlers")


async def create_pool():
    """Create table in postgres database if it doesn't already exist. Otherwise, get the n-word data"""

    bot.pool = await asyncpg.create_pool(config.POSTGRES)
    async with bot.pool.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS nwords (
                id BIGINT PRIMARY KEY,
                total BIGINT NOT NULL DEFAULT 0,
                hard_r BIGINT NOT NULL DEFAULT 0
            )
        ;""")

        await conn.execute("""
                INSERT INTO nwords
                (id)
                VALUES (0)
                ON CONFLICT (id)
                    DO NOTHING
            ;""")

        query = await conn.fetch("SELECT * FROM nwords;")

    bot.nwords = {}
    for i in query:
        bot.nwords.update({i.get("id"): dict(i)})


@bot.event
async def on_connect():
    print("\nConnected to Discord")


@bot.event
async def on_ready():
    await create_pool()

    print("\nLogged in as:")
    print(bot.user)
    print(bot.user.id)
    print("-----------------")
    print(datetime.datetime.now().strftime("%m/%d/%Y %X"))
    print("-----------------")
    print("Shards: " + str(bot.shard_count))
    print("Servers: " + str(len(bot.guilds)))
    print("Users: " + str(len(bot.users)))
    print("-----------------\n")

    update_db.start()
    bot.ready_for_commands = True
    bot.started_at = datetime.datetime.utcnow()
    bot.app_info = await bot.application_info()

    await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(
        name=f"for N-Words on {len(bot.guilds)} servers", type=discord.ActivityType.watching))


@bot.event
async def on_message(message):
    if not bot.ready_for_commands or message.author.bot:
        return

    if message.guild is not None:
        for m in re.finditer(r"\b(nigga)(s\b|\b)", message.content, re.IGNORECASE):
            if message.author.id not in bot.nwords:
                bot.nwords.update(
                    {message.author.id: {"total": 0, "hard_r": 0, "id": message.author.id}})
            bot.nwords[message.author.id]["total"] += 1
            bot.nwords[0]["total"] += 1
        for m in re.finditer(r"\b(nigger)(s\b|\b)", message.content, re.IGNORECASE):
            if message.author.id not in bot.nwords:
                bot.nwords.update(
                    {message.author.id: {"total": 0, "hard_r": 0, "id": message.author.id}})
            bot.nwords[message.author.id]["total"] += 1
            bot.nwords[0]["total"] += 1
            bot.nwords[message.author.id]["hard_r"] += 1
            bot.nwords[0]["hard_r"] += 1

    ctx = await bot.get_context(message)
    if ctx.valid:
        await bot.invoke(ctx)
    else:
        if bot.user in message.mentions and len(message.mentions) == 2:
            await message.channel.send(f"You need to do `@{bot.user} count <user>` to get the "
                                       f"N-word count of another user.\nDo `@{bot.user} help` "
                                       "for help on my other commands")
        elif bot.user in message.mentions:
            await message.channel.send(f"Do `@{bot.user} help` for help on my commands")


@bot.event
async def on_guild_join(guild):
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(
        name=f"for N-Words on {len(bot.guilds)} servers", type=discord.ActivityType.watching))


@bot.event
async def on_guild_remove(guild):
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(
        name=f"for N-Words on {len(bot.guilds)} servers", type=discord.ActivityType.watching))


@tasks.loop(minutes=5, loop=bot.loop)
async def update_db():
    """Update the SQL database every 5 minutes"""

    async with bot.pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO nwords
            (id)
            VALUES {}
            ON CONFLICT
                DO NOTHING
        ;""".format(", ".join([f"({u})" for u in bot.nwords])))

        for data in bot.nwords.copy().values():
            await conn.execute("""
                UPDATE nwords
                SET total = {},
                    hard_r = {}
                WHERE id = {}
            ;""".format(data["total"], data["hard_r"], data["id"]))


@bot.command(hidden=True)
@commands.is_owner()
async def reload(ctx):
    """Reload the bot's cogs"""

    bot.reload_extension("commands")
    bot.reload_extension("error_handlers")
    await ctx.send("Reloaded extensions")


@bot.command(hidden=True)
@commands.is_owner()
async def restartdb(ctx):
    await create_pool()
    await ctx.send("Restarted database")


@bot.command(hidden=True)
@commands.is_owner()
async def restartudb(ctx):
    update_db.cancel()
    update_db.start()
    await ctx.send("Cancelled and restarted `update_db()`")


try:
    bot.loop.run_until_complete(bot.start(config.TOKEN))
except KeyboardInterrupt:
    print("\nClosing")
    bot.loop.run_until_complete(bot.change_presence(status=discord.Status.invisible))
    for e in bot.extensions.copy():
        bot.unload_extension(e)
    print("Logging out")
    bot.loop.run_until_complete(bot.logout())
finally:
    update_db.cancel()
    bot.loop.run_until_complete(bot.pool.close())
    print("Closed")
