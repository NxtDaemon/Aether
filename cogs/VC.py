import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup as bs
from __main__ import logger, RecordUser
import time
import asyncio


class VoiceChannel(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Lock a Voice Channel")
    @commands.before_invoke(RecordUser)
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx,):
        # https://stackoverflow.com/questions/62132007/discord-py-channel-edit-doesnt-do-anything-and-bot-doesnt-go-past-that-line
        # Rate Limited Per 10 Minutes
        channel = ctx.author.voice.channel
        Name = channel.name
        MemCount = len(channel.members)
        await ctx.send("Attempting to Lock VC")
        try:
            await asyncio.wait_for(channel.edit(name=f"Locked {Name}", user_limit=MemCount), timeout=3.0)
            await ctx.send(f"Locked {Name} to {MemCount} Members")
        except asyncio.TimeoutError:
            await ctx.send(" ERROR : :no_entry_sign: Unable to Edit Channel Due to Discord Rate Limiting, Please try again in 10 minutes.")

    @commands.command(brief="Unlock a Voice Channel")
    @commands.before_invoke(RecordUser)
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx,):
        channel = ctx.author.voice.channel
        NameArr = channel.name.split(" ")
        NewName = " ".join(NameArr[1:])
        if NameArr[0] == "Locked":
            await ctx.send("Attempting to Unlock VC")
            try:
                await asyncio.wait_for(channel.edit(name=NewName, user_limit=0), timeout=3.0)
                await ctx.send(f"Unlocked {NewName}")
            except asyncio.TimeoutError:
                await ctx.send(" :no_entry_sign: unable to Edit Channel Due to Discord Rate Limiting, Please try again in 10 minutes.")
        else:
            await ctx.send("This Channel Has Not Been Locked By This Bot")

    @commands.command(brief="Increase the Capacity of a Voice Channel")
    @commands.before_invoke(RecordUser)
    @commands.has_permissions(manage_channels=True)
    async def increase(self, ctx, amount=1):
        channel = ctx.author.voice.channel
        NameArr = channel.name.split(" ")
        NewName = " ".join(NameArr[1:])
        if NameArr[0] == "Locked" and amount in range(0, 99):
            await ctx.send(f"Attempting to Increase {NewName} by {amount}")
            AmendedAmount = channel.user_limit + abs(amount)
            try:
                await asyncio.wait_for(channel.edit(user_limit=AmendedAmount), timeout=3.0)
                await ctx.send(f"Increased {NewName}")
            except asyncio.TimeoutError:
                await ctx.send(" :no_entry_sign: unable to Edit Channel Due to Discord Rate Limiting, Please try again in 10 minutes.")
        else:
            await ctx.send("This Channel Is Not Locked and Hence Cannot be Modified")

    @commands.command(brief="Decrease the Capacity of a Voice Channel")
    @commands.before_invoke(RecordUser)
    @commands.has_permissions(manage_channels=True)
    async def decrease(self, ctx, amount=1):
        channel = ctx.author.voice.channel
        NameArr = channel.name.split(" ")
        NewName = " ".join(NameArr[1:])
        if NameArr[0] == "Locked" and amount in range(0, 99) and (amount < channel.user_limit):
            await ctx.send(f"Attempting to Decrease {NewName} by {amount}")
            AmendedAmount = channel.user_limit - abs(amount)
            try:
                await asyncio.wait_for(channel.edit(user_limit=AmendedAmount), timeout=3.0)
                await ctx.send(f"Decreased {NewName}")
            except asyncio.TimeoutError:
                await ctx.send(" :no_entry_sign: unable to Edit Channel Due to Discord Rate Limiting, Please try again in 10 minutes.")
        else:
            await ctx.send("This Channel Is Not Locked and Hence Cannot be Modified")


def setup(bot):
    logger.debug("| Loaded VC | ")
    bot.add_cog(VoiceChannel(bot))


def teardown(bot):
    logger.debug("| Unloaded VC | ")
    bot.remove_cog(VoiceChannel(bot))
