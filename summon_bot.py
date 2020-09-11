#!/usr/bin/env python3
import yaml
import random
import discord
from discord.ext import commands


bot = commands.Bot(command_prefix="!")


with open("config.yaml") as f:
    """
    config.yaml

    bot_token: <bot-token>
    guild_id: <guild-id>
    """
    config = yaml.load(f, Loader=yaml.FullLoader)
    BOT_TOKEN = config["bot_token"]
    GUILD_ID = config["guild_id"]


@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.id == GUILD_ID:
            break
    print(f"{bot.user} is connected to: {guild.name}(id: {guild.id})")

    await bot.change_presence(activity=discord.Game(name="with life (!summon_bot)"))


@bot.command(name="summon_bot")
async def summon_bot(ctx):
    reply = discord.Embed(color=discord.Color.green())
    reply.title = "How to summon?"
    reply.description = """
    `!summon @username [mode]`

    mode:
        - 0: CALL (3 times) -> default
        - 1: SHOUT (7 times)
        - 2: SCREAM (15 times)

    Frustrated? Just kill them: `!kill @username`
    """

    await ctx.channel.send(embed=reply)


@bot.command(name="kill")
async def kill(ctx, call_user: str = None):
    user_ids = []
    for member in ctx.guild.members:
        user_ids.append(f"{member.id}")
    call_user_id = call_user[3:-1]

    if call_user_id in user_ids:
        reply = discord.Embed()
        gifs = [
            "https://media.giphy.com/media/xTcnTjeH5rtf6bdlwA/giphy.gif",
            "https://media.giphy.com/media/xUPGcdlIDdjwxbjrO0/giphy.gif",
            "https://media.giphy.com/media/yNFjQR6zKOGmk/giphy.gif",
        ]
        reply.set_image(url=random.choice(gifs))
        reply.title = f"Mode: KILL"

        await ctx.send(embed=reply)
        await ctx.send(call_user)
    else:
        reply = discord.Embed(color=discord.Color.red())
        reply.description = "Can you kill someone from this server?"
        reply.title = "FOOL SPOTTED"
        await ctx.send(embed=reply)


@bot.command(name="summon")
async def summon(ctx, call_user: str = None, level: int = 0):
    user_ids = []
    for member in ctx.guild.members:
        user_ids.append(f"{member.id}")
    call_user_id = call_user[3:-1]

    number = 3
    strs = [f"Yo! {call_user}", f"Hey! {call_user}", f"Listen! {call_user}"]
    reply = discord.Embed(color=discord.Color.purple())
    reply.description = "Calling..."
    reply.title = "Mode: CALL"
    if level == 1:
        number = 7
        strs = [
            f"COME ONLINE!!! {call_user}",
            f"WAKE UP!!! {call_user}",
            f"REPLY ASAP!!! {call_user}",
        ]
        reply = discord.Embed(color=discord.Color.orange())
        reply.description = "SHOUTING..."
        reply.title = "Mode: SHOUT"
    elif level == 2:
        number = 15
        strs = [
            f"WHY AREN'T YOU ONLINE, YOU DUMB FUCK? {call_user}",
            f"WHAT THE HELL IS THE MATTER WITH YOU, YOU TWAT? {call_user}",
            f"YOU ARE A HORRIBLE PERSON! {call_user}",
        ]
        reply = discord.Embed(color=discord.Color.red())
        reply.description = "SCREAMING!!!"
        reply.title = "Mode: SCREAM"

    await ctx.send(embed=reply)

    if call_user_id in user_ids:
        reply = random.choice(strs)
        for _ in range(number):
            await ctx.send(reply)
    else:
        reply = discord.Embed(color=discord.Color.red())
        reply.description = "Whom do I call again?"
        reply.title = "FOOL SPOTTED"
        await ctx.send(embed=reply)


bot.run(BOT_TOKEN)
