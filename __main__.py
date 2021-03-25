# import required dependicies
import discord 
from discord.ext import commands  
import os

# Import Bot Token 
BOT_TOKEN = os.environ['BOT_TOKEN']

# Load Rich Intents
intents = discord.Intents.default()
intents.members = True 

# Instantiate Bot 
bot = commands.Bot(command_prefix = '/', intents=intents)

# Start Up

@bot.event
async def on_ready():
  print(f"""
      ════════════════════════════════════
      Logged On As {bot.user.name} ϕ       
      ID : {bot.user.id}                
      ════════════════════════════════════\n""")

@bot.event
async def on_member_join(member):
  'Welcomes Users'
  channel = client.get_channel(822449146622509068)
  await channel.send(f"Welcome, <@{member.id}>")

@bot.event
async def on_member_remove(member):
  'Checks When Users Leave'
  channel = client.get_channel(822471540057964657)
  await channel.send(f"{member} has left")  

print("")

if __name__ == "__main__":
  for filename in os.listdir('cogs'):
    if filename.endswith(".py"):
      bot.load_extension(f'cogs.{filename[:-3]}')
      print(f"Loaded {filename}")
  bot.run(BOT_TOKEN)