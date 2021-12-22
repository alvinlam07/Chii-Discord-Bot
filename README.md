<h3 align="center">
  <a href="https://github.com/alam1517/Chii-Discord-Bot">
	  <img src=./images/Chii_Discord_Bot_Banner.png>
  </a>
</h3>

<h2 align="center">
  A personal Python Discord bot built with <a href="https://github.com/discord/discord-api-docs">discord.py</a>
</h2>

<p align="center"> Table of Contents </p>

<p align="center">
  <a href="https://github.com/alam1517/Chii-Discord-Bot/blob/main/README.md#-about">About</a> 
  | 
  <a href="https://github.com/alam1517/Chii-Discord-Bot/blob/main/README.md#-features">Features</a>
  | 
  <a href="https://github.com/alam1517/Chii-Discord-Bot/blob/main/README.md#-setupinstallation">Setup/Installation</a>
  | 
  <a href="https://github.com/alam1517/Chii-Discord-Bot/blob/main/README.md#-command-list">Command List</a>
  |
  <a href="https://github.com/alam1517/Chii-Discord-Bot/blob/main/README.md#-todos">TODOs</a>
</p>

## 📃 About
Chii is a personal Discord bot that is in continuous development. It uses the following APIs:
* [Discord](https://github.com/discord/discord-api-docs)
* [OpenWeather](https://openweathermap.org/current)
* [Reddit](https://github.com/reddit-archive/reddit)
* [Dog API](https://github.com/ElliottLandsborough/dog-ceo-api)
* [The Cat API](https://documenter.getpostman.com/view/5578104/RWgqUxxh)

Invite Chii to your server [here](https://discord.com/api/oauth2/authorize?client_id=788205742188003368&permissions=8&scope=bot)!

## 🔧 Features
* Welcome new members to the server via direct message
* Respond back to certain messages
* React to certain messages
* Display guild/server information
* Simple probability/chance
* Display the weather for a city
* Display the 10 hottest reddit posts
* Display dog and cat images

## ⚙ Setup/Installation
You can invite Chii to your server using this [link](https://discord.com/api/oauth2/authorize?client_id=788205742188003368&permissions=8&scope=bot)!
Alternatively, you can clone this repo and host it yourself:
```
git clone https://github.com/alam1517/Chii-Discord-Bot.git
```
Before starting, making sure that you have latest version of python3 and python3-pip.
To check, do the following:
```
python3 --version
pip --version
```
If you do not have either or both installed, do the following:
```
sudo apt-get install python3
sudo apt-get install python3-pip
```
Afterwards, you will need to install the other libraries/APIs if you do not have it:
```
pip install -U discord.py
```

## 🤖 Command List:
The prefix for these commands is `-`. Arguments encased with `[]` are required and `<>` are optional.

### 🧑‍🤝‍🧑 Utility
| Command | Description                          | Usage   |
|---------|--------------------------------------|---------|
| Guild   | Display the guild/server information | -guild  |
| Server  | Display the guild/server information | -server |

### 🪙 Probability/Chance 
| Command  | Description                      | Usage           |
|----------|----------------------------------|-----------------|
| Coinflip | Flips a coin                     | -coinflip       |
| Rolldice | Rolls a dice                     | -rolldice       |
| Choose   | Chooses a number between n and m | -choose [n] [m] |

### ☀ Weather
| Command | Description                            | Usage           |
|---------|----------------------------------------|-----------------|
| Weather | Display weather information for a city | -weather [City] |

### 👽 Reddit
| Command | Description                                                           | Usage                 |
|---------|-----------------------------------------------------------------------|-----------------------|
| Reddit  | Display the 10 hottest posts from r/all or a subreddit of your choice | -reddit \<Subreddit\> |
  
### 🖼 Image
| Command | Description                                 | Usage  |
|---------|---------------------------------------------|--------|
| Memes   | Display a meme image from r/memes subreddit | -memes |
| Dog     | Display a cute dog image                    | -dog   |
| Cat     | Display a cute cat image                    | -cat   |

## ✔ TODOs
Chii is still in development and will be adding new features/updates at an upcoming time.
Below are ideas that I would like to implement:
- [x] React to certain string messages
- [x] Respond to reaction(s)
- [ ] Add game command where users could interact with it
- [ ] Add other APIs to it:
  - [ ] Spotify
  - [x] Weather
  - [ ] Image-based
  - [x] Reddit
  - [x] Dog & Cat
- [ ] Host it in the cloud (using [repl.it](https://repl.it) or some other alternative) or locally (using raspberry pi)
- [x] Organize the project more (seperate certain functions into different file)
- [x] Add server info command to show info of current server

And more will be added.
