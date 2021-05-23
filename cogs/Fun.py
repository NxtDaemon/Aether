import discord
from discord.ext import commands
from Main import logger,RecordUser

class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # * Poll Code is taken from JackBot https://github.com/pwnker/Jackbot/blob/main/cogs/fun.py

    @commands.command(pass_context=True)
    @commands.before_invoke(RecordUser)
    async def poll(self, ctx , poll_question: str):
        "Takes a poll question and creates a poll in the poll channel or in the same channel it was invoked if no poll channel is setup."

        poll_channel_id = 845824179530235914
        confirm_msg = discord.Embed(description=f":white_check_mark: Your poll has been sent to <#{poll_channel_id}> to be voted on.",color=0x6ABE6C)
        confirm_msg.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=confirm_msg)

        poll_channel = self.bot.get_channel(poll_channel_id)
        poll_embed = discord.Embed(color=0x37A7F3, title=poll_question)
        poll_embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        poll_embed.set_footer(text="React bellow to vote.")
        poll = await poll_channel.send(embed=poll_embed)
        await poll.add_reaction("✅")
        await poll.add_reaction("❌")

def setup(bot):
    logger.debug("| Loaded Poll | ")
    bot.add_cog(Fun(bot))
