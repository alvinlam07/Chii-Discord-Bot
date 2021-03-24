# UtilityCommands.py
import discord
from discord.ext import commands

class UtilityCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # bot command (-guild)
    # summary: display the information of the guild
    @commands.command(name="guild")
    async def guild(self, ctx):
        # get guild/server info
        name  		 = ctx.guild.name
        description  = ctx.guild.description
        owner 		 = ctx.guild.owner
        id    		 = ctx.guild.id
        region 		 = ctx.guild.region
        member_count = ctx.guild.member_count
        icon_url     = ctx.guild.icon_url

        embed = discord.Embed(
            title=f"{name} Server Information",
            description=description,
            color=discord.Colour.from_rgb(255,192,203)
        )
        embed.add_field(name="Server Owner:", value=owner,inline=False)
        embed.add_field(name="Server ID:", value=id,inline=False)
        embed.add_field(name="Region:", value=region,inline=False)
        embed.add_field(name="Member Count:", value=member_count,inline=False)
        embed.set_thumbnail(url=icon_url)

        await ctx.send(embed=embed)

    # bot command (-server)
    # summary: display the information of the guild (invoke -guild command)
    @commands.command(name="server")
    async def server(self, ctx):
        await ctx.invoke(self.bot.get_command("guild"))

def setup(bot):
    bot.add_cog(UtilityCommands(bot))