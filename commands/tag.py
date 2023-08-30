import sqlite3
import traceback

import discord

import util
from util.Victor import Victor
from util.decorators import guildCommand


@guildCommand
async def main(message: discord.Message, command: dict, victor: Victor) -> bool:
    if len(command["args"]) > 0 and len(command["args"][0]) >= 10 and command["args"][0].isdigit():
        target = await message.channel.fetch_message(command["args"][0])
        tag = " ".join(command["args"][1:])
    elif message.reference is not None:
        target = await message.channel.fetch_message(message.reference.message_id)
        tag = " ".join(command["args"])
    else:
        tag = " ".join(command["args"])
        nextflag = False
        size = 5
        while not nextflag and size < 50:
            hist = await message.channel.history(limit=size).flatten()
            for m in hist:
                if nextflag:
                    target = m
                    break
                elif m.id == message.id:
                    nextflag = True
        size += 5
    if tag == "":
        tag = "pinned"
    try:
        victor.sqldb.execute("INSERT INTO tags(messageId, guildId, channelId, tag, content, link, authorId, timeAdded, messageCreatedAt) VALUES (?,?,?,?,?,?,?,?,?)",
                      (target.id, target.guild.id, target.channel.id, tag, target.content, target.jump_url, target.author.id, message.created_at.timestamp(), target.created_at.timestamp()))
        embed = discord.Embed(title="Success", description="[Message]({}) tagged as '{}'.".format(target.jump_url, tag), color=0x00ff00)
        await message.channel.send(embed=embed)
    except sqlite3.IntegrityError:
        embed = discord.Embed(title="Error", description="Message is already tagged.", color=0xFF0000)
        await message.channel.send(embed=embed)
    return True


# commands must include a help dictionary with the following keys: name, description, usage
help = {
    "name": "tag",
    "description": "Tags message with <tag>. If a <messageid> is provided as the first argument, <messageid> is tagged. If the command replies to a message, the replied message will be tagged, otherwise the next message up is tagged. Tags can not be only numbers.",
    "usage": ["tag <tag>", "tag <messageid> <tag>"]
}
