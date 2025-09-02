import os
os.system("cls")

import disnake
from disnake.ext import commands
from dotenv import load_dotenv
import io

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

client.load_extension('cogs.help')

@client.command()
@commands.has_any_role(1411620168328810588)
async def cog_status(ctx):
    msg_author = ctx.author
    await ctx.reply(msg_author.mention)

@cog_status.error
async def cog_status_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        await ctx.reply(":x: **Missing permission to run command**")
        return
    error_msg = str(error)
    file = disnake.File(fp=io.StringIO(error_msg), filename="error.txt")
    await ctx.reply(f":warning: **Something went really wrong... If persistant please contact Management** :warning:", file=file)
    raise error

client.run(TOKEN)