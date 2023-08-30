import sqlite3

import discord

import util
from util.Victor import Victor
from util.decorators import guildCommand


@guildCommand
async def main(message: discord.Message, command: dict, victor: Victor) -> bool:
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
