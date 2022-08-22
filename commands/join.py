import sqlite3

import discord

from util.decorators import guildCommand
from util.errors import CommandError


@guildCommand
async def main(message: discord.Message, client: discord.Client, data: dict, command: dict,
               sqldb: sqlite3.Cursor, logger: util.logger.Logger) -> bool:
    if len(command["args"]) == 1:
        channel = client.get_channel(int(command["args"][0]))
    else:
        if message.author.voice is None:
            # send an embed to the user indicating that they need to be in a voice channel
            raise CommandError("You must be in a voice channel to use this command. See `!help join`.")
        channel = message.author.voice.channel
    if channel is not None:
        # loop through client.voice_clients and find the one that is in the same guild as the message
        for voice_client in client.voice_clients:
            if voice_client.guild == message.guild:
                await voice_client.disconnect()
                break
        await channel.connect()
    return False


help = {
    "name": "join",
    "description": "Joins voice channel.",
    "usage": ["join", "join <channelid>"]
}
