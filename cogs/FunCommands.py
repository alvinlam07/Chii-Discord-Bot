# FunCommands.py
import discord, os, sys, requests, json
from discord.ext import commands
if not os.path.isfile("config.py"):
	sys.exit("'config.py' could not be found. Add the file and try again.")
else:
	import config

class FunCommands(commands.Cog):
    def _init_(self, bot):
        self.bot = bot
    
    # bot command (-randomquote)
    # summary: send a random quote
    @commands.command(name="randomquote")
    async def random_quote(self, ctx):
        embed = discord.Embed(color=discord.Colour.from_rgb(255,192,203))

        # send get request, convert response to string, and load url
        response = requests.get("https://api.quotable.io/random")
        quote = json.loads(response.text)
        if response:
            embed.title = quote["author"]
            embed.description = quote["content"]
            embed.set_footer(text=f"Requested by {ctx.author.name}")
        else:
            embed.description = "Error occured. Couldn't get random quote. ⛔"
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(FunCommands(bot))