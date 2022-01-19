# FunCommands.py
import re
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
    @commands.command(name="randomquote", brief="Send a random quote")
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
    @commands.command(name="randomactivity", brief="Send a random activity")
    async def random_activity(self, ctx):
        embed = discord.Embed(color=discord.Colour.from_rgb(255,192,203))

        async with ctx.typing():
            # send get request, convert response to string, and load url
            response = requests.get("https://www.boredapi.com/api/activity/")
            activity = json.loads(response.text)
            if response:
                embed.title = "Random Activity You Can Do!"
                embed.description = activity["activity"]
                embed.add_field(name="Type of Activity:", value=activity["type"], inline=False)
                embed.add_field(name="Number of Participant(s):", value=activity["participants"], inline=False)
                embed.set_footer(text=f"Requested by {ctx.author.name}")
            else:
                embed.description = "Error occured. Couldn't get random activity. ⛔"
            await ctx.send(embed=embed)

    # bot command (-apod)
    # summary: display NASA's APOD (Astronomy Picture of the Day) and information about it
    @commands.command(name="apod", brief="Display NASA's APOD (Astronomy Picture of the Day)")
    async def apod(self, ctx):
        embed = discord.Embed(color=discord.Colour.from_rgb(255,192,203))

        # send get request, convert response to string, and load url
        response = requests.get("https://api.nasa.gov/planetary/apod?api_key=" + config.NASA_KEY)
        pic = json.loads(response.text)
        if response:
            embed.title = pic["title"]
            embed.description = pic["explanation"]
            embed.set_image(url=pic["hdurl"])
            embed.set_footer(text=f"Requested by {ctx.author.name}")
        else:
            embed.description = "Error occured. Couldn't get APOD. ⛔"
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(FunCommands(bot))