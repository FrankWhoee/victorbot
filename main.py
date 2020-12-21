import asyncio

import discord
import json
import os
from os import walk

if os.path.exists("secrets.json"):
    with open("secrets.json") as f:
        secrets = json.load(f)
else:
    secrets = {}
    secrets["token"] = os.environ.get("token")

TOKEN = secrets["token"]
client = discord.Client()
prefix = "`"
vc = None
volume = 1

def current_vc(guild):
    for vc in client.voice_clients:
        if vc.guild == guild:
            return vc

def get_score(query, compare):
    score = 0
    for letter in compare:
        if letter in query:
            score += 0.5
    if min(len(compare), len(query)) == len(query):
        for i in range(0,len(query)):
            if query[i] == compare[i]:
                score += 1
    else:
        for i in range(0,len(compare)):
            if query[i] == compare[i]:
                score += 1
    return score


def search_sound(query):
    scores = {}
    f = []
    for (dirpath, dirnames, filenames) in walk("sounds"):
        f.extend(filenames)
        break
    for file in f:
        scores[file] = get_score(query, file)
    max = list(scores.keys())[0]
    for s in scores:
        if scores[s] > scores[max]:
            max = s
    return max


@client.event
async def on_message(message):
    global vc
    global volume
    param = None
    # Filter out non-command messages
    if message.author == client.user:
        return
    if len(message.content.split(" ")) < 2:
        command = message.content
    elif prefix in message.content:
        command = message.content.split(" ")[0]
        param = message.content.split(" ")[1:]
    command = command[1:]
    if not message.content.startswith(prefix):
        return
    if command == "join":
        if client.voice_clients:
            await current_vc(message.guild).disconnect()
        vc = await message.author.voice.channel.connect()
    if command == "leave":
        await current_vc(message.guild).disconnect()
    if command == "play":
        if not client.voice_clients:
            vc = await message.author.voice.channel.connect()
        elif current_vc(message.guild).channel != message.author.voice.channel:
            await current_vc(message.guild).disconnect()
            vc = await message.author.voice.channel.connect()
        if not discord.opus.is_loaded():
            discord.opus.load_opus('opus')
        print('sounds/' + search_sound(param[0]))
        # audio_source = discord.FFmpegPCMAudio('sounds/' + search_sound(param[0]))
        audio_source = discord.FFmpegPCMAudio('sounds/hooah.mp3')
        audio_source = discord.PCMVolumeTransformer(audio_source, volume=volume)
        vc.play(audio_source, after=None)
    if command == "volume":
        if not param:
            await message.channel.send("Volume is " + str(volume * 100) + "% right now.")
        else:
            volume = float(param[0]) / 100
            await message.channel.send("Volume is now " + str(volume * 100) + "%")

@client.event
async def on_member_join(member):
    print("New member joined.")


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
