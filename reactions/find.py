import sqlite3

import discord

import util.logger
from commands.find import create_embed
from commands.find import fetch_information
from commands.find import main as command_main
from util.Victor import Victor
from util.static import number_emojis


# data will always be assumed to be modified, and thus saved.
async def main(reaction: discord.Reaction, user: discord.User, obj: dict, victor: Victor) -> bool:
    # Must return a boolean that indicates whether you want the main thread to delete the object in data.
    if obj["pageable"] and (reaction.emoji == '◀️' or reaction.emoji == '▶️'):
        target = await reaction.message.channel.fetch_message(obj["message"])
        if reaction.emoji == '◀️':
            if obj["page"] > 0:
                obj["page"] -= 1
                await command_main(message=target, command={"args": obj["args"]}, victor=victor, page=obj["page"], edit=True)
        elif reaction.emoji == '▶️':
            if obj["page"] < (obj["length"] // 10):
                obj["page"] += 1
                await command_main(message=target, command={"args": obj["args"]}, victor=victor, page=obj["page"], edit=True)
        await reaction.message.remove_reaction("◀️", user)
        await reaction.message.remove_reaction("▶️", user)
    else:
        index = number_emojis.index(reaction.emoji)
        if index == -1 or index >= len(obj["results"]):
            return False
        # use fetch_information and create_embed to make and send embed
        data = await fetch_information(obj["results"][index], victor.client)
        embed = create_embed(data)
        await reaction.message.channel.send(embed=embed)
        for emoji in number_emojis.__reversed__():
            await reaction.message.remove_reaction(emoji, victor.client.user)
    return obj["pageable"]
