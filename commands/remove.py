import sqlite3
import traceback

import discord

import util.logger
from util.Victor import Victor
from util.decorators import guildCommand

@guildCommand
async def main(message: discord.Message, command: dict, victor: Victor) -> bool:
    if len(command["args"]) >= 1:
        target = await message.channel.fetch_message(command["args"][0])
        victor.sqldb.execute("SELECT * FROM tags WHERE messageId = ? AND guildId = ? AND channelId = ?",
                      (target.id, target.guild.id, target.channel.id))
        tag = victor.sqldb.fetchone()[3]
        jump_url = target.jump_url
        id = target.id
        guild = target.guild.id
        channel = target.channel.id
    elif message.reference is not None:
        target = await message.channel.fetch_message(message.reference.message_id)
        victor.sqldb.execute("SELECT * FROM tags WHERE messageId = ? AND guildId = ? AND channelId = ?", (target.id, target.guild.id, target.channel.id))
        tag = victor.sqldb.fetchone()[3]
        jump_url = target.jump_url
        id = target.id
        guild = target.guild.id
        channel = target.channel.id
    else:
        # Get the last tag added to sqldb
        victor.sqldb.execute("SELECT * FROM tags ORDER BY timeAdded DESC LIMIT 1")
        target = victor.sqldb.fetchone()
        tag = target[3]
        jump_url = target[5]
        id = target[0]
        guild = target[1]
        channel = target[2]
    # delete guild, channel, id from sqldb
    try:
        # check if message is in sqldb
        victor.sqldb.execute("SELECT * FROM tags WHERE messageId=? AND guildId=? AND channelId=?", (id, guild, channel))
        if victor.sqldb.fetchone() is not None:
            victor.sqldb.execute("DELETE FROM tags WHERE messageId=? AND guildId=? AND channelId=?", (id, guild, channel))
            embed = discord.Embed(title="Success", description="[Message]({}) untagged from '{}'.".format(jump_url, tag), color=0x00ff00)
            await message.channel.send(embed=embed)
        else:
            embed = discord.Embed(title="Error", description="Message is not tagged.", color=0xFF0000)
            await message.channel.send(embed=embed)
    except Exception as e:
        traceback.print_exc()
        await message.channel.send(embed=discord.Embed(title="Error", description="Tag not found.", color=0xFF0000))

    return True


# commands must include a help dictionary with the following keys: name, description, usage
help = {
    "name": "remove",
    "description": "Removes a tagged message. If you give a message ID, that message will be untagged, otherwise if you reply to a message, the replied message will be untagged, otherwise the last message tagged is untagged.",
    "usage": ["remove", "remove <messageid>"]
}
