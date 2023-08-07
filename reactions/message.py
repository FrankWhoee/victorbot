import sqlite3

import discord

# data will always be assumed to be modified, and thus saved.
import util.logger
from util.Victor import Victor


async def main(reaction: discord.Reaction, user: discord.User, obj: dict, victor: Victor) -> bool:
    # Must return a boolean that indicates whether you want the main thread to delete the object in data.
    if reaction.emoji == "✅":
        # get the channel and message from the data
        channel = victor.client.get_channel(obj["args"][0])
        message = obj["args"][1]
        # send the message
        await channel.send(message)
    await reaction.message.remove_reaction("❌", victor.client.user)
    await reaction.message.remove_reaction("✅", victor.client.user)
    return False
