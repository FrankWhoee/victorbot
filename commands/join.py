import sqlite3

import discord

from util.Victor import Victor
from util.decorators import guildCommand
from util.errors import CommandError
import util
from util.fuzzy import search
from util.vc_util import disconnect_from_guild


@guildCommand
async def main(message: discord.Message, command: dict, victor: Victor) -> bool:
    if len(command["args"]) > 0 and len(command["args"][0]) >= 10 and command["args"][0].isdigit():
        channel = victor.client.get_channel(int(command["args"][0]))
    elif len(command["args"]) > 0:
        fuzzy_channel = command["args"][0]
        channels = {c.name: c for c in message.guild.voice_channels}
        channel = search(fuzzy_channel, list(channels.keys()))
        channel = channels[channel]
    else:
        if message.author.voice is None:
            # send an embed to the user indicating that they need to be in a voice channel
            raise CommandError("You must be in a voice channel to use this command. See `!help join`.")
        channel = message.author.voice.channel
    if channel is not None:
        # loop through client.voice_clients and find the one that is in the same guild as the message
        await disconnect_from_guild(victor.client, message)
        await channel.connect()
    return False

help = {
    "name": "join",
    "description": "Joins voice channel. Joins your voice channel if no channel is specified.",
    "usage": ["join", "join <channelid>"]
}
