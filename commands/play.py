import random
from os import listdir

import discord

from util.Victor import Victor
from util.decorators import guildCommand
from util.fuzzy import search
from util.vc_util import disconnect_from_guild


@guildCommand
async def main(message: discord.Message, command: dict, victor: Victor) -> bool:
    # get voice client in this current guild
    vc = message.guild.voice_client
    if message.author.voice is not None and message.author.voice.channel is not None:
        channel = message.author.voice.channel
        if vc is None or channel != vc.channel or vc.is_connected() is False:
            await disconnect_from_guild(victor.client, message)
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
                                                    volume=victor.data["guilds"][str(message.guild.id)]["volume"])
        vc.play(audio_source, after=None)


# commands must include a help dictionary with the following keys: name, description, usage
help = {
    "name": "play",
    "description": "Plays a sound file. If no file is specified, a random file will be played.",
    "usage": ["play <filename>""play"]
}
