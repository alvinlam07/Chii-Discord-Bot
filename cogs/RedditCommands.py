# RedditCommands.py
import discord, os, sys, asyncpraw, asyncprawcore
from discord.ext import commands
if not os.path.isfile("config.py"):
	sys.exit("'config.py' could not be found. Add the file and try again.")
else:
	import config

class RedditCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # bot command (-reddit <subreddit>)
    # summary: displays the 10 hottest posts from all subreddit or from a specfic subreddit
    @commands.command(name="reddit")
    async def reddit(self, ctx, *, subreddit: str=None):
        embed = discord.Embed(color=discord.Colour.from_rgb(255,192,203))

        # reddit authentication
        r_auth = asyncpraw.Reddit(
            client_id=config.REDDIT_CLIENT_ID, 
            client_secret=config.REDDIT_SECRET, 
            user_agent=config.REDDIT_NAME
        )

        async with ctx.typing():
            # check for optional argument
            if subreddit is None:
                sr_name = "all"
            else:
                sr_name = subreddit
            
            post_list = []
            sr = await r_auth.subreddit(sr_name) # get post info from subreddit
            try:
                async for post in sr.hot(limit=10):
                # append post's title and url
                    if (len(post.title) > 256):
                        short_title = post.title[0:256]
                        post_list.append([short_title, post.shortlink])
                    else:
                        post_list.append([post.title, post.shortlink])
                # fetch subreddit icon
                if subreddit is not None:
                    await sr.load()
                    sr_icon = sr.icon_img
            except Exception:
                embed.description="Could not find the subreddit. Try again. ⛔"
                return await ctx.send(embed=embed)

            embed.title="10 Hot Posts from r/" + sr_name
            for post in post_list:
                embed.add_field(name=post[0], value=post[1], inline=False)
            # make thumbnail as subreddit's icon
            if subreddit is None:
                embed.set_thumbnail(url="https://external-preview.redd.it/iDdntscPf-nfWKqzHRGFmhVxZm4hZgaKe5oyFws-yzA.png?auto=webp&s=38648ef0dc2c3fce76d5e1d8639234d8da0152b2")
            else:
                embed.set_thumbnail(url=sr_icon)
            embed.set_footer(text=f"Requested by {ctx.author.name}")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(RedditCommands(bot))