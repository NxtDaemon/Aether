from discord.ext import commands 
import discord
from Main import logger, RecordUser
import asyncio
import datetime 

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
            bot.unload_extension(module)?la 
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
    
    # Command Taken from https://stackoverflow.com/questions/67157139/im-trying-to-setup-a-clear-purge-command-for-my-discord-py-bot-there-are-no-err
    @commands.command(name="purge")
    @commands.has_permissions(manage_messages=True)
    async def purge(self,ctx, limit: int):
        await ctx.message.delete()
        await asyncio.sleep(1)
        await ctx.channel.purge(limit=limit)
        purge_embed = discord.Embed(title='Purge [?purge]', description=f'Successfully purged {limit} messages. \n Command executed by {ctx.author}.', color=discord.Colour.random())
        purge_embed.set_footer(text=str(datetime.datetime.now()))
        await ctx.channel.send(embed=purge_embed, delete_after=True)



def setup(bot):
    logger.debug("| Loaded Admin | ")
    bot.add_cog(Admin(bot))

def teardown(bot):
    logger.debug("| Unloaded Admin | ")
    bot.remove_cog(Admin(bot))     