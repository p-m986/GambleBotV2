import time
import discord

async def createVerificationEmbed(ctx, gameName, currentCountryIcon, currentcountryName, targetName, targetCountryIcon):
        timestamp = int(time.time())
        timeoutTime = timestamp + 320
        res = discord.Embed(
            title="Verify Krunker Username",
            description=f"""{ctx.author.mention} change the country flag of **[{gameName}](https://krunker.io/social.html?p=profile&q={gameName.lower()})**

                        **Once you have changed the flag **
                        To verify click on :white_check_mark: 
                        To cancel it click on :x:

                        This will timeout **<t:{timeoutTime}:R>**""",
            color=0xffff58,
            timestamp=discord.utils.utcnow(),
            url="https://krunker.io/"
        )

        res.set_author(
            name="Krunker.io",
            url="https://krunker.io/",
            icon_url="https://yt3.googleusercontent.com/QQ4sFJjSxp9y54tx5ygCqHUysN-eCFaeFf3y2EGCuPIFIjB6CFNh7DebKJXemuo9x32zOTUvqg=s900-c-k-c0x00ffffff-no-rj"
        )

        res.set_thumbnail(url="https://krunker.io/img/police.png")

        res.add_field(
            name="From",
            value=f":{currentCountryIcon}:: {currentcountryName}",
            inline=True
        )
        res.add_field(
            name="To",
            value=f":{targetCountryIcon}:: {targetName}",
            inline=True
        )

        res.set_footer(
            text="Gamble Bot", icon_url="https://cdn.discordapp.com/avatars/782252708685414470/9935b133ae26d24ae0722846eab6a91a.png?size=1024")
        return res



async def createProcessingEmbed():
        res = discord.Embed(
            title="Processing...",
            description=f"Verifying details",
            color=0xffff58,
            timestamp=discord.utils.utcnow(),
        )

        res.set_author(
            name="Krunker.io",
            url="https://krunker.io/",
            icon_url="https://yt3.googleusercontent.com/QQ4sFJjSxp9y54tx5ygCqHUysN-eCFaeFf3y2EGCuPIFIjB6CFNh7DebKJXemuo9x32zOTUvqg=s900-c-k-c0x00ffffff-no-rj"
        )

        res.set_thumbnail(url="https://media.tenor.com/T3k4hLelPPIAAAAd/loading-waiting.gif")

        res.set_footer(
            text="Gamble Bot", icon_url="https://cdn.discordapp.com/avatars/782252708685414470/9935b133ae26d24ae0722846eab6a91a.png?size=1024")
        return res

async def createErrorEmbed(Error):
        res = discord.Embed(
            title=f"{Error}",
            description=f"",
            color=0xff0000,
            timestamp=discord.utils.utcnow(),
        )

        res.set_author(
            name="Krunker.io",
            url="https://krunker.io/",
            icon_url="https://yt3.googleusercontent.com/QQ4sFJjSxp9y54tx5ygCqHUysN-eCFaeFf3y2EGCuPIFIjB6CFNh7DebKJXemuo9x32zOTUvqg=s900-c-k-c0x00ffffff-no-rj"
        )

        res.set_thumbnail(url="https://media.tenor.com/JWrO9tZNp7IAAAAC/cross-logo-letter-x.gif")

        res.set_footer(
            text="Gamble Bot", icon_url="https://cdn.discordapp.com/avatars/782252708685414470/9935b133ae26d24ae0722846eab6a91a.png?size=1024")
        return res

async def createSuccessEmbed(ctx, gameName):
        res = discord.Embed(
            title=f"Verified Successfully",
            description=f"""{ctx.author.mention}
                            {gameName} has been linked 
                            with your discord successfully""",
            color=0x14ff00,
            timestamp=discord.utils.utcnow(),
        )

        res.set_author(
            name="Krunker.io",
            url="https://krunker.io/",
            icon_url="https://yt3.googleusercontent.com/QQ4sFJjSxp9y54tx5ygCqHUysN-eCFaeFf3y2EGCuPIFIjB6CFNh7DebKJXemuo9x32zOTUvqg=s900-c-k-c0x00ffffff-no-rj"
        )

        res.set_thumbnail(url="https://media.tenor.com/BSY1qTH8g-oAAAAM/check.gif")

        res.set_footer(
            text="Gamble Bot", icon_url="https://cdn.discordapp.com/avatars/782252708685414470/9935b133ae26d24ae0722846eab6a91a.png?size=1024")
        return res