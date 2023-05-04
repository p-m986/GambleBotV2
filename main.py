from discord.ext import commands
from Logs import logevents
from dotenv import load_dotenv
import discord
import os
import asyncio

load_dotenv()
bot = commands.Bot(command_prefix="$", help_command=None, strip_after_prefix=True, intents=discord.Intents.all())

# Connecting to the Discord API


@bot.event
async def on_connect():
    print("Connected to the api successfully")


@bot.event
async def on_ready():
    obj = logevents()
    await obj.log_restart()
    await bot.tree.sync()
    print("Ready for code execution")


# @bot.event
# async def on_message(message):
#     await message.channel.send("Working on it")

# Fetching the modules sotred in the cogs folder and loading them onto the bot using the load_extension function
@bot.hybrid_command(name="reload", with_app_command=True)
async def reload(ctx: commands.Context, cog:str):
    if ctx.author.id in [782252708685414470]:
        try:
            await bot.unload_extension(f"cogs.{cog}")
            await bot.load_extension(f"cogs.{cog}", package='BOTAPRILUPDATE.database')
            await ctx.reply(f"{cog} has been reloaded successfully",ephemeral=True)
        except Exception as e:
            obj = logevents()
            errorid = await obj.log_error(class_name="Main", function_name="ReloadCommand", message=str(e))
            print(f'An error occoured in the Uer class wtihin the {cog} cog, check error logs with id {errorid} for more details')
            raise e
                
async def loadcog():
    for cog in os.listdir("./cogs"):
        if cog.endswith(".py"):
            try:
                cog = f"cogs.{cog.replace('.py', '')}"
                await bot.load_extension(cog, package='BOTAPRILUPDATE')
                print("Loaded:\t", cog)
            except Exception as e:
                obj = logevents()
                errorid = await obj.log_error(class_name="Main", function_name="loadcog", message=str(e))
                print(f'An error occoured in the Uer class wtihin the {cog} cog, check error logs with id {errorid} for more details')
                raise e


try:
    asyncio.run(loadcog())
except Exception as e:
    print(e)


try:
    bot.run(os.getenv('TOKEN'))
except Exception as e:
    obj = logevents()
    asyncio.run(obj.log_error(class_name="Main", function_name="loadcog", message=str(e)))
