# Chii Discord Bot

## About
Chii is a personal Discord bot that is in continuous development.

It uses [Discord](https://github.com/discord/discord-api-docs), [Youtube](https://github.com/ytdl-org/youtube-dl), & [OpenWeather](https://openweathermap.org/current) APIs.

Invite Chii to your server [here](https://discord.com/api/oauth2/authorize?client_id=788205742188003368&permissions=8&scope=bot)!

## Features
* Welcome new members to the server via direct message
* Respond back to certain messages
* React to certain messages
* Display guild/server information
* Simple probability/chance
* Play audio (Youtube)
* Display the weather for a city

## Installation
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

## Commands (prefix "-")
Command Name | Description
-------------|------------
coinflip | Flips a coin
rolldice | Rolls a dice
guild | Display the guild/server information
server | Display the guild/server information
choose [n] [m] | Chooses a number between n and m
play [Youtube Link] | Play music using, so far, Youtube links
exit | Exit the bot from voice channel
pause | Pauses the music the bot is currently playing
resume | Resumes the music from bot if it is paused
stop | Stops the music the bot is playing
weather [City] | Display weather information for a city

## TODOs
Chii is still in development and will be adding new features/updates at an upcoming time.
Below are ideas that I would like to implement:
- [x] React to certain string messages
- [ ] Add game command where users could interact with it
- [ ] Add other APIs to it:
  - [ ] Spotify
  - [x] Weather
  - [ ] Image-based
- [ ] Host it in the cloud (using [repl.it](https://repl.it) or some other alternative) or locally (using raspberry pi)
- [ ] Organize the project more (seperate certain functions into different file)
- [x] Add server info command to show info of current server

And more will be added.
