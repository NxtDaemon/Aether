from discord.ext import commands 
from datetime import datetime
import discord

# List Exceptions
class FileEmpty(Exception):
  '''Exception for Files Being Empty '''
  pass

class MessageEmpty(Exception):
  '''Exception For Messages Being Empty'''
  pass

class List(commands.Cog):
  def __init__(self,bot):
    self.bot = bot 

  @commands.command(brief="Add items to a TODO List",aliases=['LA'])
  async def ListAdd (self,ctx,*message):
    'Adds to TODO list'
    name = ListAdd.__name__
    print(f"{ctx.author} running command `{name}`")
    try:
      if len(message) == 0:
        raise(MessageEmpty)
      st = datetime.now().strftime("%H:%M:%S")
      with open("TODO.txt","a") as f:
        f.write(f"{message} : {st}\n")
      await ctx.send("Todo List updated")
    except(MessageEmpty):
      await ctx.send("You didnt say what you wish to add. Please try again")


  @commands.command(brief="List Items from TODO List",aliases=['L'])
  async def List (self,ctx):
    'Lists all items In TODO List'
    name = self.__name__
    print(f"{ctx.author} running command `{name}`")
    try:
      STP = ""
      with open("TODO.txt","r") as f:
        content = f.readlines()
        if len(content) == 0:
          raise FileEmpty("Contents Found Empty")
        else:
          i = 0
          for _ in content:
            i += 1
            STP += f"{i} : `{_}`"
          await ctx.send(STP + " ")
    except(FileEmpty):
      await ctx.send('List is Empty')
          
  @commands.command(brief="Remove Items from TODO List",aliases=['LR'])
  async def ListRemove(self,ctx,Number):
    'Removes Items From TODO List'
    name = self.__name__
    print(f"{ctx.author} running command `{name}`")
    try:
      with open("TODO.txt","r+") as f:
        content = f.readlines()
        if len(content) == 0:
          raise FileEmpty
        line = content[int(Number)-1]
        print(line)
        content.remove(line)
        f.seek(0)
        f.truncate()
        for _ in content:
          f.write(_)
      if line in content:
        await ctx.send(f"Error Recieved")
      else:
        await ctx.send(f"Removed `{Number} : {line}`")
    except(IndexError):
      await ctx.send(f"This Component Does Not Exist in The List : `{str(Number)}`")
    except(FileEmpty):
      await ctx.send('List is Empty')
            
def setup(bot):
  bot.add_cog(List(bot))