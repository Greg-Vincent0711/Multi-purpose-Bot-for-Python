# Gregory Vincent
# Manfred Fong
# 12/11/21 - version 1.0 is created
# As of 12/17/21 bot is usable
# As of 1/21/22 polishing is finished

import discord
import asyncio
from discord.ext import commands
Coord_List = {} 
TOKEN = 'INSERT TOKEN HERE'
# 12月17日現在、ボットの名前はKamiです。
heavenly_blessed_denomination = "Kami"

client = commands.Bot(command_prefix='-')

#Making sure the bot joins successfully
@client.event
async def on_ready():
   print('Bot is ready!')

async def getUserInput(ctx,prompt:str,timeout=float)->str:
    def check(msg):
        return msg.author==ctx.author and msg.channel==ctx.channel

    await ctx.send(prompt)
    try:
        msg=await client.wait_for("message", check=check, timeout=timeout)
    except asyncio.TimeoutError:
        embed = discord.Embed(description = "Sorry, you didn't respond in time.", 
        color = discord.Color.dark_green())
        await ctx.send(embed = embed)
    return msg.content

async def find_Coord(ctx,prompt:str):
    if prompt in Coord_List: return Coord_List[prompt]
    elif prompt not in Coord_List:
        embed = discord.Embed(description=f"Sorry {prompt} could not be found",
        color=discord.Color.dark_green())
        await ctx.send(embed = embed)
        

@client.command(
    name = "search",
    description="searches through the dictionary for specific key"
)
async def search(ctx):
    userPrompt = await getUserInput(ctx,"Enter the name of what your looking for?",timeout=10)
    userCoords = await find_Coord(ctx,userPrompt)
    if userCoords is not None:
        embed = discord.Embed(title = f"{userPrompt}", description = 
        f"You can find this location here: {userCoords}" , color = discord.Color.dark_green())
        await ctx.send(embed = embed)    
    else:
        embed = discord.Embed(description = "We couldn't retrieve your coordinates. Sorry.", 
        color = discord.Color.dark_green())
        await ctx.send(embed = embed)

@client.command(
    name = "add",
    description = "Allows user to enter the coordinates of what they have found"
)
async def addCoord(ctx):
    location = await getUserInput(ctx,"What have you found ?",timeout=30)
    x = await getUserInput(ctx,"Enter the x Coordinate",timeout=30)
    y = await getUserInput(ctx,"Enter the y Coordinate",timeout=30)
    z = await getUserInput(ctx,"Enter the z Coordinate",timeout=30)
    Coordinates = f"[ {x}, {y}, {z} ]"
    if location in Coord_List.keys():
        await ctx.send("Coordinates with this name already exist. Please enter a different name.")
    else:
        Coord_List[location] = Coordinates
        embed = discord.Embed(title = "Coordinates Added", description = f"{location} :  {Coordinates}",
        color = discord.Color.dark_green())
        await ctx.send(embed = embed)

@client.command(
    name = "list",
    description="shows user the saved list coordinates"
)
async def show(ctx):
    if len(Coord_List)==0:
        embed = discord.Embed(
        description = "No coordinates saved.", 
        color = discord.Color.dark_green())
        await ctx.send(embed = embed)  
    else:
        output=' '.join(['{0}  :  {1}\n'.format(key, value) for (key, value) in Coord_List.items()])
        embed = discord.Embed(title = "Saved Coordinates",
        description = f"{output}",
        color = discord.Color.dark_green())
        await ctx.send(embed = embed)

@client.command(
    name="clear",
    description="Clears all inputs"  
)  
async def clear(ctx):
    if len(Coord_List)==0:
        embed = discord.Embed(description = "No Coordinates found.", 
        color = discord.Colour.dark_green())
        await ctx.send(embed = embed) 
    else:
        Coord_List.clear()
        embed = discord.Embed(description = "Successfully cleared all entries.", 
        color = discord.Color.dark_green())
        await ctx.send(embed = embed)

@client.command(
    name="remove",
    description="Removes user selected elements from list"
)
async def remove(ctx):
    userPrompt = await getUserInput(ctx,"Enter the name of what you want to remove from the list",timeout=30)
    removeVal = await find_Coord(ctx,userPrompt)
    for key,value in Coord_List.items():
        if value==removeVal:
            Coord_List.pop(key)
        break
    embed = discord.Embed(title = f"{userPrompt}", description = 
    "Your element has been removed from the list" , color = discord.Color.dark_green())
    await ctx.send(embed = embed)    


@client.command(
    name = 'commands',
    description = 'Display a message for all the commands you can do'
)
async def assistance(ctx):
    embed=discord.Embed(
        title="Commands",
        description="Here is a list of my commands",
        colour=discord.Colour.dark_green()
    )
    embed.add_field(name="-add",value="Add a coordinate to the bot's dictionary",inline=False)
    embed.add_field(name="-remove",value="Remove a coordinate from the bot ",inline=False) 
    embed.add_field(name="-search", value="Search for a particular element in the bot's dictionary ",inline=False)
    embed.add_field(name="-list",value="Show all coordinates saved ",inline=False)
    embed.add_field(name="-clear",value="Removes all coordinates",inline=False)
    await ctx.send(embed = embed)
    

@client.command(
    name = "kill",
    description = "Gently puts the bot to sleep"
)
async def shutdown(ctx):
    await ctx.send("Killing the bot...")
    await ctx.bot.logout()
client.run(TOKEN)  
