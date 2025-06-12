import discord
from discord.ext import commands, tasks
import logging
from dotenv import load_dotenv
import os
from typing import cast
from pomodoro_model import PomodoroHandler, Pomodoro, Timer, PomodoroState

Context = commands.Context[commands.Bot]


load_dotenv() 
token = os.getenv("DISCORD_TOKEN") # Get token from .env file

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w') # for logging
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guild_reactions = True


bot = commands.Bot(command_prefix= "!", intents= intents, help_command=None)

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

@bot.command(name="help")
async def custom_help(ctx: Context):
    embed = discord.Embed(title="Pomodoro Bot Help", color=discord.Color.green())
    embed.add_field(name="!pomodoro", value="Initialize your pomodoro", inline=False)
    embed.add_field(name="!start", value="Start the pomodoro timer", inline=False)
    embed.add_field(name="!skip", value="Skip the current timer", inline=False)
    embed.add_field(name="!time_left", value="Check remaining time", inline=False)
    embed.add_field(name="!finish", value="Finish your pomodoro", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def pomodoro(ctx: Context):
    embed = discord.Embed(title="Start Pomodoro", 
                          color=discord.Color.orange(),
                          description=f"{ctx.author.mention}'s pomodoro is set!")
    pomodoro_handler.set_pomodoro(ctx)
    await ctx.reply(embed=embed)


@bot.command()
async def timeleft(ctx: Context):
    if not pomodoro_handler.validate(ctx):
        await ctx.reply(embed=discord.Embed(description=f"{ctx.author.mention}, Please set your own Pomodoro first",
                                            title="Pomodoro Error",
                                            color=discord.Color.red()), ephemeral=True)
        return
    time_left: str = pomodoro_handler.get_time_left(ctx)
    await ctx.reply(embed=discord.Embed(description=f"{time_left}",
                                        title="Time Left",
                                        color=discord.Color.orange()))

@bot.command()
async def start(ctx: Context):
    if not pomodoro_handler.validate(ctx):
        await ctx.reply(embed=discord.Embed(description=f"{ctx.author.mention}, Please set your own Pomodoro first",
                                            title="Pomodoro Error",
                                            color=discord.Color.red()), ephemeral=True)
        return
    pomodoro_handler.start(ctx)

    state: PomodoroState = pomodoro_handler.state(ctx)
    match state:
        case PomodoroState.BREAK:
            await ctx.reply(embed=discord.Embed(title=f"Start",
                                                description="Started Break",
                                                color=discord.Color.blue()))
        case PomodoroState.LONG_BREAK:
            await ctx.reply(embed=discord.Embed(title=f"Start",
                                                description="Started Long Break",
                                                color=discord.Color.blurple()))
        case PomodoroState.WORK:
            await ctx.reply(embed=discord.Embed(title=f"Start",
                                                description="Started Work",
                                                color=discord.Color.orange()))
        case _:
            raise ValueError("Can't start a standby state")

    await timeleft(ctx)

@bot.command()
async def skip(ctx: Context):
    if not pomodoro_handler.validate(ctx):
        await ctx.reply(embed=discord.Embed(description=f"{ctx.author.mention}, Please set your own Pomodoro first",
                                            title="Pomodoro Error",
                                            color=discord.Color.red()), ephemeral=True)
        return
    pomodoro_handler.skip(ctx)
    embed = discord.Embed(title="Skip", color=discord.Color.green(), description=f"Skipped {ctx.author.mention}'s timer")
    embed.set_footer(text="Type !start to proceed")
    await ctx.reply(embed=embed)


@bot.command()
async def finish(ctx: Context):
    if not pomodoro_handler.validate(ctx):
        await ctx.reply(embed=discord.Embed(description=f"{ctx.author.mention}, Please set your own Pomodoro first",
                                            title="Pomodoro Error",
                                            color=discord.Color.red()), ephemeral=True)
        return
    pomodoro_handler.end(ctx)
    await ctx.reply(embed=discord.Embed(title="Pomodoro Session Done",
                                        description=f"Good work {ctx.author.mention}",
                                        color=discord.Color.orange()
    ))

@tasks.loop(seconds= 1)
async def check_time_is_up():
    ctx = pomodoro_handler.check_time_is_up()
    for c in ctx:
        embed = discord.Embed(title="Timer is Up!", color=discord.Color.green(), description=f"{c.author.mention}'s timer is up")
        embed.set_footer(text="Type !start to proceed")
        await c.send(embed=embed)

token = cast(str, token)
bot.run(token, log_handler=handler, log_level=logging.DEBUG) 
