# bot.py
import os, platform, sys, random, discord, youtube_dl, requests, json

from discord.ext import commands
from discord.ext.commands import Bot

if not os.path.isfile("config.py"):
	sys.exit("'config.py' could not be found. Add the file and try again.")
else:
	import config

# base url(s)
weather_url = "http://api.openweathermap.org/data/2.5/weather?"

# enable intents and create bot object and defined the prefix for bot commands
intents = discord.Intents.all()
bot     = Bot(command_prefix=config.BOT_PREFIX, intents=intents)

# initialize the random number generator
random.seed

# code is executed when the bot is ready
# summary: sends confirmation and list all of the servers it is initally 
# 		   in since run via command-line
@bot.event
async def on_ready():
	print(f"{bot.user.name} is up and running!\n")

	print("Connected Servers: ")
	guilds = bot.guilds
	for guild in guilds:
		print(" - " + guild.name)

# code is executed when a member joins a guild
# summary: send an embedded message to the new member through direct message
@bot.event
async def on_member_join(member):
	guild_list     = bot.guilds	
	# store the guild's name and icon url the member just joined
	for guild in guild_list:
		if member.guild.id == guild.id:
			guild_name = guild
			guild_icon_url = guild.icon_url

	welcome = discord.Embed(
		title=f"Welcome to the {guild_name} server!",
		description=f"Thank you for joining this server {member.mention}. I hope you enjoy your stay!",
		colour=discord.Colour.from_rgb(255,192,203)
	)
	welcome.set_thumbnail(url=guild_icon_url)

	await member.send(embed=welcome)

# code is executed when a message is sent by a member (with/without prefix)
# summary: respond and react to messages from members
@bot.event
async def on_message(message):
	# ignore its own and other bot(s)'s message
	if message.author == bot.user or message.author.bot:
		return
	else:
		# -----------responding back to messages-----------

		# wishes someone a happy birthday message
		if "happy birthday" in message.content.lower():
			embed = discord.Embed(
				description="Happy Birthday! 🎈🎉", 
				color=discord.Colour.from_rgb(255,192,203)
			)
			await message.channel.send(embed=embed)
			
		# easter egg: Rick Astley - Never Gonna Give You Up chorus
		if "never gonna give you up" in message.content.lower():
			embed = discord.Embed(
				description="Never gonna let you down! 🎶", 
				color=discord.Colour.from_rgb(255,192,203)
			)
			await message.channel.send(embed=embed)
		elif "never gonna run around and desert you" in message.content.lower():
			embed = discord.Embed(
				description="Never gonna make you cry! 🎶", 
				color=discord.Colour.from_rgb(255,192,203)
			)
			await message.channel.send(embed=embed)
		elif "never gonna say goodbye" in message.content.lower():
			embed = discord.Embed(
				description="Never gonna tell a lie and hurt you! 🎶", 
				color=discord.Colour.from_rgb(255,192,203)
			)
			await message.channel.send(embed=embed)

		#-----------reacting to string messages------------

		if ("hi" in message.content.lower()) or ("hey" in message.content.lower()) or ("hello" in message.content.lower()):
			await message.add_reaction('👋')
		elif ("nice" in message.content.lower()) or ("ok" in message.content.lower()) :
			await message.add_reaction('👌')
		elif "please" in message.content.lower():
			await message.add_reaction('🥺')
		elif "love" in message.content.lower():
			await message.add_reaction('💖')

		await bot.process_commands(message)

# bot command (-guild)
# summary: display the information of the guild
@bot.command(name="guild")
async def guild(ctx):
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
# summary: display the information of the guild (same as -guild command)
@bot.command(name="server")
async def server(ctx):
	await guild.invoke(ctx)

# bot command (-coinflip)
# summary: flips a coin

@bot.command(name="coinflip")
async def coin_flip(ctx):
	coinside = random.randint(0, 1)
	# head
	if coinside == 0:
		embed = discord.Embed(
			description="It's Head! 🪙", 
			color=discord.Colour.from_rgb(255,192,203)
		)
		await ctx.channel.send(embed=embed)
	# tail
	elif coinside == 1:
		embed = discord.Embed(
			description="It's Tail! 🪙", 
			color=discord.Colour.from_rgb(255,192,203)
		)
		await ctx.channel.send(embed=embed)

# bot command (-rolldice)
# summary: rolls a dice
@bot.command(name="rolldice")
async def dice_roll(ctx):
	dice = random.randint(1, 6)
	if dice in range(1, 7):
		embed = discord.Embed(
			description="It's a " + str(dice) + "! 🎲", 
			color=discord.Colour.from_rgb(255,192,203)
		)
		await ctx.channel.send(embed=embed)

# bot command (-choose [n] [m])
# summary: chooses a number between n and m
@bot.command(name = 'choose')
async def choose(ctx, num1: int, num2: int):
	number = random.randint(num1, num2)
	if number in range(num1, num2+1):
		embed = discord.Embed(
			description="It's a " + str(number) + "! 🔢", 
			color=discord.Colour.from_rgb(255,192,203)
		)
		await ctx.channel.send(embed=embed)

