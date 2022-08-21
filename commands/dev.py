import sqlite3
import discord

async def main(message: discord.Message, client: discord.Client, data: dict, command: dict, sqldb: sqlite3.Cursor) -> bool:
    if data["dev"]:
        data["dev"] = False
        embed = discord.Embed(title="Dev mode", description="Dev mode disabled.")
        await message.channel.send(embed=embed)
    else:
        data["dev"] = True
        embed = discord.Embed(title="Dev mode", description="Dev mode enabled.", color=0x00ff00)
        await message.channel.send(embed=embed)
    return True

help = {
    "name": "dev",
    "description": "Toggle developer mode.",
    "usage": ["dev"]
}
