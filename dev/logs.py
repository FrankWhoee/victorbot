import sqlite3

import discord

import util.logger


async def main(message: discord.Message, client: discord.Client, data: dict, command: dict, sqldb: sqlite3.Cursor, logger: util.logger.Logger) -> bool:
    await message.channel.send(file=discord.File(logger.log_file))

# commands must include a help dictionary with the following keys: name, description, usage
help = {
    "name": "logs",
    "description": "Sends current logs.",
    "usage": ["logs"]
}
