import discord 
from discord.ext import commands
import requests
from bs4 import BeautifulSoup as bs 
from __main__ import logger,RecordUser

#+++++++++++++++++++++++++++++++++++++++++++++++Main Code++++++++++++++++++++++++++++++++++++++++++++++++++#

class Netflix(commands.Cog):
    def __init__(self,bot):
        self.bot = bot 

    @commands.command(brief="Search Film Compatibility")
    async def query(self,ctx,Query):
        'Queries if film is avaliable in your areas'
        name = "Query"
        print(f"{ctx.author} running command {name}")
        try:
            Query = str(Query)
            r = requests.get(f"https://unogs.com/search/{Query}?country_andorunique=and&start_year=1900&end_year=2021&end_rating=10&genrelist=&audiosubtitle_andor=or&countrylist=39,46")
            print(r.text) 
            soup = bs(r,"html.parser")
        except(Exception) as Exc:
            logger.error(f"Uncaught Exception in Module : `{name}`, ErrorType : `{type(Exc)}` : {Exc}")

def setup(bot):
    bot.add_cog(Netflix(bot))
        
#+++++++++++++++++++++++++++++++++++++++++++++++Main Code++++++++++++++++++++++++++++++++++++++++++++++++++#
