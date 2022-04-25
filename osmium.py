import discord, tomli, tomli_w, os
from discord.ext import commands

with open("config.toml", "rb") as Config:
    Conf = tomli.load(Config)

uConf = Conf["universal"]
dConf = Conf["discord"]

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=dConf["prefix"], intents=intents, activity=discord.Activity(type=discord.ActivityType.listening, name="my bones snap"), help_command=None, status=discord.Status.dnd)

def embedCreator(title, desc, color):
    embed = discord.Embed(
        title=f"{title}",
        description=f"{desc}",
        color=color
    )
    return embed

#stops the bot from running (away from you and your computer while you try not to beat it with a stick)
@bot.command()
async def stop(ctx):
    await ctx.send(embed=embedCreator("Stopping", "Shutting Down Osmium.py", 0xFF0000))
    await bot.close()

@bot.command()
async def reload(ctx, command = None):
    if not command:
        try:
            await ctx.send(embed=embedCreator("Reload", "Reloading all commands", 0x00FF00))
            for file in os.listdir("./cogs"):
                if file.endswith(".py"):
                    bot.reload_extension(f"cogs.{file[:-3]}")
        except Exception as e:
            await ctx.send(embed=embedCreator("Failed to Reload", f"{e}", 0xFF0000))

    else:
        try:
            await ctx.send(embed=embedCreator("Reload", f"Reloading {command}", 0x00FF00))
            bot.reload_extension(f"cogs.{command}")
        except Exception as e:
            await ctx.send(embed=embedCreator(f"Failed to Reload {command}", f"{e}", 0xFF0000))

@bot.command()
async def load(ctx, command = None):
    if not command:
        await ctx.send(embed=embedCreator("Error", "Provide a command to load!", 0xFF0000))
    else:
        try:
            await ctx.send(embed=embedCreator("Load", f"Loading {command}", 0x00FF00))
            bot.load_extension(f"cogs.{command}")
        except Exception as e:
            await ctx.send(embed=embedCreator(f"Failed to Load {command}", f"{e}", 0xFF0000))

@bot.command()
async def unload(ctx, command = None):
    if not command:
        await ctx.send(embed=embedCreator("Error", "Provide a command to unload!", 0xFF0000))
    else:
        try:
            await ctx.send(embed=embedCreator("Unload", f"Unloading {command}", 0x00FF00))
            bot.unload_extension(f"cogs.{command}")
        except Exception as e:
            await ctx.send(embed=embedCreator(f"Failed to Unload {command}", f"{e}", 0xFF0000))

# load cogs on startup
for filename in sorted(os.listdir('./cogs/')):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(dConf["token"])
