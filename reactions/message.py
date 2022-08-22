import sqlite3

import discord

# data will always be assumed to be modified, and thus saved.
import util.logger


async def main(reaction: discord.Reaction, user: discord.User, client: discord.Client, data: dict, obj: dict,
               sqldb: sqlite3.Cursor, logger: util.logger.Logger) -> bool:
    # Must return a boolean that indicates whether you want the main thread to delete the object in data.
    if reaction.emoji == "✅":
        # get the channel and message from the data
        channel = client.get_channel(obj["args"][0])
        message = obj["args"][1]
        # send the message
        await channel.send(message)
    await reaction.message.remove_reaction("❌", client.user)
    await reaction.message.remove_reaction("✅", client.user)
    return False
