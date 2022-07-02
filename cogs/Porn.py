import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup as bs
from __main__ import logger, RecordUser
import random
import re
#+++++++++++++++++++++++++++++++++++++++++++++++Main Code++++++++++++++++++++++++++++++++++++++++++++++++++#


class Porn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="rule34", brief="Random Rule 34")
    @commands.before_invoke(RecordUser)
    async def random_porn(self, ctx, Query: str):
        # Sometime Breaks, Likely to be rate limited
        'Queries if a film is avaliable in your countries'
        BANLIST = ["Children", "furry", ]
        EXIT = 0

        for _ in Query:
            if _ in BANLIST:
                await ctx.send("Stop being a weird cunt")
                EXIT = 1

        if ctx.channel.id == 986006069060964383 and EXIT != 1:
            r = requests.get(
                f"https://rule34.xxx/index.php?page=post&s=list&tags={Query}")
            soup = bs(r.text, "html.parser")
            results = soup.find_all(class_="thumb")
            C = random.choice(results)
            URL_REGEX = re.compile('(?P<url>https?://[^\s]+)')
            URL = URL_REGEX.search(repr(C)).group(1)
            Response = discord.Embed(
                color=0xffd700, title=f"Rule34 Result")
            Response.set_image(url=URL)
            Response.set_author(name=ctx.message.author.name,
                                icon_url=ctx.message.author.avatar_url)
            await ctx.send(embed=Response)

        elif ctx.channel.id != 986006069060964383 & EXIT != 1:
            await ctx.send("Invalid channel for this command")


def setup(bot):
    logger.debug("| Loaded Porn | ")
    bot.add_cog(Porn(bot))


def teardown(bot):
    logger.debug("| Unloaded Porn | ")
    bot.remove_cog(Porn(bot))


#+++++++++++++++++++++++++++++++++++++++++++++++Main Code++++++++++++++++++++++++++++++++++++++++++++++++++#
