from discord.ext import commands
import discord
from Main import logger, RecordUser, bot
import asyncio
import datetime


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Command Taken from https://stackoverflow.com/questions/67157139/im-trying-to-setup-a-clear-purge-command-for-my-discord-py-bot-there-are-no-err
    @commands.command(name="purge", brief="Mass Delete Messages")
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, limit: int):
        await ctx.message.delete()
        await asyncio.sleep(1)
        await ctx.channel.purge(limit=limit)
        purge_embed = discord.Embed(
            title='Purge [?purge]', description=f'Successfully purged {limit} messages. \n Command executed by {ctx.author}.', color=discord.Colour.random())
        purge_embed.set_footer(text=str(datetime.datetime.now()))
        await ctx.channel.send(embed=purge_embed, delete_after=True)

    @commands.command(name="reload", brief="Reload Extension")
    @commands.has_permissions(administrator=True)
    async def reload(self, ctx, Cog):
        await ctx.send(f"Attempting to reload {Cog}")
        try:
            self.bot.reload_extension(f"cogs.{Cog}")
            await ctx.send(":gear: Cog Has Been Successfully Reloaded")
        except commands.ExtensionNotFound:
            await ctx.send(f"Cog `{Cog}` Could Not Be Found")

    @commands.command(name="unload", brief="Unload Extension")
    @commands.has_permissions(administrator=True)
    async def unload(self, ctx, Cog):
        await ctx.send(f"Attempting to Unload {Cog}")
        try:
            self.bot.unload_extension(f"cogs.{Cog}")
            await ctx.send(":gear: Cog Has Been Successfully Unloaded")
        except commands.ExtensionNotFound:
            await ctx.send(f"Cog `{Cog}` Could Not Be Found")

    @commands.command(name="load", brief="Load Extension")
    @commands.has_permissions(administrator=True)
    async def load(self, ctx, Cog):
        await ctx.send(f"Attempting to load {Cog}")
        try:
            self.bot.load_extension(f"cogs.{Cog}")
            await ctx.send(":gear: Cog Has Been Successfully Loaded")
        except commands.ExtensionNotFound:
            await ctx.send(f"Cog `{Cog}` Could Not Be Found")


def setup(bot):
    logger.debug("| Loaded Admin | ")
    bot.add_cog(Admin(bot))


def teardown(bot):
    logger.debug("| Unloaded Admin | ")
    bot.remove_cog(Admin(bot))
