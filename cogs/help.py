import disnake
from disnake.ext import commands

class Help(commands.Cog):
      client = commands
      def __init__(self, client):
        self.client = client
        self.slash_command_interactions = {}
        self.timers = {}

      @commands.Cog.listener()
      async def on_ready(self):
       print(f'Help Cog is online.')

def setup(bot):
    bot.add_cog(Help(bot))