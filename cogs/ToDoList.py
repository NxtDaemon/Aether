from discord.ext import commands 
import time
import discord
from __main__ import logger
import random

#+++++++++++++++++++++++++++++++++++++++++++++Exceptions+++++++++++++++++++++++++++++++++++++++++++++++++++#

class FileEmpty(Exception):
    'Exception for Files Being Empty'
    pass

class ParameterEmpty(Exception):
    'Exception For Messages Being Empty'
    pass

class IdError(Exception):
    'Exception class for ids'
    pass

class ItemNotFound(Exception):
    'Exception for '
    pass

#++++++++++++++++++++++++++++++++++++++++++++++Exceptions++++++++++++++++++++++++++++++++++++++++++++++++++#

#+++++++++++++++++++++++++++++++++++++++++++Custom Functions+++++++++++++++++++++++++++++++++++++++++++++++#

async def FileEmptyCheck(FileListObj,ctx):
    'Manage Empty File Checks'
    name = "FileEmptyCheck"
    try:
        if len(FileListObj) == 0:
            logger.info("FileObj Detected Empty")
            await ctx.send('List is Empty')
            return(1)
    except(Exception) as Exc:
        logger.error(f"Uncaught Exception in Module : `{name}`, ErrorType : `{type(Exc)}` : {Exc}")
    else:
        return(0)

async def ParameterEmptyCheck(Parameter,ctx):
    'Manage Empty Message Checks'
    name = "ParameterEmptyCheck"
    try:
        if len(Parameter) == 0:
            logger.info("Required Parameter Detected Empty")
            await ctx.send("A parameter was not set. Please try again")
            return(1)
    except(Exception) as Exc:
        logger.error(f"Uncaught Exception in Module : `{name}`, ErrorType : `{type(Exc)}` : {Exc}")
    else:
      return(0)

async def IntCheck(TypeObj):
    'Manage if something is an Int'
    name = "IntCheck"
    try:
      TypeObj = int(TypeObj)
      return(0)
    except(ValueError):
      return(1)
    except(Exception) as Exc:
        logger.error(f"Uncaught Exception in Module : `{name}`, ErrorType : `{type(Exc)}` : {Exc}")
    else:
      return(1)

async def IDCheck(ID):
    'Only Let "Gods" Use the Command'
    with open("Gods.txt","r+") as f:
        GodIDList = f.readlines()
    if str(ID) in GodIDList:
        return(0)
    elif str(ID) == "539928505488506882":
        return(0)
    else: 
        return(1)

#+++++++++++++++++++++++++++++++++++++++++++Custom Functions+++++++++++++++++++++++++++++++++++++++++++++++#

#+++++++++++++++++++++++++++++++++++++++++++++++Main Code++++++++++++++++++++++++++++++++++++++++++++++++++#

