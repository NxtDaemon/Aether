# import required dependicies
import discord 
from discord.ext import commands , tasks 
from discord.ext.commands import has_permissions, MissingPermissions
import json , time  
from datetime import datetime

# Import Bot Token 
from API_Keys import * 

intents = discord.Intents.default()
intents.members = True 

# Exceptions
class FileEmpty(Exception):
  '''Exception for File's being empty '''
  pass

client = commands.Bot(command_prefix = '!', intents=intents)

@client.event
async def on_ready():
  print("""
      __________________________________
      DaemonBot is Online , Welcome User\n 
      
      """)

@client.event
async def on_member_join(member):
  'Welcomes Users'
  channel = client.get_channel(822449146622509068)
  await channel.send(f"Welcome, <@{member.id}>")

@client.event
async def on_member_remove(member):
  'Checks When Users Leave'
  channel = client.get_channel(822471540057964657)
  await channel.send(f"{member} has left")  

@client.command()
async def ListAdd (ctx,message):
  'Adds to TODO list'
  st = datetime.now().strftime("%H:%M:%S")
  print(message)
  with open("TODO.txt","a") as f:
    f.write(f"{message} : {st}\n")
  await ctx.send("Todo List updated")

@client.command()
async def ListAll (ctx):
  try:
    STP = ""
    with open("TODO.txt","r") as f:
      content = f.readlines()
      if content == "":
        raise FileEmpty
      else:
        i = 0
        for _ in content:
          i += 1
          STP += f"{i} : `{_}`"
        await ctx.send(STP + " ")
  except(FileEmpty):
    ctx.send('List is Empty')
        
@client.command()
async def ListRemove(ctx,Number):
  try:
    with open("TODO.txt","r+") as f:
      content = f.readlines()
      line = content[int(Number)-1]
      content.remove(line)
      f.seek(0)
      f.truncate()
      for _ in content:
        f.write(_)
    if line in content:
      await ctx.send(f"Error Recieved")
    else:
      await ctx.send(f"Removed {Number}")
  except(IndexError):
    await ctx.send(f"This Component Does Not Exist in The List : `{Number}`")
      
client.run(BotToken)