import sqlite3

import discord

import util
from util.Victor import Victor


async def main(message: discord.Message, command: dict, victor: Victor) -> bool:
    if message.guild is not None:
        if "subscribe_channel" not in victor.guild_data(message.guild.id):
            embed = discord.Embed(title="Unsubscribe", description="No channel is subscribed in this guild.",
                                  color=0xff0000)
            await message.channel.send(embed=embed)
            return False
        del victor.guild_data(message.guild.id)["subscribe_channel"]
        embed = discord.Embed(title="Unsubscribe", description="Unsubscribed from this channel.")
        await message.channel.send(embed=embed)
    else:
        if message.author.id not in victor.data["dmsubscribers"]:
            embed = discord.Embed(title="Unsubscribe", description="No channel is subscribed in this DM.",
                                  color=0xff0000)
            await message.channel.send(embed=embed)
            return False
        victor.data["dmsubscribers"].remove(message.author.id)
        embed = discord.Embed(title="Unsubscribe", description="Unsubscribed from this channel.")
        await message.channel.send(embed=embed)
    return True


help = {
    "name": "unsubscribe",
    "description": "Unsubscribes this channel from boot update.",
    "usage": ["unsubscribe"]
}
