import discord
import sqlite3

async def main(message: discord.Message, client: discord.Client, data: dict, command: dict, sqldb: sqlite3.Cursor) -> bool:
    # commands must return a boolean that indicates whether they modified data
    data["prefix"] = command["args"][0]
    embed = discord.Embed(title="Prefix", description=f"Set prefix to {command['args'][0]}.", color=0x00ff00)
    await message.channel.send(embed=embed)
    return True

# commands must include a help dictionary with the following keys: name, description, usage
help = {
    "name": "prefix",
    "description": "Set prefix to <prefix>.",
    "usage": ["prefix <prefix>"]
}
