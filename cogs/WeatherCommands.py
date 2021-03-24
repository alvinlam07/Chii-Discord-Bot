# WeatherCommands.py
import discord, os, sys, requests
from discord.ext import commands
if not os.path.isfile("config.py"):
	sys.exit("'config.py' could not be found. Add the file and try again.")
else:
	import config

class WeatherCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # bot command (-weather [City])
    # summary: displays the weather information for a city name
    @commands.command(name="weather")
    async def weather(self, ctx, *, city: str):
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

def setup(bot):
    bot.add_cog(WeatherCommands(bot))