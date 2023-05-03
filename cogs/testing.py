from discord.ext import commands
from discord.ui import TextInput, View, Button, Select
import asyncio
import sys
sys.path.append('../database')
from User import User

class testing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command(name="verify", with_app_command=True)
    async def verify(self, ctx: commands.Context, game_name: str):
        obj = User()
        found = await obj._User__find_username(username = game_name)
        await ctx.send(found, ephemeral=True)
        # inputfield1 = Button(label="Testing out write fields", custom_id='INPUT1')
        # my_view = View()
        # my_view.add_item(inputfield1)
        # await ctx.send("It works", view=my_view)


async def setup(bot):
    await bot.add_cog(testing(bot))

if __name__ == "__main__":
    obj = User()
    print(asyncio.run(obj._User__find_username('B_M_9_8_6')))