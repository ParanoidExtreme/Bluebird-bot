import disnake
import json
from disnake.ext import commands

with open("config.json", "r") as f:
    config = json.load(f)

class Design(commands.Cog):
      client = commands
      def __init__(self, client):
        self.client = client

      @commands.Cog.listener()
      async def on_ready(self):
        print(f'Design Cog is online.')
      
      @commands.slash_command(description="Used to log an order upon completion")
      @commands.has_any_role(*config["roles"]["support+"])
      async def log_order(
            self, inter, designer : disnake.Member = commands.Param(description="The designer whom finished an order"),
            order_total : str = commands.Param(description="Order Total"),
            order_item : str = commands.Param(description="Quantity & Item Bought"),
            service_charge : str = commands.Param(description="Service Fee (%)", choices={"10%": "1.10", "5%": "1.05"}),
            order_id : int = commands.Param(description="Ticket ID REQUIRED")
            ):

        if not order_total.startswith("$"):
            try:
                float(order_total)
            except:
                embed = disnake.Embed(title="Something went wrong", description="Invalid pricing format \n\nPlease use one the following formats:", colour=0xff0000)
                embed.set_thumbnail(url="https://media.discordapp.net/attachments/1413529440469782599/1413652483456110743/error-icon-4.png?ex=68bcb5f8&is=68bb6478&hm=5354b5fee887eb8beb48d2e69cdcc4c3589a681411116df3ee727c10383864d0&=&format=webp&quality=lossless")
                embed.add_field(name="Robux (R$)", value="Basic numerals (ex. **0** or **0.00**).", inline=False)
                embed.add_field(name="Dollar ($)", value="Dollar sign **'$'** followed by basic numerals (ex. **$0** or **$0.00**).", inline=False)
                await inter.response.send_message(embed=embed)
                return
        else:
            order_total = float(order_total.replace("$", ""))
            
        embed = disnake.Embed(title="Order Log")
        embed.add_field(name="Designer", value=designer.mention)
        embed.add_field(name="Order Total", value=order_total)
        embed.add_field(name="Ordered item", value=order_item)
        embed.add_field(name="Service charge rate", value=service_charge)
        embed.add_field(name="Order ID", value=order_id)

        await inter.response.send_message(designer.mention, embed=embed, ephemeral=False)

def setup(bot):
    bot.add_cog(Design(bot))