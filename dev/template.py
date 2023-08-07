import sqlite3

import discord

import util.logger
from util.Victor import Victor


async def main(message: discord.Message, command: dict, victor: Victor) -> bool:
    # commands must return a boolean that indicates whether they modified data
    return False

# commands must include a help dictionary with the following keys: name, description, usage
help = {
    "name": "template",
    "description": "Template command.",
    "usage": ["template"]
}
