# bot.py
import asyncio
from email.mime import application
import discord, os
from discord.ext.commands import Bot
from dotenv import load_dotenv

load_dotenv()

# define intents and create bot object
intents = discord.Intents.all()
bot = Bot(command_prefix=os.getenv("BOT_PREFIX"), intents=intents)

# load each of the extensions
async def load():
	for cog_file in os.listdir('./cogs'):
		if cog_file.endswith(".py"):
			try:
				await bot.load_extension(f"cogs.{cog_file[:-3]}")
				print(f"Loaded {cog_file}")
			except Exception:
				print(f"Failed to load {cog_file}")

async def main():
	await load()
	await bot.start(os.getenv("TOKEN"))

asyncio.run(main())