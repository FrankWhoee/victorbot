import sqlite3
from util.static import number_emojis
from commands.find import fetch_information
from commands.find import create_embed
import discord

# data will always be assumed to be modified, and thus saved.
async def main(reaction: discord.Reaction, user: discord.User, client: discord.Client, data: dict, obj: dict, sqldb: sqlite3.Cursor):
    # it is the main thread's responsibility to delete the object in data
    index = number_emojis.index(reaction.emoji)
    if index == -1:
        return False
    # use fetch_information and create_embed to make and send embed
    data = await fetch_information(obj["results"][index],client)
    embed = create_embed(data)
    await reaction.message.channel.send(embed=embed)
    for emoji in number_emojis.__reversed__():
        await reaction.message.remove_reaction(emoji, client.user)
    return False