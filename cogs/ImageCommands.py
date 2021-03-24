# ImageCommands.py
import discord, os, sys, random, asyncpraw, asyncprawcore, requests, json
from discord.ext import commands
if not os.path.isfile("config.py"):
	sys.exit("'config.py' could not be found. Add the file and try again.")
else:
	import config

# initialize the random number generator
random.seed
class ImageCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # bot command (-memes)
    # summary: display a meme image from r/memes subreddit
    @commands.command(name="memes")
    async def memes(self, ctx):
        # reddit authentication
        r_auth = asyncpraw.Reddit(
            client_id=config.REDDIT_CLIENT_ID, 
            client_secret=config.REDDIT_SECRET, 
            user_agent=config.REDDIT_NAME
        )

        async with ctx.typing():
            post_list = []
            sr = await r_auth.subreddit("memes") # get post info from subreddit
            async for post in sr.hot():
                post_list.append([post.title, post.shortlink, post.url])

            random_post = random.choice(post_list)

            embed = discord.Embed(
                title=random_post[0],
                url=random_post[1],
                color=discord.Colour.from_rgb(255,192,203)
            )
            embed.set_image(url=random_post[2])
            embed.set_footer(text=f"Requested by {ctx.author.name}")
            await ctx.send(embed=embed)

    # bot command (-dog)
    # summary: display a cute dog image
    @commands.command(name="dog")
    async def dog(self, ctx):
        embed = discord.Embed(color=discord.Colour.from_rgb(255,192,203))

        # send get request, convert response to string, and load url
        response  = requests.get("https://dog.ceo/api/breeds/image/random")
        dog_image = json.loads(response.text)
        print(dog_image)
        if response:
            embed.title = "🐶🐶🐶"
            embed.set_image(url=dog_image["message"])
            embed.set_footer(text=f"Requested by {ctx.author.name}")
        else:
            embed.description="Error occured. Couldn't get dog image. ⛔"
        await ctx.send(embed=embed)
        
    # bot command (-cat)
    # summary: display a cute cat image
    @commands.command(name="cat")
    async def cat(self, ctx):
        embed = discord.Embed(color=discord.Colour.from_rgb(255,192,203))

        # send get request, convert response to string, and load url
        response  = requests.get("https://api.thecatapi.com/v1/images/search")
        cat_image = json.loads(response.text)
        if response:
            embed.title = "🐱🐱🐱"
            embed.set_image(url=cat_image[0]["url"])
            embed.set_footer(text=f"Requested by {ctx.author.name}")
        else:
            embed.description = "Error occured. Couldn't get cat image. ⛔"
        await ctx.send(embed=embed)

    # bot command (-waifu)
    # summary: display a cute waifu image
    @commands.command(name="waifu")
    async def waifu(self, ctx):
        embed = discord.Embed(color=discord.Colour.from_rgb(255,192,203))

        amiru_url = "https://animu.p.rapidapi.com/waifus"
        headers = {
            'x-rapidapi-key': config.ANIMU_KEY,
            'x-rapidapi-host': "animu.p.rapidapi.com"
        }

        response = requests.request("GET", amiru_url, headers=headers, stream=True)
        waifu = json.loads(response.text)
        if response:
            embed.title       = waifu["names"]["en"]
            embed.description = "From: "+waifu["from"]["name"]+"\nMedia: "+waifu["from"]["type"]
            embed.set_image(url=waifu["images"][0])
            embed.set_footer(text=f"Requested by {ctx.author.name}")
        else:
            embed.description = "Error occured. Couldn't get waifu image. ⛔"
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(ImageCommands(bot))