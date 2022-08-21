import sqlite3

import discord

# data will always be assumed to be modified, and thus saved.
async def main(reaction: discord.Reaction, user: discord.User, client: discord.Client, data: dict, obj: dict, sqldb: sqlite3.Cursor):
    # it is the main thread's responsibility to delete the object in data
    if reaction.emoji == "✅":
        # get the channel and message from the data
        channel = client.get_channel(obj["args"][0])
        message = obj["args"][1]
        # send the message
        await channel.send(message)
    await reaction.message.remove_reaction("❌", client.user)
    await reaction.message.remove_reaction("✅", client.user)
    return True