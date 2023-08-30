import sqlite3

import discord

import util.logger
from util.Victor import Victor


async def main(message: discord.Message, command: dict, victor: Victor) -> bool:
    await message.channel.send(file=discord.File(victor.logger.log_file))

# commands must include a help dictionary with the following keys: name, description, usage
help = {
    "name": "logs",
    "description": "Sends current logs.",
    "usage": ["logs"]
}
