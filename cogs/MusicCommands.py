# MusicCommands.py
import discord, os, youtube_dl
from discord.ext import commands

class MusicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # bot command (-play [YouTube link])
    # summary: play audio from Youtube
    @commands.command(name="play")
    async def play(self, ctx, url: str):
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
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

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
    @commands.command(name="exit")
    async def exit(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
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
    @commands.command(name="pause")
    async def pause(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
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
    @commands.command(name="resume")
    async def resume(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
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
    @commands.command(name="stop")
    async def stop(self, ctx):
        try:
            voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
            voice.stop()
        except AttributeError:
            embed = discord.Embed(
                description="I'm not connected to a voice channel! ⛔", 
                color=discord.Colour.from_rgb(255,192,203)
            )
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(MusicCommands(bot))