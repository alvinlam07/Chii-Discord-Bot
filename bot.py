# bot.py
import discord, os, sys
from discord.ext import commands
from discord.ext.commands import Bot
if not os.path.isfile("config.py"):
	sys.exit("'config.py' could not be found. Add the file and try again.")
else:
	import config

# create bot object, defined the prefix for bot commands, and enable all intents
bot = Bot(command_prefix=config.BOT_PREFIX, intents=discord.Intents.all())

# # load extensions
# @bot.command(name="load")
# async def load(ctx, extension):
# 	bot.load_extension(f"cos.{extension}")

# # unload extensions
# @bot.command(name="unload")
# async def unload(ctx, extension):
# 	bot.unload_extension(f"cos.{extension}")

# load each of the extensions
for cog_file in os.listdir('./cogs'):
	if cog_file.endswith(".py"):
		try:
			bot.load_extension(f"cogs.{cog_file[:-3]}")
			print(f"Loaded {cog_file}")
		except Exception:
			print(f"Failed to load {cog_file}")

# run the bot with token`
bot.run(config.TOKEN)