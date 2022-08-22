import sqlite3

import discord

import util.logger


async def main(message: discord.Message, client: discord.Client, data: dict, command: dict, sqldb: sqlite3.Cursor, logger: util.logger.Logger) -> bool:
    # commands must return a boolean that indicates whether they modified data
    return False

# commands must include a help dictionary with the following keys: name, description, usage
help = {
    "name": "template",
    "description": "Template command.",
    "usage": ["template"]
}
