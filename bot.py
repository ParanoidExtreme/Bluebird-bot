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

extensions = ['cogs.help']
for extension in extensions:
    client.load_extension(extension)

# cog status command
@client.command()
@commands.has_any_role(1411620168328810588)
async def cog_status(ctx):
    embed = disnake.Embed(
        title="Cog Status",
        description="yeet"
        )
    for ext in extensions:  
        status = "loaded" if ext in client.extensions else "not loaded"
        embed.add_field(name=ext, value=status)

    msg_author = ctx.author
    await ctx.reply(embed=embed)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        missing_roles = []
        for r in error.missing_roles:
            role = ctx.guild.get_role(r) if isinstance(r, int) else r
            missing_roles.append(role.name if role else str(r))

        await ctx.reply(
            f":x: You need one of the following roles to run this command: **{', '.join(missing_roles)}**"
        )
        return
    error_msg = str(error)
    error_file = disnake.File(fp=io.StringIO(error_msg), filename="error.txt")
    await ctx.reply(
        ":warning: **Something went really wrong... If persistent, please contact Management** :warning:",
        file=error_file
    )
    raise error



client.run(TOKEN)