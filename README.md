# Chii Discord Bot

### About
Chii is a personal Discord bot that is in continuous development.

It uses [Discord API](https://discord.com/developers/docs/reference), [Youtube API](https://pypi.org/project/youtube_dl/), & [OpenWeather API](https://openweathermap.org/api).

Invite Chii to your server [here](https://discord.com/api/oauth2/authorize?client_id=788205742188003368&permissions=8&scope=bot)!

### Features
* Welcome new members to the server via direct message
* Respond back to certain messages
* React to certain messages
* Probability
* Play audio (YT)
* Display the weather

### Installation
You can invite Chii to your server using this [link](https://discord.com/api/oauth2/authorize?client_id=788205742188003368&permissions=8&scope=bot)!
Alternatively, you can clone this repo and host it yourself:
```
git clone https://github.com/alam1517/Chii-Discord-Bot.git
```
Make sure that you install the discord.py, youtube_dl, and dotenv if you do not have it:
```
pip install -U discord.py

pip install -U youtube_dl

pip install -U python-dotenv
```

### Commands (prefix "-")
Command Name | Description
-------------|------------
coinflip | Flips a coin
rolldice | Rolls a dice
choose *n* *m* | Chooses a number between n and m
play *YTlink* | Play music using, so far, Youtube links
exit | Exit the bot from voice channel
pause | Pauses the music the bot is currently playing
resume | Resumes the music from bot if it is paused
stop | Stops the music the bot is playing
weather *city* | Display weather information for a city

### TODOs
Chii is still in development and will be adding new features/updates at an upcoming time.
Below are ideas that I would like to implement:
- [x] React to certain string messages
- [ ] Add game command where users could interact with it
- [ ] Add other APIs to it (Spotify, Weather, image-based, etc.)
- [ ] Host it in the cloud (using [repl.it](https://repl.it))
