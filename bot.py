# bot.py
import os
import discord
import random
from dotenv import load_dotenv
from discord.ext import commands

# loads the .env file
load_dotenv()
# grab the API token from the .env file
TOKEN = os.getenv('DISCORD_TOKEN')

# create bot object and defined the prefix for bot commands
bot = commands.Bot(command_prefix = '-')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_member_join(member):
	guild = discord.utils.get(bot.guilds, name = GUILD)
	await member.create_dm()
	await member.dm_channel.send(
	    f'Hi {member.name}, welcome to the {guild} server!'
	)

@bot.event
async def on_message(message):
	# do not include/respond to bot messages 
    if message.author == bot.user:
        return

    if "happy birthday" in message.content.lower():
    	await message.channel.send('Happy Birthday! 🎈🎉')

    # need this to trigger bot commands
    await bot.process_commands(message)

# bot command (-coinflip)
# flips a coin and respond with the result
@bot.command(name = 'coinflip')
async def coin_flip(ctx):
	coinside = random.randint(0, 1)

	# flipped heads 
	if coinside == 0:
		await ctx.channel.send("It's Head!")
	# flipped tails
	elif coinside == 1:
		await ctx.channel.send("It's Tail!")
	# exception handler
	else:
		raise discord.DiscordException

# bot command (-rolldice)
# rolls a dice abd respond with the result
@bot.command(name = 'rolldice')
async def dice_roll(ctx):
	dice = random.randint(1, 6)

	# rolled a number 1-6
	if dice in range(1, 6):
		await ctx.channel.send("It's a " + str(dice) + "!")
	# exception handler
	else:
		raise discord.DiscordException

# handles exception that occurs and log the error
@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

# run the bot with specified token
bot.run(TOKEN)