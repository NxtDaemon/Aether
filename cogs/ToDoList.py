from discord.ext import commands 
import time
import discord
from Main import logger, RecordUser
import random,os

#++++++++++++++++++++++++++++++++++++++++++ < Exceptions > ++++++++++++++++++++++++++++++++++++++++++++++++#

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
    'Exception for Items Not being found in an index'
    pass

#+++++++++++++++++++++++++++++++++++++++++ < Custom Functions > ++++++++++++++++++++++++++++++++++++++++++++#

async def FileEmptyCheck(FileListObj,ctx):
    'Manage Empty File Checks'
    try:
        if len(FileListObj) == 0:
            logger.info("FileObj Detected Empty")
            await ctx.send('List is Empty')
            return(1)
    except(Exception) as Exc:
        logger.error(f"Uncaught Exception in Module : `FileEmptyCheck`, ErrorType : `{type(Exc)}` : {Exc}")
    else:
        return(0)

async def ParameterEmptyCheck(Parameter,ctx):
    'Manage Empty Message Checks'
    try:
        if len(Parameter) == 0:
            logger.info("Required Parameter Detected Empty")
            await ctx.send("A parameter was not set. Please try again")
            return(1)
    except(Exception) as Exc:
        logger.error(f"Uncaught Exception in Module : `ParameterEmptyCheck`, ErrorType : `{type(Exc)}` : {Exc}")
    else:
      return(0)

async def IntCheck(TypeObj):
    'Manage if something is an Int'
    try:
      TypeObj = int(TypeObj)
      return(0)
    except(ValueError):
      return(1)
    except(Exception) as Exc:
        logger.error(f"Uncaught Exception in Module : `IntCheck`, ErrorType : `{type(Exc)}` : {Exc}")
    else:
      return(1)

async def IDCheck(ID):
    'Only Let "Auth" Users use the Command'
    ID = str(ID) + "\n"
    with open("Auth.txt","r+") as f:
        AuthIDList = f.readlines()
    if str(ID) in AuthIDList:
        return(0)
    elif str(ID) == "539928505488506882":
        return(0)
    else: 
        return(1)

async def GetActiveName(id):
    with open(f"Lists/{id}/Active.txt") as f:
        Active = f.read()
    return(f"Lists/{id}/{Active}")

#+++++++++++++++++++++++++++++++++++++++++++++ < Main Code > ++++++++++++++++++++++++++++++++++++++++++++++#

