import sqlite3

import discord

import util
from util.Victor import Victor
from util.decorators import guildCommand


@guildCommand
async def main(message: discord.Message, command: dict, victor: Victor) -> bool:
    if message.guild.voice_client is not None:
        await message.guild.voice_client.disconnect(force=True)
    else:
        embed = discord.Embed(title="Error", description="I am not in a voice channel.", color=0xFF0000)
        await message.channel.send(embed=embed)
    return False


help = {
    "name": "leave",
    "description": "Leaves voice channel.",
    "usage": ["leave"]
}
