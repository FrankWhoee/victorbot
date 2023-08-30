import sqlite3

import discord

import util

from util.Victor import Victor


async def main(message: discord.Message, command: dict, victor: Victor) -> bool:
    if victor.data["dev"]:
        victor.data["dev"] = False
        embed = discord.Embed(title="Dev mode", description="Dev mode disabled.")
        await message.channel.send(embed=embed)
    else:
        victor. data["dev"] = True
        embed = discord.Embed(title="Dev mode", description="Dev mode enabled.", color=0x00ff00)
        await message.channel.send(embed=embed)
    return True


help = {
    "name": "dev",
    "description": "Toggle developer mode.",
    "usage": ["dev"]
}
