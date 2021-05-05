# import required dependicies
import discord 
from discord.ext import commands 
import logging, coloredlogs
import os , time 

# * Create formatters And custom logger
DETAILED = logging.Formatter("%(asctime)-30s %(module)-15s %(levelname)-8s %(funcName)-20s %(message)s")

logger = logging.getLogger(__name__)
coloredlogs.install(logger=logger,level=logging.DEBUG)
FileHandler = logging.FileHandler("Aether-Error.log")
FileHandler.setFormatter(DETAILED)
logger.addHandler(FileHandler)

# * Records Who uses what command 
async def RecordUser(self, ctx):
    logger.debug(f"{ctx.author} running command `{ctx.command}` at `{ctx.message.created_at}`")

# * Import Bot Token 
BOT_TOKEN = os.environ['BOT_TOKEN']

# * Load Rich Intents
intents = discord.Intents.default()
intents.members = True 

# Instantiate Bot and Startup 
bot = commands.Bot(command_prefix = '?', intents=intents)

@bot.event
async def on_ready():
    HRT = time.asctime()
    print(f"""
        ════════════════════════════════════
        Logged On As : {bot.user.name} ϕ      
        Prefix : {bot.command_prefix}
        Time : {HRT}
        ID : {bot.user.id}                
        ════════════════════════════════════\n""")
    logger.info(f"Aether Online At {HRT}")

# Exceptions and Error handling 
@bot.event
async def on_command_error(ctx,error):
    if isinstance(error, commands.MissingRequiredArgument):
        logger.info("A Request was sent that had Missing Parameters , Request Ignored")
        await ctx.send("A parameter was not set. Please try again")
    else:
        logger.warning(f"Unexpected Error : `{error}` in {ctx.command}")
        await ctx.send("Error Encountered :no_entry_sign:")

if __name__ == "__main__":
    print("")
    for filename in os.listdir('cogs'):
        if filename.endswith(".py"):
            bot.load_extension(f'cogs.{filename[:-3]}')
    bot.run(BOT_TOKEN)