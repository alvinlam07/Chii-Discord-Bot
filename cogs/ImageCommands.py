# ImageCommands.py
import discord, os, sys, random, asyncpraw, requests, json
from discord.ext import commands
from PIL import Image
from io import BytesIO
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
    # summary: displays a meme image from r/memes subreddit
    @commands.command(name="memes", brief="Displays a meme image from r/memes subreddit")
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
    # summary: displays a cute dog image
    @commands.command(name="dog", brief="Displays a cute dog image")
    async def dog(self, ctx):
        embed = discord.Embed(color=discord.Colour.from_rgb(255,192,203))

        # send get request, convert response to string, and load url
        response  = requests.get("https://dog.ceo/api/breeds/image/random")
        dog_image = json.loads(response.text)
        if response:
            embed.title = "🐶🐶🐶"
            embed.set_image(url=dog_image["message"])
            embed.set_footer(text=f"Requested by {ctx.author.name}")
        else:
            embed.description="Error occured. Couldn't get dog image. ⛔"
        await ctx.send(embed=embed)
        
    # bot command (-cat)
    # summary: displays a cute cat image
    @commands.command(name="cat", brief="Displays a cute cat image")
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

    # bot command (-wanted)
    # summary: image manipulation; displays a wanted poster of user
    @commands.command(name="wanted", brief="Displays a wanted poster of user")
    async def wanted(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author

        wanted = Image.open("./images/wanted.jpeg")

        asset = user.avatar_url_as(size=128)
        data  = BytesIO(await asset.read())
        pfp   = Image.open(data).resize((177, 177))

        wanted.paste(pfp, (120, 212))
        wanted.save("./images/profile.jpeg")

        await ctx.send(file = discord.File("./images/profile.jpeg"))

    # bot command (-waifu)
    # summary: display a cute cat image
    @commands.command(name="waifu", brief="Display a cute cat image")
    async def waifu(self, ctx):
        embed = discord.Embed(color=discord.Colour.from_rgb(255,192,203))

        # send get request, convert response to string, and load url
        response = requests.get("https://api.waifu.pics/sfw/waifu")
        waifu_img = json.loads(response.text)
        if response:
            embed.title = "Here's your waifu!"
            embed.set_image(url=waifu_img["url"])
            embed.set_footer(text=f"Requested by {ctx.author.name}")
        else:
            embed.description = "Error occured. Couldn't get waifu image. ⛔"
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(ImageCommands(bot))