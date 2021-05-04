from discord.ext import commands 
import discord
from Main import logger, RecordUser

class Admin(commands.Cog):
    def __init__(self,bot):
        self.bot = bot 

    @commands.command(name="load",hidden=True)
    @commands.before_invoke(RecordUser)
    @commands.is_owner()
    async def load(self, module : str):
        """Loads a module."""
        name = "load"
        try:
            bot.load_extension(module)
        except Exception as Exc:
            pass
        else:
            await ctx.send('\N{OK HAND SIGN}')

    @commands.command(name="unload",hidden=True)
    @commands.before_invoke(RecordUser)
    @commands.is_owner()
    async def unload(self,ctx, *, module : str):
        """Unloads a module."""
        name = "unload"
        try:
            bot.unload_extension(module)
        except Exception as Exc:
            pass
        else:
            await ctx.send('\N{OK HAND SIGN}')

    @commands.command(name='reload', hidden=True)
    @commands.before_invoke(RecordUser)
    @commands.is_owner()
    async def reload(self,ctx, *, module : str):
        """Reloads a module."""
        try:
            bot.unload_extension(module)
            bot.load_extension(module)
        except Exception as Exc:
            pass
        else:
            await ctx.send('\N{OK HAND SIGN}')

def setup(bot):
    logger.debug("| Loaded Admin | ")
    bot.add_cog(Admin(bot))

def teardown(bot):
    logger.debug("| Unloaded Admin | ")
    bot.remove_cog(Admin(bot))     