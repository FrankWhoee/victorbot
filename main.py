import asyncio
import discord
import json
import os
from os import walk
import subprocess

intents = discord.Intents.default()
intents.members = True

if os.path.exists("secrets.json"):
    with open("secrets.json") as f:
        secrets = json.load(f)
else:
    secrets = {}
    secrets["token"] = os.environ.get("token")

TOKEN = secrets["token"]
client = discord.Client(intents=intents)
prefix = "`"
vc = None
volume = 0.25

admin = [194857448673247235, 385297155503685632]


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
        for i in range(0, len(query)):
            if query[i] == compare[i]:
                score += 1
    else:
        for i in range(0, len(compare)):
            if query[i] == compare[i]:
                score += 1
    qsplit = query.split(" ")
    csplit = compare.split(" ")
    for s in qsplit:
        if s in csplit:
            score += 3
    return score


def search_sound(query):
    scores = {}
    f = []
    for (dirpath, dirnames, filenames) in walk("sounds"):
        f.extend(filenames)
        break
    for file in f:
        scores[file] = get_score(query, file.replace(".mp3",""))
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
        elif message.author.voice != None and current_vc(message.guild).channel != message.author.voice.channel:
            await current_vc(message.guild).disconnect()
            vc = await message.author.voice.channel.connect()
        vc.stop()
        audio_source = discord.FFmpegPCMAudio('sounds/' + search_sound(" ".join(param)))
        audio_source = discord.PCMVolumeTransformer(audio_source, volume=volume)
        vc.play(audio_source, after=None)
    if command == 'stop':
        vc.stop()
    if command == "volume":
        if not param:
            await message.channel.send("Volume is " + str(volume * 100) + "% right now.")
        else:
            volume = float(param[0]) / 100
            await message.channel.send("Volume is now " + str(volume * 100) + "%")
    if command == "focus":
        if not param and message.author.id in [194857448673247235, 385297155503685632]:
            for vch in message.guild.voice_channels:
                if not vch.members and not vch.id == 758559024962207795:
                    await message.guild.get_member(194857448673247235).move_to(vch)
                    await message.guild.get_member(385297155503685632).move_to(vch)
                    break
        elif (message.author.roles[len(message.author.roles) - 1] >= message.guild.get_role(
                756005374955487312) and message.author in message.mentions) or (
                message.author.roles[len(message.author.roles) - 1] >= message.guild.get_role(685269061512331288)):
            for vch in message.guild.voice_channels:
                if not vch.members and not vch.id == 758559024962207795:
                    for m in message.mentions:
                        await m.move_to(vch)
                    break
    if command == "pull":
        if message.author.id in admin:
            proc = await asyncio.create_subprocess_exec(
                'git', 'pull',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE)
            stdout, stderr = await proc.communicate()
            embed = discord.Embed(title="Git Pull Output", description=stdout.decode("utf-8"), colour=0xffffff)
            await message.channel.send(embed=embed)
        else:
            await message.channel.send("You are not authorized to use this command.")


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
