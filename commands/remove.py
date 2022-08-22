import sqlite3
import traceback

import discord

import util.logger
from util.decorators import guildCommand

@guildCommand
async def main(message: discord.Message, client: discord.Client, data: dict, command: dict, sqldb: sqlite3.Cursor,
               logger: util.logger.Logger) -> bool:
    if len(command["args"]) >= 1:
        target = await message.channel.fetch_message(command["args"][0])
        sqldb.execute("SELECT * FROM tags WHERE messageId = ? AND guildId = ? AND channelId = ?",
                      (target.id, target.guild.id, target.channel.id))
        tag = sqldb.fetchone()[3]
        jump_url = target.jump_url
        id = target.id
        guild = target.guild.id
        channel = target.channel.id
    elif message.reference is not None:
        target = await message.channel.fetch_message(message.reference.message_id)
        sqldb.execute("SELECT * FROM tags WHERE messageId = ? AND guildId = ? AND channelId = ?", (target.id, target.guild.id, target.channel.id))
        tag = sqldb.fetchone()[3]
        jump_url = target.jump_url
        id = target.id
        guild = target.guild.id
        channel = target.channel.id
    else:
        # Get the last tag added to sqldb
        sqldb.execute("SELECT * FROM tags ORDER BY timeAdded DESC LIMIT 1")
        target = sqldb.fetchone()
        tag = target[3]
        jump_url = target[5]
        id = target[0]
        guild = target[1]
        channel = target[2]
    # delete guild, channel, id from sqldb
    try:
        # check if message is in sqldb
        sqldb.execute("SELECT * FROM tags WHERE messageId=? AND guildId=? AND channelId=?", (id, guild, channel))
        if sqldb.fetchone() is not None:
            sqldb.execute("DELETE FROM tags WHERE messageId=? AND guildId=? AND channelId=?", (id, guild, channel))
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
    "name": "template",
    "description": "Template command.",
    "usage": ["template"]
}
