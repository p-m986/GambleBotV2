from discord.ext import commands
from discord.ui import TextInput, View, Button, Select
from database.User import User

class testing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command(name="verify", with_app_command=True)
    async def verify(self, ctx: commands.Context, game_name: str):
        obj = User()
        await obj.set_client()
        found = await obj._User__find_username(username = game_name)
        if found:
            await ctx.send(found, ephemeral=True)
        else:
            await ctx.send("User not found", ephemeral=True)

async def setup(bot):
    await bot.add_cog(testing(bot))