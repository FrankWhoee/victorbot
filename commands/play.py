import random
import sqlite3
from os import listdir

import discord

import util
from util.decorators import guildCommand
from util.fuzzy import search


@guildCommand
async def main(message: discord.Message, client: discord.Client, data: dict, command: dict,
               sqldb: sqlite3.Cursor, logger: util.logger.Logger) -> bool:
    # get voice client in this current guild
    vc = message.guild.voice_client
    if message.author.voice is not None and message.author.voice.channel is not None:
        channel = message.author.voice.channel
        if vc is None or channel != vc.channel:
            vc = await channel.connect()
        vc.stop()
    else:
        embed = discord.Embed(title="Error", description="You are not in a voice channel.", color=0xFF0000)
        await message.channel.send(embed=embed)
        return False

    files = listdir("sounds")

    query = " ".join(command["args"])
    if query is not None:
        if len(command["args"]) > 0:
            filename = search(query, files)
        else:
            filename = random.choice(files)
        audio_source = discord.FFmpegPCMAudio('sounds/' + filename)
        audio_source = discord.PCMVolumeTransformer(audio_source,
                                                    volume=data["guilds"][str(message.guild.id)]["volume"])
        vc.play(audio_source, after=None)


# commands must include a help dictionary with the following keys: name, description, usage
help = {
    "name": "play",
    "description": "Plays a sound file. If no file is specified, a random file will be played.",
    "usage": ["play <filename>""play"]
}
