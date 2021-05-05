import discord
from discord.ext import commands
from Main import logger,RecordUser

class QuickPoll(commands.Cog):
    """Code Stolen from https://gist.github.com/Vexs/f2c1bfd6bda68a661a71accd300d2adc, however this was modified to fit with modern py3 and latest discord.py """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True,aliases=["poll","p"])
    @commands.before_invoke(RecordUser)

    async def Poll(self, ctx, question, *options: str):
        if len(options) <= 1:
            await ctx.send('You need more than one option to make a poll!')
            return
        if len(options) > 10:
            await ctx.send('You cannot make a poll for more than 10 things!')
            return

        if len(options) == 2 and options[0] == 'yes' and options[1] == 'no':
            reactions = ['✅', '❌']
        else:
            reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']

        description = []
        for x, option in enumerate(options):
            description += f"\n {reactions[x]} {option}"
        embed = discord.Embed(title=question, description=''.join(description))
        react_message = await ctx.send(embed=embed)
        for reaction in reactions[:len(options)]:
            await react_message.add_reaction(reaction)
        embed.set_footer(text=f'Poll ID: {react_message.id}')
        await react_message.edit(embed=embed)

    # TODO Maybe fix this code, IDK what it does but might be useful
    # @commands.command(pass_context=True)
    # @commands.before_invoke(RecordUser)
    # async def tally(self, ctx, id):
    #     poll_message = await bot.get_message(ctx.message.channel, id)
    #     if not poll_message.embeds:
    #         return
    #     embed = poll_message.embeds[0]
    #     if poll_message.author != ctx.message.server.me:
    #         return
    #     if not embed['footer']['text'].startswith('Poll ID:'):
    #         return
    #     unformatted_options = [x.strip() for x in embed['description'].split('\n')]
    #     opt_dict = {x[:2]: x[3:] for x in unformatted_options} if unformatted_options[0][0] == '1' \
    #         else {x[:1]: x[2:] for x in unformatted_options}
    #     # check if we're using numbers for the poll, or x/checkmark, parse accordingly
    #     voters = [ctx.message.server.me.id]  # add the bot's ID to the list of voters to exclude it's votes

    #     tally = {x: 0 for x in opt_dict.keys()}
    #     for reaction in poll_message.reactions:
    #         if reaction.emoji in opt_dict.keys():
    #             reactors = await self.bot.get_reaction_users(reaction)
    #             for reactor in reactors:
    #                 if reactor.id not in voters:
    #                     tally[reaction.emoji] += 1
    #                     voters.append(reactor.id)

    #     output = f"Results of the poll for `{embed['title']}\n`:" + '\n'.join(['{}: {}'.format(opt_dict[key], tally[key]) for key in tally.keys()])
    #     await ctx.send(output)


def setup(bot):
    logger.debug("| Loaded Poll | ")
    bot.add_cog(QuickPoll(bot))
