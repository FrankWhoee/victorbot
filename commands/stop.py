import sqlite3

import discord

import util
from util.decorators import guildCommand


@guildCommand
async def main(message: discord.Message, client: discord.Client, data: dict, command: dict,
               sqldb: sqlite3.Cursor, logger: util.logger.Logger) -> bool:
    # stops what is currently playing
    if message.guild.voice_client is not None:
        message.guild.voice_client.stop()
    return False


# commands must include a help dictionary with the following keys: name, description, usage
help = {
    "name": "stop",
    "description": "Stops what's currently playing.",
    "usage": ["stop"]
}
