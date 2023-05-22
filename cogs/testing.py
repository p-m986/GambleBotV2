from asyncio import sleep
from discord.ext import commands, bridge
from database.User import User
from Logs import logevents
from cogs.controllers.assignTargetcountry import assignTargetcountry
from cogs.controllers.makeEmbeds import createVerificationEmbed, createProcessingEmbed, createErrorEmbed, createSuccessEmbed

import discord
import requests
import json
import asyncio

# url = "https://testapi.parthmishra3.repl.co/api/fetch"
# This url dosent return flag name
url = "https://krunkerverificationapi.parthmishra3.repl.co/api/fetch"


async def getUserdetails(username):
    data = {
        "username": username
    }

    res = requests.get(url=url, data=data)
    res_data = json.loads(res.text)
    return res.status_code, res_data


class testing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logevents()

    @bridge.bridge_command()
    async def testcommand(self, ctx: bridge.BridgeContext):
        await ctx.defer()
        res = await ctx.respond("Responded")

        await asyncio.sleep(3)

        testEmbed = discord.Embed(
            title="Test Embed",
            description=f"{ctx.author.mention}",
            color=discord.Color.dark_gold(),
            timestamp=discord.utils.utcnow()
        )

        return await res.edit(content=None, embed=testEmbed)

    @bridge.bridge_command(name="save")
    async def save_(self, ctx: bridge.BridgeContext, game_name: str):
        try:
            await ctx.defer()
            res = await ctx.respond("Connecting to Database", embed=None)

            obj = User()
            await obj.set_client()
            user = await obj._User__find_user(id=ctx.author.id)
            print("Got result from database")
            if user:
                Error = await createErrorEmbed(
                    "You have already registerd, Use addAlt command to add another account"
                )
                return await res.edit(embed = Error, content=None)
            
                # The commented part should be a part of the add alt command not this
                # # If username already exsists in the database
                # if (ctx.author.id == user["discord_userid"]):
                #     return await res.edit(content="Verification Failed: This account already belongs to you")
                # else:
                #     # If username is registered with some other user
                #     return await res.edit(content="Verification Failed: This account already belongs to someone else")

            else:
                print("User dosen't exsist in database")
                # If username doses't already exsist in database
                requestStatus, beforeUserdata = await getUserdetails(game_name)
                print("Got data from Api")
                if requestStatus == 500:
                    return await res.edit(content="Verification Failed: Server error")

                if requestStatus == 200:
                    # Check if the its a valid username
                    if beforeUserdata["hasError"]:
                        print(beforeUserdata["hasError"])
                        return await res.edit(content="Verification Failed: Invalid username")
                    else:
                        # If the username is set to hacker
                        if beforeUserdata["hacker"]:
                            return await res.edit(content="Verification Failed: You cant use hacker tagged account")

                        # If it is a valid username initiate the verification process
                        # Initialize target
                        print("Valid Request")
                        targetNum, targetName, targetflagIcon, currentflagIcon, currentCountryName = await assignTargetcountry(beforeUserdata["flagnum"])
                        print("Target assigned")

                        print("Creating embed")
                        embed = await createVerificationEmbed(ctx, game_name, currentflagIcon, currentCountryName, targetName, targetflagIcon)
                        print("Embed created")

                        print("Editing embed in response")
                        await res.edit(content=None, embed=embed)
                        print("Editing finished")

                        try:
                            await res.add_reaction("✅")
                            await res.add_reaction("❌")

                            def check(reaction, user):
                                return user.id == ctx.author.id and not user.bot and str(reaction.emoji) in ["✅", "❌"]

                            try:
                                reaction, _ = await self.bot.wait_for("reaction_add", timeout=180, check=check)
                                await res.clear_reactions()

                                if str(reaction.emoji) == "✅":
                                    # Start Processing
                                    processing = await createProcessingEmbed()
                                    await res.edit(embed=processing)

                                    # Send another req to api
                                    afterrequestStatus, afterUserdata = await getUserdetails(game_name)
                                    print("Got after data from Api")
                                    if requestStatus == 500:
                                        return await res.edit(content="Verification Failed: Server error")
                                    
                                    if afterUserdata["flagnum"] == targetNum:
                                        success = await createSuccessEmbed(ctx, game_name)

                                        # Push the changes to the user in database
                                        await obj._User__add_user(ctx.author.name, ctx.author.id, game_name)
                                        return await res.edit(embed =  success)
                                    else:
                                        Error = await createErrorEmbed("The flag dosent match the target")
                                        return await res.edit(embed = Error)

                                elif str(reaction.emoji) == "❌":
                                    error = await createErrorEmbed(Error="Canceled")
                                    return await res.edit(embed=error)

                            except TimeoutError as T:
                                error = await createErrorEmbed(Error = "Time Out")
                                return await res.edit(embed = error)

                        except Exception as error:
                            
                            error = await createErrorEmbed(Error = "An Error Occoured")
                            await res.edit(embed = error)
                            raise error

        # if data_before["hasError"] == True:

            print("Passed")
        except Exception as error:
            errorid = await self.logger.log_error(class_name="testing", function_name="verify", message=str(error))
            print(f'An error occoured in the Uer class wtihin the testing class, check error logs with id {errorid} for more details')
            raise error


def setup(bot):
    bot.add_cog(testing(bot))


if __name__ == "__main__":
    obj = User()
    obj.set_client()
