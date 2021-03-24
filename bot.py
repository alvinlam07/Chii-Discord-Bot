# bot.py
import os, platform, sys, random, discord, youtube_dl, requests, json, asyncpraw, asyncprawcore
from discord.ext import commands
from discord.ext.commands import Bot
if not os.path.isfile("config.py"):
	sys.exit("'config.py' could not be found. Add the file and try again.")
else:
	import config

# reddit authentication
r_auth = asyncpraw.Reddit(
	client_id=config.REDDIT_CLIENT_ID, 
	client_secret=config.REDDIT_SECRET, 
	user_agent=config.REDDIT_NAME
)

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
	guild_list = bot.guilds	
	# store the guild's name and icon url the member just joined
	for guild in guild_list:
		if member.guild.id == guild.id:
			guild_name = guild
			guild_icon_url = guild.icon_url

	embed = discord.Embed(
		title=f"Welcome to the {guild_name} server!",
		description=f"Thank you for joining this server {member.mention}. I hope you enjoy your stay!",
		colour=discord.Colour.from_rgb(255,192,203)
	)
	embed.set_thumbnail(url=guild_icon_url)

	await member.send(embed=embed)

# code is executed when a message is sent by a member (with/without prefix)
# summary: respond and react to messages from members
@bot.event
async def on_message(message):
	embed = discord.Embed(color=discord.Colour.from_rgb(255,192,203))

	# ignore its own and other bot(s)'s message
	if message.author == bot.user or message.author.bot:
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
# summary: display the information of the guild (same as -guild command)
@bot.command(name="server")
async def server(ctx):
	await guild.invoke(ctx)

# bot command (-coinflip)
# summary: flips a coin

@bot.command(name="coinflip")
async def coin_flip(ctx):
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
	embed = discord.Embed(color=discord.Colour.from_rgb(255,192,203))

	try:
		number = random.randint(num1, num2)
		if number in range(num1, num2+1):
			embed.description = "It's a " + str(number) + "! 🔢"
	except ValueError:
		embed.description = "Error: 1st number should be less than or equal to the 2nd number! Try again. ⛔"
	await ctx.channel.send(embed=embed)

# bot command (-play [YouTube link])
# summary: play audio from Youtube
@bot.command(name="play")
async def play(ctx, url: str):
	embed = discord.Embed(color=discord.Colour.from_rgb(255,192,203))

	song = os.path.isfile('song.mp3')
	try:
		if song:
			os.remove('song.mp3')
	except PermissionError:
		embed.description = "Current music is still playing. Wait for it to end or use the -stop command ⛔"
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
		info_dict         = ydl.extract_info(url, download=False)
		video_title       = info_dict.get("title", None)
		embed.title       = "Currently Playing:"
		embed.description = f"[{video_title}]({url})"
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
	embed = discord.Embed(color=discord.Colour.from_rgb(255,192,203))

	weather_url = "http://api.openweathermap.org/data/2.5/weather?" # base url
	# get response from openweather website
	full_url = weather_url + "q=" + city + "&appid=" + config.WEATHER_TOKEN 
	request  = requests.get(full_url)
	response = request.json()
	channel  = ctx.message.channel

	# check if city exist
	if response["cod"] != "404":
		async with channel.typing():
			# get weather info for city
			city_weather                   = response["main"]
			current_temperature            = city_weather["temp"]
			current_temperature_celsiuis   = str(round(current_temperature - 273.15))
			current_temperature_fahrenheit = str(round((current_temperature - 273.15) * (9/5) + 32))
			current_pressure               = city_weather["pressure"]
			current_humidity               = city_weather["humidity"]
			response_weather               = response["weather"]
			weather_description            = response_weather[0]["description"]

			embed.title = f"Weather in {city}"
			embed.add_field(name="Description", value=f"**{weather_description}**", inline=False)
			embed.add_field(name="Temperature(F)/(C)", value=f"**{current_temperature_fahrenheit}°F/{current_temperature_celsiuis}°C**", inline=False)
			embed.add_field(name="Humidity(%)", value=f"**{current_humidity}%**", inline=False)
			embed.add_field(name="Atmospheric Pressure(hPa)", value=f"**{current_pressure}hPa**", inline=False)
			embed.set_thumbnail(url="https://i.ibb.co/CMrsxdX/weather.png")
			embed.set_footer(text=f"Requested by {ctx.author.name}")
	else:
		embed.description="City does not exist/not found. Try again. ⛔"
	await channel.send(embed=embed)

# bot command (-reddit <subreddit>)
# summary: displays the 10 hottest posts from all subreddit or from a specfic subreddit
@bot.command(name="reddit")
async def reddit(ctx, *, subreddit: str=None):
	embed = discord.Embed(color=discord.Colour.from_rgb(255,192,203))

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

# bot command (-memes)
# summary: display a meme image from r/memes subreddit
@bot.command(name="memes")
async def memes(ctx):
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
@bot.command(name="dog")
async def dog(ctx):
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
@bot.command(name="cat")
async def cat(ctx):
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
@bot.command(name="waifu")
async def waifu(ctx):
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

# code is executed when an error has occured
# summary: handles error from discord commands
@bot.event
async def on_command_error(ctx, error):
	print("IN ON_COMMAND_ERROR") # for
	print(error) 				 # debugging
	embed = discord.Embed(color=discord.Colour.from_rgb(255,192,203))

	if isinstance(error, commands.CommandNotFound):
		return
	if isinstance(error, commands.MissingRequiredArgument):
		embed.description = "Error: Missing required argument(s). Try again. ⛔"
	# if isinstance(error, commands.ClientException):
	# 	embed.description = "I'm already connected to the voice channel. ⛔"
	await ctx.send(embed=embed)

# run the bot with token`
bot.run(config.TOKEN)