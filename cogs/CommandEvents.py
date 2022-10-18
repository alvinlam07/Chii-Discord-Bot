# CommandsEvents.py
import discord
from discord.ext import commands

class CommandEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # code is executed when the bot is ready
    # summary: sends confirmation and list all of the servers it is initally 
    # 		   in since run via command-line
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"\n{self.bot.user.name} is up and running!\n")
        
        # show server bot is in
        print("Connected Servers: ")
        guilds = self.bot.guilds
        for guild in guilds:
            print(" - " + guild.name)

    # code is executed when a member joins a guild
    # summary: send an embedded message to the new member through direct message
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        guild_list = self.bot.guilds
        # store the guild's name and icon url the member just joined
        for guild in guild_list:
            if member.guild.id == guild.id:
                guild_name = guild
                guild_icon_url = guild.icon.url

        embed = discord.Embed(
            title=f"Welcome to the {guild_name} server!",
            description=f"Thank you for joining this server {member.mention}. I hope you enjoy your stay!",
            colour=discord.Colour.from_rgb(255,192,203)
        )
        embed.set_thumbnail(url=guild_icon_url)

        await member.send(embed=embed)

    # code is executed when a message is sent by a member (with/without prefix)
    # summary: respond and react to messages from members
    @commands.Cog.listener()
    async def on_message(self, message):
        embed = discord.Embed(color=discord.Colour.from_rgb(255,192,203))

        # ignore its own and other bot(s)'s message
        if message.author == self.bot.user or message.author.bot:
            return
        else:
            # -----------responding back to messages-----------

            # wishes someone a happy birthday message
            if "happy birthday" in message.content.lower():
                embed.description = "Happy Birthday! 🎈🎉"
                await message.channel.send(embed=embed)
                
            # easter egg: Rick Astley - Never Gonna Give You Up chorus
            if "never gonna give you up" in message.content.lower():
                embed.description = "Never gonna let you down! 🎶"
                await message.channel.send(embed=embed)
            elif "never gonna run around and desert you" in message.content.lower():
                embed.description = "Never gonna make you cry! 🎶"
                await message.channel.send(embed=embed)
            elif "never gonna say goodbye" in message.content.lower():
                embed.description = "Never gonna tell a lie and hurt you! 🎶"
                await message.channel.send(embed=embed)

            # delete message containing certain strings
            if ("rugby" in message.content.lower()) or ("cricket" in message.content.lower()):
                await message.delete()

            #-----------reacting to string messages------------

            if ("hi" in message.content.lower()) or ("hey" in message.content.lower()) or ("hello" in message.content.lower()):
                await message.add_reaction('👋')
            elif ("nice" in message.content.lower()) or ("ok" in message.content.lower()) :
                await message.add_reaction('👌')
            elif "please" in message.content.lower():
                await message.add_reaction('🥺')
            elif "love" in message.content.lower():
                await message.add_reaction('💖')

    # code is executed when an error has occured
    # summary: handles error from discord commands
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        print("\nCalled on_command_error") # for
        print("ERROR: "+str(error)) 	     # debugging
        embed = discord.Embed(color=discord.Colour.from_rgb(255,192,203))
        embed.description = "An error has occurred"

        if isinstance(error, commands.CommandNotFound):
            return
        if isinstance(error, commands.MissingRequiredArgument):
            embed.description = "Error: Missing required argument(s). Try again. ⛔"
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(CommandEvents(bot))