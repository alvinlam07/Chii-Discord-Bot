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
            embed.title = "Random Quote For You!"
            embed.description = quote["content"] + "\n-" + quote["author"]
            embed.set_footer(text=f"Requested by {ctx.author.name}")
        else:
            embed.description = "Error occured. Couldn't get random quote. ⛔"
        await ctx.send(embed=embed)

    # bot command (-randomactivity)
    # summary: send a random activity
    @commands.command(name="randomactivity")
    async def random_activity(self, ctx):
        embed = discord.Embed(color=discord.Colour.from_rgb(255,192,203))

        async with ctx.typing():
            # send get request, convert response to string, and load url
            response = requests.get("https://www.boredapi.com/api/activity/")
            activity = json.loads(response.text)
            if response:
                embed.title = "Random Activity You Can Do!"
                embed.description = activity["activity"]
                embed.add_field(name="Type of Activity:", value=activity["type"])
                embed.add_field(name="Number of Participant(s):", value=activity["participants"])
                embed.set_footer(text=f"Requested by {ctx.author.name}")
            else:
                embed.description = "Error occured. Couldn't get random activity. ⛔"
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(FunCommands(bot))