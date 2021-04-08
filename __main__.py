# import required dependicies
import discord 
from discord.ext import commands  
import logging, coloredlogs
import os , time 

# Create formatters 
DETAILED = logging.Formatter("%(asctime)-30s %(module)-15s %(levelname)-8s %(funcName)-20s %(message)s")

# Custom Logger
logger = logging.getLogger(__name__)
coloredlogs.install(logger=logger,level=logging.DEBUG)
FileHandler = logging.FileHandler("DaemonBot_Errors.log")
FileHandler.setFormatter(DETAILED)
logger.addHandler(FileHandler)

# Import Bot Token 
BOT_TOKEN = os.environ['BOT_TOKEN']

# Load Rich Intents
intents = discord.Intents.default()
intents.members = True 

# Instantiate Bot 
bot = commands.Bot(command_prefix = '?', intents=intents)

# Start Up

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
    logger.info(f"DaemonBot Online At {HRT}")

@bot.event
async def on_member_join(member):
    'Welcomes Users'
    channel = bot.get_channel(822449146622509068)
    await channel.send(f"Welcome, <@{member.id}>")

@bot.event
async def on_member_remove(member):
    'Checks When Users Leave'
    channel = bot.get_channel(822471540057964657)
    await channel.send(f"{member} has left")  

@bot.event
async def on_command_error(ctx,error):
    if isinstance(error, commands.MissingRequiredArgument):
        logger.info("A Request was sent that had Missing Parameters , Request Ignored")
        await ctx.send("A parameter was not set. Please try again")
    else:
        logger.warning(f"Unexpected Error : `{error}`")

print("")

if __name__ == "__main__":
    for filename in os.listdir('cogs'):
        if filename.endswith(".py"):
            bot.load_extension(f'cogs.{filename[:-3]}')
            print(f"Loaded {filename[:-3]}")
    bot.run(BOT_TOKEN)