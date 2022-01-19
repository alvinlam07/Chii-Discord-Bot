# ProbabilityCommands.py
import discord, random
from discord.ext import commands

# initialize the random number generator
random.seed
class ProbabilityCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # bot command (-coinflip)
    # summary: flips a coin
    @commands.command(name="coinflip", brief="Flips a coin")
    async def coin_flip(self, ctx):
        embed = discord.Embed(color=discord.Colour.from_rgb(255,192,203))

        coinside = random.randint(0, 1)
        # head
        if coinside == 0:
            embed.description = "It's Head! 🪙"
        # tail
        elif coinside == 1:
            embed.description = "It's Tail! 🪙"
        await ctx.channel.send(embed=embed)

    # bot command (-rolldice)
    # summary: rolls a dice
    @commands.command(name="rolldice", brief="Rolls a dice")
    async def dice_roll(self, ctx):
        dice = random.randint(1, 6)
        if dice in range(1, 7):
            embed = discord.Embed(
                description="It's a " + str(dice) + "! 🎲", 
                color=discord.Colour.from_rgb(255,192,203)
            )
            await ctx.channel.send(embed=embed)

    # bot command (-choose [n] [m])
    # summary: chooses a number between n and m
    @commands.command(name = 'choose', brief="Chooses a number between n and m")
    async def choose(self, ctx, num1: int, num2: int):
        embed = discord.Embed(color=discord.Colour.from_rgb(255,192,203))

        try:
            number = random.randint(num1, num2)
            if number in range(num1, num2+1):
                embed.description = "It's a " + str(number) + "! 🔢"
        except ValueError:
            embed.description = "Error: 1st number should be less than or equal to the 2nd number! Try again. ⛔"
        await ctx.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(ProbabilityCommands(bot))