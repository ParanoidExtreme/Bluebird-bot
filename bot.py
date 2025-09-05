import os
os.system("cls")

# imports
import disnake
import json
from disnake.ext import commands
from dotenv import load_dotenv

# load error_handler functions
from error_handler import handle_generic_error, handle_missing_roles

# load config file
with open("config.json", "r") as f:
    config = json.load(f)

# load enviorment variables from .env file
load_dotenv('.env')

# set constant "TOKEN" with app token
TOKEN = os.getenv('DISCORD_TOKEN')

# set disnake intents
intents = disnake.Intents.all()
intents.members = True

client = commands.Bot(command_prefix='.', intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user.id}')

extensions = ['cogs.help', 'cogs.design']
for extension in extensions:
    client.load_extension(extension)

# cog status command
@client.command()
@commands.has_any_role(config["roles"]["ownership-only"])
async def cog_status(ctx):
    embed = disnake.Embed(
        title="Cog Status"
        )
    for ext in extensions:  
        status = "loaded" if ext in client.extensions else "not loaded"
        embed.add_field(name=ext, value=status)

    msg_author = ctx.author
    await ctx.reply(embed=embed)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        await handle_missing_roles(ctx, error, is_inter=False)
        return
    elif isinstance(error, commands.CommandNotFound):
        return
    await handle_generic_error(ctx, error, is_inter=False)
    raise error


@client.event
async def on_slash_command_error(inter, error):
    if isinstance(error, commands.MissingAnyRole):
        await handle_missing_roles(inter, error, is_inter=True)
        return
    elif isinstance(error, commands.CommandNotFound):
        return
    await handle_generic_error(inter, error, is_inter=True)
    raise error



client.run(TOKEN)