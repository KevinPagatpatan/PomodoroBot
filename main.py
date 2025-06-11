import discord
from discord.ext import commands, tasks
import logging
from dotenv import load_dotenv
import os
from typing import cast
from pomodoro_model import PomodoroHandler, Pomodoro, Timer

Context = commands.Context[commands.Bot]


load_dotenv() 
token = os.getenv("DISCORD_TOKEN") # Get token from .env file

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w') # for logging
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix= "!", intents= intents)

pomodoro_handler = PomodoroHandler(Pomodoro, Timer)


@bot.event
async def on_ready():
    if bot.user is not None:
        name = bot.user.name
        print(f"{name} is ready")
        check_time_is_up.start()
    else:
        raise TypeError("Bot has no username")
    
@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)


@bot.command()
async def pomodoro(ctx: Context):
    pomodoro_handler.set_pomodoro(ctx)
    await ctx.send("Timer set!")

@bot.command()
async def time_left(ctx: Context):
    if not pomodoro_handler.validate(ctx):
        await ctx.reply("Please set your own Pomodoro first")
        return
    time_left: str = pomodoro_handler.get_time_left(ctx)
    await ctx.send(f"{time_left}")

@bot.command()
async def start(ctx: Context):
    if not pomodoro_handler.validate(ctx):
        await ctx.reply("Please set your own Pomodoro first")
        return
    pomodoro_handler.start(ctx)
    await ctx.send(f"started{pomodoro_handler.state(ctx)}")

@bot.command()
async def skip(ctx: Context):
    if not pomodoro_handler.validate(ctx):
        await ctx.reply("Please set your own Pomodoro first")
        return
    pomodoro_handler.skip(ctx)
    await ctx.reply(f"{ctx.author.mention} skipped")

@bot.command()
async def end(ctx: Context):
    if not pomodoro_handler.validate(ctx):
        await ctx.reply("Please set your own Pomodoro first")
        return
    pomodoro_handler.end(ctx)
    await ctx.reply(f"ended {ctx.author.mention}'s pomodoro")

@tasks.loop(seconds= 1)
async def check_time_is_up():
    ctx = pomodoro_handler.check_time_is_up()
    for c in ctx:
        await c.send("Timer is up!")




token = cast(str, token)
bot.run(token, log_handler=handler, log_level=logging.DEBUG)
