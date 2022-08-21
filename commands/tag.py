import sqlite3

import discord


async def main(message: discord.Message, client: discord.Client, data: dict, command: dict,
               sqldb: sqlite3.Cursor) -> bool:
    if len(command["args"]) == 2:
        target = await message.channel.fetch_message(command["args"][0])
        tag = command["args"][1]
    elif message.reference is not None:
        target = await message.channel.fetch_message(message.reference.message_id)
        tag = command["args"][0]
    else:
        tag = command["args"][0]
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
    try:
        sqldb.execute("INSERT INTO tags(messageId, guildId, channelId, tag, content, link, authorId) VALUES (?,?,?,?,?,?,?)",
                      (target.id, target.guild.id, target.channel.id, tag, target.content, target.jump_url, target.author.id))
        embed = discord.Embed(title="Success", description="Message tagged.", color=0x00ff00)
        await message.channel.send(embed=embed)
    except:
        await message.channel.send(embed=discord.Embed(title="Error", description="Writing to tags database failed.", color=0xFF0000))
    return True


# commands must include a help dictionary with the following keys: name, description, usage
help = {
    "name": "tag",
    "description": "Tags message with <tag>. If a <messageid> is provided, <messageid> is tagged. If the command replies to a message, the replied message will be tagged, otherwise the next message up is tagged.",
    "usage": ["tag <tag>", "tag <messageid> <tag>"]
}
