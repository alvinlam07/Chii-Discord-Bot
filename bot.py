# bot.py
import os
import discord
import random
import youtube_dl
from dotenv import load_dotenv
from discord.ext import commands

# loads the .env file
load_dotenv()
# grab the API token from the .env file
TOKEN = os.getenv('DISCORD_TOKEN')

# create bot object and defined the prefix for bot commands
bot = commands.Bot(command_prefix = '-')

# initialize the random number generator
random.seed

@bot.event
async def on_ready():
	print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_member_join(member):
	guild = discord.utils.get(bot.guilds)
	await member.create_dm()
	await member.dm_channel.send(
		f'Hi {member.name}, welcome to the {guild} server!'
	)

@bot.event
async def on_message(message):
	# do not include/respond to bot messages 
	if message.author == bot.user:
		return

	# wishes someone a happy birthday message
	if "happy birthday" in message.content.lower():
		await message.channel.send('Happy Birthday! 🎈🎉')
		
	# easter egg: Rick Astley - Never Gonna Give You Up chorus
	if "never gonna give you up" in message.content.lower():
		await message.channel.send('Never gonna let you down!')
	elif "never gonna run around and desert you" in message.content.lower():
		await message.channel.send('Never gonna make you cry!')
	elif "never gonna say goodbye" in message.content.lower():
		await message.channel.send('Never gonna tell a lie and hurt you!')

	# need this to trigger bot commands
	await bot.process_commands(message)

# bot command (-coinflip)
# flips a coin and respond with the result
@bot.command(name = 'coinflip')
async def coin_flip(ctx):
	coinside = random.randint(0, 1)

	# flipped head
	if coinside == 0:
		await ctx.channel.send("It's Head!")
	# flipped tail
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
	if dice in range(1, 7):
		await ctx.channel.send("It's a " + str(dice) + "!")
	# exception handler
	else:
		raise discord.DiscordException

# bot command (-choose)
# chooses a number between n and m
@bot.command(name = 'choose')
async def choose(ctx, num1: int, num2: int):
	number = random.randint(num1, num2)

	# chose a number between num1 and num2
	if number in range(num1, num2+1):
		await ctx.channel.send("It's a " + str(number) + "!")
	# exception handler
	else:
		raise discord.DiscordException

# bot command (-play)
# play music from Youtube
@bot.command(name = 'play')
async def play(ctx, url: str):
	song = os.path.isfile('song.mp3')
	try:
		if song:
			os.remove('song.mp3')
	except PermissionError:
		await ctx.send("Current music is still playing. Wait for it to end or use the -stop command")
		return
	
	vc = discord.utils.get(ctx.guild.voice_channels)
	await vc.connect()
	v = discord.utils.get(bot.voice_clients, guild=ctx.guild)

	ydl_opts = {
		'format': 'bestaudio/best',
		'postprocessors': [{
			'key': 'FFmpegExtractAudio',
			'preferredcodec': 'mp3',
			'preferredquality': '192',
		}],
	}

	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.download([url])
	for file in os.listdir("./"):
		if file.endswith(".mp3"):
			os.rename(file, "song.mp3")
	v.play(discord.FFmpegPCMAudio("song.mp3"))

# bot command (-exit)
# exit the bot from VC
@bot.command(name = 'exit')
async def exit(ctx):
	v = discord.utils.get(bot.voice_clients, guild=ctx.guild)
	if v.is_connected():
		await v.disconnect()
	else:
		await ctx.send("I'm not connected to a voice channel!")

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