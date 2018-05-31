import discord
import asyncio
import sys
import os
from discord.ext import commands
from discord.ext.commands import Bot
import time
import datetime
from subprocess import Popen
import traceback
from bs4 import BeautifulSoup
import requests

client = discord.Client()

nowplaying_song = ""
nowplaying_song_stored = ""
nowplaying_artist = ""

async def play_stream():
    try:
        global nowplaying_song
        global nowplaying_song_stored
        global nowplaying_artist
        voice_channel = discord.Object(id='445826635401265152')
        voice = await client.join_voice_channel(voice_channel)
        await client.change_presence(game=discord.Game(name=None))
        player = voice.create_ffmpeg_player('KAFA.mp3')
        player.volume = 0.0
        player.start()
        for _ in range(10):
            player.volume = player.volume + .05
            await asyncio.sleep(0.5)
        player.volume = 0.5
        await asyncio.sleep(15)
        player = voice.create_ffmpeg_player('http://ice9.securenetsystems.net/KAFA')
        player.volume = 0.0
        player.start()
        for _ in range(10):
            player.volume = player.volume + .05
            await asyncio.sleep(0.5)
        player.volume = 0.5

        while player.is_playing():
            today = datetime.date.today()
            page = requests.get("http://streamdb7web.securenetsystems.net/v5/sd/index.cfm?stationCallSign=KAFA")
            soup = BeautifulSoup(page.content, 'html.parser')
            nowplaying_song = soup.find_all(class_="cover-overlay-title", limit=1)
            nowplaying_artist = soup.find_all(class_="cover-overlay-artist", limit=1)
            for res in nowplaying_song:
                nowplaying_song = res.text
            for res in nowplaying_artist:
                nowplaying_artist = res.text
            if nowplaying_song != nowplaying_song_stored:
                await asyncio.sleep(3)
                os.system('cls')
                print("Stream OK ", datetime.datetime.now())
                print("Now playing " + nowplaying_song + " by " + nowplaying_artist)
                await client.change_presence(game=discord.Game(name=nowplaying_song + " by " + nowplaying_artist))
                nowplaying_song_stored = nowplaying_song
                await asyncio.sleep(2)
            else:
                await asyncio.sleep(5)
                pass
            
        else:
            print("Stream Error " , datetime.datetime.now())
            await client.change_presence(game=None, status=discord.Status.dnd)
            await asyncio.sleep(5)
            Popen("Radio.py", shell=True)
    except:
        Popen("Radio.py", shell=True)
            
@client.event
async def on_ready():
    await asyncio.sleep(1)
    await client.change_presence(game=discord.Game(name=None), status=discord.Status.dnd)
    await asyncio.sleep(5)
    print("Stream Starting " , datetime.datetime.now())
    try:
        await play_stream()
    except:
        Popen("Radio.py", shell=True)
      
client.run('', bot=True)
