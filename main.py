from discord.ext import bridge, commands
from Logs import logevents
from dotenv import load_dotenv
import discord
import os
import asyncio

load_dotenv()
bot = bridge.Bot(command_prefix=commands.when_mentioned_or(
    '$'), help_command=None, strip_after_prefix=True, intents=discord.Intents.all())

# Connecting to the Discord API


@bot.event
async def on_connect():
    if bot.auto_sync_commands:
        await bot.sync_commands()
    print(f"{bot.user.name} connected to the api successfully")


@bot.event
async def on_ready():
    obj = logevents()
    await obj.log_restart()
    print("Ready for code execution")

# @bot.bridge_command()
# async def ping(ctx: bridge.BridgeContext):
#     await ctx.respond("Pong!")

# Fetching the modules sotred in the cogs folder and loading them onto the bot using the load_extension function


@bot.bridge_command()
async def reload(ctx: bridge.BridgeContext, cog: str):
    if ctx.author.id == 782252708685414470:
        try:
            bot.reload_extension(f"cogs.{cog}")
            await ctx.reply(f"{cog} has been reloaded successfully", ephemeral=True)
        except Exception as e:
            obj = logevents()
            errorid = await obj.log_error(class_name="Main", function_name="ReloadCommand", message=str(e))
            print(f'An error occoured in the Main class wtihin the {cog} cog, check error logs with id {errorid} for more details')
            raise e


async def loadcog():
    for cog in os.listdir("./cogs"):
        if cog.endswith(".py"):
            try:
                cog = f"cogs.{cog.replace('.py', '')}"
                bot.load_extension(cog, package='BOTAPRILUPDATE')
                print("Loaded:\t", cog)
            except Exception as e:
                obj = logevents()
                errorid = await obj.log_error(class_name="Main", function_name="loadcog", message=str(e))
                print(
                    f'An error occoured in the Uer class wtihin the {cog} cog, check error logs with id {errorid} for more details')
                raise e


try:
    asyncio.run(loadcog())
except Exception as e:
    print(e)


try:
    bot.run(os.getenv('TOKEN'))
except Exception as e:
    obj = logevents()
    asyncio.run(obj.log_error(class_name="Main",
                function_name="loadcog", message=str(e)))
