from discord.ext import commands 
from datetime import datetime

# List Exceptions
class FileEmpty(Exception):
  '''Exception for File's being empty '''
  pass

class List(commands.Cog):
  def __init__(self,bot):
    self.bot = bot 

  @commands.command(brief="Add items to a TODO List",aliases=['LA','L-A'])
  async def ListAdd (self,ctx,message):
    'Adds to TODO list'
    st = datetime.now().strftime("%H:%M:%S")
    print(message)
    with open("TODO.txt","a") as f:
      f.write(f"{message} : {st}\n")
    await ctx.send("Todo List updated")

  @commands.command(brief="List Items from TODO List"aliases=['L','l'])
  async def List (self,ctx):
     'Lists all items In TODO List'
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
          
  @commands.command(brief="Remove Items from TODO List"aliases=['',''])
  async def ListRemove(self,ctx,Number):
    'Removes Items From TODO List'
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
            
def setup(bot):
  bot.add_cog(List(bot))