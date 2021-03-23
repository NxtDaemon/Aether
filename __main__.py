# import required dependicies
import discord 
from discord.ext import commands  
from discord.ext.commands import has_permissions, MissingPermissions
import json , time  

# Import Bot Token 
from API_Keys import * 

intents = discord.Intents.default()
intents.members = True 

bot = commands.Bot(command_prefix = ';', intents=intents, help_command=None)

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

extentions = ['cogs/List']
if __name__ == "__main__":
  for ext in extentions:
    bot.load_extension(ext)
    
bot.run(BotToken)