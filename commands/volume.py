import sqlite3

import discord

import util
from util.decorators import guildCommand


@guildCommand
async def main(message: discord.Message, client: discord.Client, data: dict, command: dict,
               sqldb: sqlite3.Cursor, logger: util.logger.Logger) -> bool:
    # Changes the volume to the given value.
    if len(command["args"]) == 1:
        data["guilds"][str(message.guild.id)]["volume"] = float(command["args"][0]) / 100
        embed = discord.Embed(title="Volume", description=f"Volume set to {command['args'][0]}%.", color=0x00FF00)
        await message.channel.send(embed=embed)
        return True
    else:
        embed = discord.Embed(title="Volume", description=f'{data["guilds"][str(message.guild.id)]["volume"] * 100}%',
                              color=0x00FF00)
        await message.channel.send(embed=embed)
        return False


# commands must include a help dictionary with the following keys: name, description, usage
help = {
    "name": "volume",
    "description": "Change the volume or check the volume. Accepts values between 0 and 100.",
    "usage": ["volume <volume>", "volume"]
}
