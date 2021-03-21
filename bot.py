# bot.py
import os
import discord
import random
import youtube_dl
import requests, json
from dotenv import load_dotenv
from discord.ext import commands

# loads the .env file
load_dotenv()

# grab the API token from the .env file
TOKEN = os.getenv('DISCORD_TOKEN')
WEATHER = os.getenv('WEATHER_TOKEN')

# url(s)
weather_url = "http://api.openweathermap.org/data/2.5/weather?"

# enable intents and create bot object and defined the prefix for bot commands
intents = discord.Intents.all()
bot     = commands.Bot(command_prefix = '-', intents = intents)

# initialize the random number generator
random.seed

@bot.event
async def on_ready():
	# confirm that the bot is up and running
	print(f'{bot.user.name} has connected to Discord!\n')

	# list all servers it is in
	print('Connected Servers: ')

	guilds = bot.guilds

	for guild in guilds:
		print(' - ' + guild.name)


@bot.event
async def on_member_join(member):
	guilds         = bot.guilds	# list of guilds that bot is in

	# used to store name and icon url of specfic guild
	guild_name 	   = ""
	guild_icon_url = ""

	# get the name and icon url of guild the member just joined
	for guild in guilds:
		if member.guild.id == guild.id:
			guild_name = guild
			guild_icon_url = guild.icon_url

	welcome = discord.Embed(
		colour = discord.Colour.from_rgb(255,192,203),
		title = f'Welcome to the {guild_name} server!',
		description = f'Thank you for joining this server {member.mention}. I hope you enjoy your stay!',
	)
	welcome.set_thumbnail(url=guild_icon_url)
	
	await member.send(embed=welcome)

@bot.event
async def on_message(message):
	# do not include/respond to bot messages 
	if message.author == bot.user:
		return

	# -------responding back to string messages-------

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

	#-----------reacting to string messages-----------

	if ("hi" in message.content.lower()) or ("hey" in message.content.lower()) or ("hello" in message.content.lower()):
		await message.add_reaction('👋')

	elif ("nice" in message.content.lower()) or ("ok" in message.content.lower()) :
		await message.add_reaction('👌')
	
	elif "please" in message.content.lower():
		await message.add_reaction('🥺')

	elif "love" in message.content.lower():
		await message.add_reaction('💖')

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

# bot command (-rolldice)
# rolls a dice abd respond with the result
@bot.command(name = 'rolldice')
async def dice_roll(ctx):
	dice = random.randint(1, 6)

	# rolled a number 1-6
	if dice in range(1, 7):
		await ctx.channel.send("It's a " + str(dice) + "!")

# bot command (-choose n m)
# chooses a number between n and m
@bot.command(name = 'choose')
async def choose(ctx, num1: int, num2: int):
	number = random.randint(num1, num2)

	# chose a number between num1 and num2
	if number in range(num1, num2+1):
		await ctx.channel.send("It's a " + str(number) + "!")

# bot command (-play [YTlink])
# play music from Youtube
@bot.command(name = 'play')
async def play(ctx, url: str):	
	song = os.path.isfile('song.mp3')
	try:
		if song:
			os.remove('song.mp3')
	except PermissionError:
		return await ctx.send("Current music is still playing. Wait for it to end or use the -stop command")
	
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

# bot command (-pause)
# pauses the music the bot is currently playing
@bot.command(name = 'pause')
async def pause(ctx):
	v = discord.utils.get(bot.voice_clients, guild=ctx.guild)
	if v.is_playing(): v.pause()
	else: await ctx.send("No music is being played at the moment!")

# bot command (-resume)
# resumes the music if it is paused
@bot.command(name = 'resume')
async def resume(ctx):
	v = discord.utils.get(bot.voice_clients, guild=ctx.guild)
	if v.is_paused(): v.resume()
	else: await ctx.send("The music is not paused!")

# bot command (-stop)
# stops the music the bot is playing
@bot.command(name = 'stop')
async def stop(ctx):
	v = discord.utils.get(bot.voice_clients, guild=ctx.guild)
	v.stop()

# bot command (-weather [City])
# displays the weather for [City]
@bot.command(name = 'weather')
async def weather(ctx, *, city: str):
	# get response from openweather website (requests) and read it (json)
	url = weather_url + "appid=" + WEATHER + "&q=" + city
	response = requests.get(url)
	x = response.json()
	channel = ctx.message.channel

	# check if city exist
	if x["cod"] != "404":
		async with channel.typing():
			# get weather info at [city]
			y = x["main"]
			current_temperature = y["temp"]
			current_temperature_celsiuis = str(round(current_temperature - 273.15))
			current_pressure = y["pressure"]
			current_humidity = y["humidity"]
			z = x["weather"]
			weather_description = z[0]["description"]

			# display the info inside a discord.Embed
			embed = discord.Embed(title=f"Weather in {city}", color=discord.Colour.teal(), timestamp=ctx.message.created_at,)
			embed.add_field(name="Descripition", value=f"**{weather_description}**", inline=False)
			embed.add_field(name="Temperature(C)", value=f"**{current_temperature_celsiuis}°C**", inline=False)
			embed.add_field(name="Humidity(%)", value=f"**{current_humidity}%**", inline=False)
			embed.add_field(name="Atmospheric Pressure(hPa)", value=f"**{current_pressure}hPa**", inline=False)
			embed.set_thumbnail(url="https://i.ibb.co/CMrsxdX/weather.png")
			embed.set_footer(text=f"Requested by {ctx.author.name}")
	else:
		return await channel.send("City does not exist/not found.")
	
	await channel.send(embed=embed)

# run the bot with specified token
bot.run(TOKEN)