# bot command (-play [YouTube link])
# summary: play audio from Youtube
@bot.command(name="play")
async def play(ctx, url: str):	
	song = os.path.isfile('song.mp3')
	try:
		if song:
			os.remove('song.mp3')
	except PermissionError:
		embed = discord.Embed(
			description="Current music is still playing. Wait for it to end or use the -stop command ⛔", 
			color=discord.Colour.from_rgb(255,192,203)
		)
		return await ctx.send(embed=embed)

	voice_channel = discord.utils.get(ctx.guild.voice_channels)
	await voice_channel.connect()
	voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

	ydl_opts = {
		'format': 'bestaudio/best',
		'postprocessors': [{
			'key': 'FFmpegExtractAudio',
			'preferredcodec': 'mp3',
			'preferredquality': '192',
		}],
	}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		info_dict   = ydl.extract_info(url, download=False)
		video_title = info_dict.get("title", None)
		embed = discord.Embed(
			title="Currently Playing:",
			description=f"[{video_title}]({url})", 
			color=discord.Colour.from_rgb(255,192,203)
		)
		embed.set_footer(text=f"Requested by {ctx.author.name}")
		await ctx.send(embed=embed)
		ydl.download([url])

	for file in os.listdir("./"):
		if file.endswith(".mp3"):
			os.rename(file, "song.mp3")
			
	voice.play(discord.FFmpegPCMAudio("song.mp3"))

# bot command (-exit)
# summary: exit the bot from voice channel
@bot.command(name="exit")
async def exit(ctx):
	voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
	try:
		if voice.is_connected():
			await voice.disconnect()
	except AttributeError:
		embed = discord.Embed(
			description="I'm not connected to a voice channel! ⛔", 
			color=discord.Colour.from_rgb(255,192,203)
		)
		await ctx.send(embed=embed)

# bot command (-pause)
# summary: pauses the currently playing audio 
@bot.command(name="pause")
async def pause(ctx):
	voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
	if voice.is_playing(): 
		voice.pause()
	else:
		embed = discord.Embed(
			description="No music is being played at the moment! 🔇", 
			color=discord.Colour.from_rgb(255,192,203)
		)
		await ctx.send(embed=embed)

# bot command (-resume)
# summary: resumes the a paused audio
@bot.command(name="resume")
async def resume(ctx):
	voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
	if voice.is_paused(): 
		voice.resume()
	else:
		embed = discord.Embed(
			description="The music is not paused! 🔇", 
			color=discord.Colour.from_rgb(255,192,203)
		)
		await ctx.send(embed=embed)

# bot command (-stop)
# summary: stops playing the audio
@bot.command(name="stop")
async def stop(ctx):
	try:
		voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
		voice.stop()
	except AttributeError:
		embed = discord.Embed(
			description="I'm not connected to a voice channel! ⛔", 
			color=discord.Colour.from_rgb(255,192,203)
		)
		await ctx.send(embed=embed)


# bot command (-weather [City])
# summary: displays the weather information for a city name
@bot.command(name="weather")
async def weather(ctx, *, city: str):
	# get response from openweather website (requests) and read it (json)
	full_url = weather_url + "q=" + city + "&appid=" + config.WEATHER_TOKEN 
	request  = requests.get(full_url)
	response = request.json()
	channel  = ctx.message.channel

	# check if city exist
	if response["cod"] != "404":
		async with channel.typing():
			# get weather info for city
			y = response["main"]
			current_temperature = y["temp"]
			current_temperature_celsiuis = str(round(current_temperature - 273.15))
			current_temperature_fahrenheit = str(round((current_temperature - 273.15) * (9/5) + 32))
			current_pressure = y["pressure"]
			current_humidity = y["humidity"]
			z = response["weather"]
			weather_description = z[0]["description"]

			embed = discord.Embed(
				title=f"Weather in {city}", 
				color=discord.Colour.from_rgb(255,192,203)
			)
			embed.add_field(name="Description", value=f"**{weather_description}**", inline=False)
			embed.add_field(name="Temperature(F)/(C)", value=f"**{current_temperature_fahrenheit}°F/{current_temperature_celsiuis}°C**", inline=False)
			embed.add_field(name="Humidity(%)", value=f"**{current_humidity}%**", inline=False)
			embed.add_field(name="Atmospheric Pressure(hPa)", value=f"**{current_pressure}hPa**", inline=False)
			embed.set_thumbnail(url="https://i.ibb.co/CMrsxdX/weather.png")
			embed.set_footer(text=f"Requested by {ctx.author.name}")

		await channel.send(embed=embed)
	else:
		embed = discord.Embed(
			description="City does not exist/not found. Try again. ⛔", 
			color=discord.Colour.from_rgb(255,192,203)
		)
		await channel.send(embed=embed)

# run the bot with token
bot.run(config.TOKEN)