class ToDoList(commands.Cog):
    def __init__(self,bot):
        self.bot = bot 

    @commands.command(brief="Remove Items from TODO List",aliases=['sl'])
    @commands.before_invoke(RecordUser)
    async def SetList(self,ctx,Listname):
        AttemptFilename = f"{Listname}-{ctx.author.id}.ToDo"
        if AttemptFilename in os.listdir(f"Lists/{ctx.author.id}/"):
            with open(f"Lists/{ctx.author.id}/Active.txt","+a") as f:
                f.seek(0)
                f.truncate()
                f.write(f"{Listname}-{ctx.author.id}.ToDo")
            await ctx.send("You're Active File has been Updated")
        else:
            await ctx.send("This List Doesn't Exist Sorry")

    @commands.command(brief="Show All of your lists",aliases=["ml"])
    @commands.before_invoke(RecordUser)
    async def MyLists(self,ctx):
        Lists = os.listdir(f"Lists/{ctx.author.id}/")
        Lists.remove("Active.txt")
        DisplayableLists = []
        for _ in Lists:
            DisplayableLists.append(_.replace(f"-{ctx.author.id}.ToDo",""))
            embed = discord.Embed(title="Your Lists",description="\n".join(DisplayableLists),color=0x0000ff)
        await ctx.send(embed=embed)

    @commands.command(brief="Manage Authed",aliases=["authmem","am"])
    @commands.before_invoke(RecordUser)
    async def AuthMember(self,ctx,mode,user : discord.Member):
        'Add and Remove people from Authed List'
        try:
            if await IDCheck(ctx.author.id) : raise IdError()

            if mode.lower() == "add":
                with open("Auth.txt","a+") as f:
                    if str(user.id) in f.readlines():
                        await ctx.send("You are already Auth Status")
                    f.write(str(user.id)+"\n")
                    await ctx.send(f"{user} is now Auth Status")

            elif mode.lower() == "remove":
                with open("Auth.txt","r+") as f:
                    content = f.read().splitlines()
                    if str(user.id) not in content: raise ItemNotFound()
                    content.remove(str(user.id))
                    f.seek(0)
                    f.truncate()
                    if(content):
                        for _ in content:
                            f.write(f"{_}\n")

        except(Exception) as Exc:
            if type(Exc) == ItemNotFound:
                await ctx.send("User Was Not Found In Auth.txt File")
            elif type(Exc) == IdError:
                await ctx.send("You aren't permitted to use this command.")
            elif type(Exc) == TypeError:
                logger.info("Auth file is now empty")
            else:
                pass

    @commands.command(brief="Authorize An Entire Role",aliases=["ar","authrole"])
    @commands.before_invoke(RecordUser)
    async def AuthRole(self,ctx,Role : discord.Role):
        for User in Role.members:
            with open("Auth.txt","a+") as f:
                f.write(str(User.id)+"\n")
                await User.send(f"Due to being a Member of the `{Role}` Role in `{User.guild}` \nYou Have Been Given Auth Status to use the Bot, Enjoy your day :)") 
        await ctx.send(f"`{Role}` Members Have Now Been Given Auth Status")
            
    @commands.command(brief="Add items to a TODO List",aliases=['la'])
    @commands.before_invoke(RecordUser)
    async def ListAdd (self,ctx,*message : str ):
        'Adds to TODO list'
        try:
            if await IDCheck(ctx.author.id) : raise (IdError)
            if await ParameterEmptyCheck(message,ctx) : raise (ParameterEmpty)
            HRT = time.asctime()
            MessageString = ""
            for _ in message:
                MessageString += f" {_}"
            Filename = await GetActiveName(ctx.author.id)
            with open(f"{Filename}","a") as f:
                f.write(f"{MessageString} : {HRT}\n")
            await ctx.message.add_reaction('☑️')

        except(ParameterEmpty,IdError) as Exc:
            if type(Exc) == IdError:
                await ctx.send("You aren't permitted to use this command.")
            pass

        except(Exception) as Exc:
            pass

    @commands.command(brief="List Items from TODO List",aliases=['l'])
    @commands.before_invoke(RecordUser)
    async def List (self,ctx):
        try:
            if await IDCheck(ctx.author.id) : raise(IdError)
            STP = ""
            FileName = await GetActiveName(ctx.author.id)
            with open(FileName,"r") as f:
                content = f.readlines()
                if await FileEmptyCheck(content,ctx) : raise(FileEmpty)
                for i, _ in enumerate(content,1):
                    STP += f"{str(i).rjust(3)} : `{_}`"
                EmbedFileName = FileName.split("/")[2]
                EmbedFileName = EmbedFileName.replace(f"-{ctx.author.id}.ToDo","")
                embed = discord.Embed(title=f"{EmbedFileName}",description=STP,color=0x0000ff)
                await ctx.send(embed=embed)

        except(FileEmpty,IdError) as Exc:
            if type(Exc) == IdError:
                await ctx.send("You aren't permitted to use this command.")
            
        except(Exception) as Exc:
            pass

    @commands.command(brief="Remove Items from TODO List",aliases=['lr'])
    @commands.before_invoke(RecordUser)
    async def ListRemove(self,ctx,Number):
        'Removes Items From TODO List'
        try:
            Filename = await GetActiveName(ctx.author.id) 
            with open(f"{Filename}","r+") as f:
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
            logger.debug(f"Caught `{type(Exc)}` in `{ctx.command}`")
            if type(Exc) == IdError:
                await ctx.send("You aren't permitted to use this command.")
            elif type(Exc) == IndexError:
                await ctx.send(f"This Component Does Not Exist in The List : `{str(Number)}`")
            elif type(Exc) == ValueError:
                await ctx.send(f"Parameter `{Number}` is not an Integer")
        except(Exception) as Exc:
            pass

    @commands.command(brief="Randomly Select From List",aliases=["rand"])
    @commands.before_invoke(RecordUser)
    async def Random(self,ctx):
        'Randomly Selected an item from the list'
        try:
            if await IDCheck(ctx.author.id) : raise IdError()
            Filename = await GetActiveName(ctx.author.id)
            with open(f"{Filename}","r+") as f:
                content = f.readlines()
                if await FileEmptyCheck(content,ctx) : raise FileEmpty()
                choice = random.choice(content)
                choice = choice.strip("\n")
                await ctx.send(f"`{choice}` || was selected :D")
        except(FileEmpty,IdError) as Exc:
            if type(Exc) == IdError:
                await ctx.send("You aren't permitted to use this command.")
        except(Exception) as Exc:
            pass

    @commands.command(brief="RemoveAll from list",aliases=["Rem-All"])
    @commands.before_invoke(RecordUser)
    async def RemoveAll(self,ctx):
        'Removes all from list'
        try:
            if await IDCheck(ctx.author.id) : raise IdError()
            Filename = await GetActiveName(ctx.author.id)
            with open(f"{Filename}","r+") as f:
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
            pass
        else:
            await ctx.send("Sorry you dont have permission to do this.")

    @commands.command(brief="Create a users ToDoList",aliases=["r","remove"])
    @commands.before_invoke(RecordUser)       
    async def Remove(self,ctx,name=None):
        'Remove a Users to do list'
        FileName = f"{name}-{ctx.author.id}.ToDo"
        if name == None: await ctx.send("Name Parameter Not Set") ; return()
        if os.path.isdir(f"Lists/{ctx.author.id}"):
            if os.path.isfile(f"Lists/{ctx.author.id}/{FileName}"):
                os.remove(f"Lists/{ctx.author.id}/{FileName}")
                await ctx.send (f"Removed List under name `{FileName}`")
            else: 
                await ctx.send(f"{name} was not found in your lists folder")
        else: 
            await ctx.send("your folder does not exist please run the `create` command ")

    @commands.command(brief="Create a users ToDoList",aliases=["c","create"])
    @commands.before_invoke(RecordUser)
    async def Create(self,ctx,name="Main"):
        'Setup for a user\'s to do list'
        if os.path.isdir(f"Lists/{ctx.author.id}"):
            try:
                if name == "Main" :
                    with open(f"Lists/{ctx.author.id}/Active.txt","+a") as ActiveFile:
                        ActiveFile.write(f"{name}-{ctx.author.id}.ToDo")
                        logger.debug(f"instantiated Active File for {ctx.author}")
                FileName = f"Lists/{ctx.author.id}/{name}-{ctx.author.id}.ToDo"
                if os.path.isfile(FileName) : await ctx.send(f"List Already Exists under name `{FileName}` ") ; return()
                file = open(FileName,"+a")
                await ctx.send(f"List Created Under Name `{FileName}`")
            except(Exception) as Exc:
                logger.info(f"{Exc}")
        else: 
            os.mkdir(f"Lists/{ctx.author.id}")
            await ctx.send("Your Folder has been created, please re-run command.")
        
def setup(bot):
    logger.debug("| Loaded ToDoList | ")
    bot.add_cog(ToDoList(bot))

def teardown(bot):
    logger.debug("| Unloaded ToDoList | ")
    bot.remove_cog(ToDoList(bot))     

