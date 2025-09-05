import disnake
import json
from disnake.ext import commands

with open("config.json", "r") as f:
    config = json.load(f)

class Help(commands.Cog):
      client = commands
      def __init__(self, client):
        self.client = client

      @commands.Cog.listener()
      async def on_ready(self):
        print(f'Help Cog is online.')

      @commands.slash_command()
      @commands.has_any_role(*config["roles"]["executive+"])
      async def test(self, inter):
        await inter.response.send_message("hello", ephemeral=True)

def setup(bot):
    bot.add_cog(Help(bot))