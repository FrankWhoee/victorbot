import sqlite3

import discord

import util
from util.Victor import Victor


async def main(message: discord.Message, command: dict, victor: Victor) -> bool:
    # commands must return a boolean that indicates whether they modified data
    victor.data["prefix"] = command["args"][0]
    embed = discord.Embed(title="Prefix", description=f"Set prefix to {command['args'][0]}.", color=0x00ff00)
    await message.channel.send(embed=embed)
    return True


# commands must include a help dictionary with the following keys: name, description, usage
help = {
    "name": "prefix",
    "description": "Set prefix to <prefix>.",
    "usage": ["prefix <prefix>"]
}
