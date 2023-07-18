import sqlite3

import discord

import util.logger


async def main(message: discord.Message, client: discord.Client, data: dict, command: dict, sqldb: sqlite3.Cursor, logger: util.logger.Logger) -> bool:
    # commands must return a boolean that indicates whether they modified data
    data["guilds"][str(message.guild.id)]["sleep"] = command["args"][0
    return True

# commands must include a help dictionary with the following keys: name, description, usage
help = {
    "name": "sleep",
    "description": "Sets your sleep time. The bot kicks you out of call at sleep time. <time> should be in the format of HH:MM.",
    "usage": ["sleep <time>", "sleep off/cancel/disable"]
}