class ToDoList(commands.Cog):
  def __init__(self,bot):
    self.bot = bot 

  @commands.command(brief="Manage Gods")
  async def God(self,ctx,mode,user : discord.Member):
    'Add and Remove people from GOD List'
    name = "God"
    logger.debug(f"{ctx.author} running command `{name}`")

    try:
        if await IDCheck(ctx.author.id) : raise IdError()

        if mode.lower() == "add":
            with open("Gods.txt","a+") as f:
                if str(user.id) in f.readlines():
                    await ctx.send("You are already God Status")
                f.write(str(user.id)+"\n")
                await ctx.send(f"{user} is now God Status")

        elif mode.lower() == "remove":
            with open("Gods.txt","r+") as f:
                content = f.read().splitlines()
                if str(user.id) not in content: raise ItemNotFound()
                content.remove(str(user.id))
                f.seek(0)
                f.truncate()
                if(content):
                    for _ in content:
                        f.write(f"{_}\n")

    except(ItemNotFound,IdError,TypeError) as Exc:
        if type(Exc) == ItemNotFound:
            await ctx.send("User Was Not Found In Gods Files")
        elif type(Exc) == IdError:
            await ctx.send("You aren't permitted to use this command.")
        elif type(Exc) == TypeError:
            logger.info("Gods file is now empty")

    except(Exception) as Exc:
        logger.error(f"Uncaught Exception in Module : `{name}`, ErrorType : `{type(Exc)}` : {Exc}")


  @commands.command(brief="Add items to a TODO List",aliases=['la'])
  async def ListAdd (self,ctx,*message : str ):
    'Adds to TODO list'
    name = "ListAdd"
    logger.debug(f"{ctx.author} running command `{name}`")

    try:
        if await IDCheck(ctx.author.id) : raise (IdError)
        if await ParameterEmptyCheck(message,ctx) : raise (ParameterEmpty)
        HRT = time.asctime()
        MessageString = ""
        for _ in message:
            MessageString += f" {_}"
        with open("ToDoList.txt","a") as f:
            f.write(f"{MessageString} : {HRT}\n")
        await ctx.send("Todo List updated")

    except(ParameterEmpty,IdError) as Exc:
        if type(Exc) == IdError:
            await ctx.send("You aren't permitted to use this command.")
        pass

    except(Exception) as Exc:
        logger.error(f"Uncaught Exception in Module : `{name}`, ErrorType : `{type(Exc)}` : {Exc}")

  @commands.command(brief="List Items from TODO List",aliases=['l'])
  async def List (self,ctx):
    'Lists all items In TODO List'
    name = "List"
    logger.debug(f"{ctx.author} running command `{name}`")

    try:
        if await IDCheck(ctx.author.id) : raise(IdError)
        STP = ""
        with open("ToDoList.txt","r") as f:
            content = f.readlines()
            if await FileEmptyCheck(content,ctx) : raise(FileEmpty)
            for i, _ in enumerate(content,1):
                STP += f"{i} : `{_}`"
            await ctx.send(STP + " ")

    except(FileEmpty,IdError) as Exc:
        if type(Exc) == IdError:
            await ctx.send("You aren't permitted to use this command.")
        pass

    except(Exception) as Exc:
        logger.error(f"Uncaught Exception in Module : `{name}`, ErrorType : `{type(Exc)}` : {Exc}")
   
  @commands.command(brief="Remove Items from TODO List",aliases=['lr'])
  async def ListRemove(self,ctx,Number):
    'Removes Items From TODO List'
    name = "ListRemove"
    logger.debug(f"{ctx.author} running command `{name}`")

    try:
        with open("ToDoList.txt","r+") as f:
            content = f.readlines()
            if await IDCheck(ctx.author.id) : raise(IdError)
            if await FileEmptyCheck(content,ctx) : raise(FileEmpty)
            if await ParameterEmptyCheck(Number,ctx) : raise(ParameterEmpty)
            if await IntCheck(Number) : raise(ValueError)
            line = content[int(Number)-1]
            content.remove(line)
            f.seek(0)
            f.truncate()
            for _ in content:
                _.strip("\n")
                f.write(f"{_}")
            if line in content:
                await ctx.send(f"Error Recieved")
            else:
                await ctx.send(f"Removed `{Number} : {str(line)}`")
                
    except(FileEmpty,ParameterEmpty,ValueError,IndexError,IdError) as Exc:
        logger.debug(f"Caught `{type(Exc)}` in `{name}`")
        if type(Exc) == IdError:
            await ctx.send("You aren't permitted to use this command.")
        elif type(Exc) == IndexError:
            await ctx.send(f"This Component Does Not Exist in The List : `{str(Number)}`")
        elif type(Exc) == ValueError:
            await ctx.send(f"Parameter `{Number}` is not an Integer")
    except(Exception) as Exc:
        logger.error(f"Uncaught Exception in Module : `{name}`, ErrorType : `{type(Exc)}` : {Exc}")

  @commands.command(brief="Randomly Select From List",aliases=["rand"])
  async def Random(self,ctx):
    'Randomly Selected an item from the list'
    name = "Random"
    logger.debug(f"{ctx.author} running command `{name}`")
    try:
        if await IDCheck(ctx.author.id) : raise IdError()
        with open("ToDoList.txt","r+") as f:
            content = f.readlines()
            choice = random.choice(content)
            choice = choice.strip("\n")
            await ctx.send(f"`{choice}` || was selected :D")
    except(FileEmpty,IdError) as Exc:
        if type(Exc) == IdError:
            await ctx.send("You aren't permitted to use this command.")
        await ctx.send("File is empty")
    except(Exception) as Exc:
        logger.error(f"Uncaught Exception in Module : `{name}`, ErrorType : `{type(Exc)}` : {Exc}")

  @commands.command(brief="RemoveAll from list",aliases=["Rem-All"])
  async def RemoveAll(self,ctx):
    'Removes all from list'
    name = "RemoveAll"
    logger.debug(f"{ctx.author} running command `{name}`")
    try:
        if await IDCheck(ctx.author.id) : raise IdError()
        with open("ToDoList.txt","r+") as f:
            content = f.readlines()
            if await FileEmptyCheck(content,ctx) : raise(FileEmpty)
            f.seek(0)
            f.truncate()
            await ctx.send("ToDoList Has Been Cleared")
    except(FileEmpty,IdError):
        if type(Exc) == IdError:
            await ctx.send("You aren't permitted to use this command.")
        pass
    except(Exception) as Exc:
        logger.error(f"Uncaught Exception in Module : `{name}`, ErrorType : `{type(Exc)}` : {Exc}")
    else:
        logger.debug(f"{ctx.author} running command `{name}`")
        await ctx.send("Sorry you dont have permission to do this.")

def setup(bot):
    bot.add_cog(ToDoList(bot))

def teardown(bot):
    logger.debug(cog_name)

#+++++++++++++++++++++++++++++++++++++++++++++++Main Code++++++++++++++++++++++++++++++++++++++++++++++++++#
