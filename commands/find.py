import sqlite3

import discord


async def main(message: discord.Message, client: discord.Client, data: dict, command: dict,
               sqldb: sqlite3.Cursor) -> bool:
    # commands must return a boolean that indicates whether they modified data
    tag = command["args"][0]
    sqldb.execute("SELECT * FROM tags WHERE tag = ?", (tag,))
    results = sqldb.fetchall()
    if len(results) == 0:
        await message.channel.send(embed=discord.Embed(title="Error", description="Tag not found.", color=0xFF0000))
        return False
    for result in results:
        # create embed and send it
        # messageId, guildId, channelId, tag, content, link, authorId
        print("creating embed")
        channel = client.get_channel(result[2])
        message = await channel.fetch_message(result[0])
        guild = client.get_guild(result[1])
        tag = result[3]
        content = result[4]
        link = result[5]
        author = client.get_user(result[6])
        embed = discord.Embed(title=tag, description=content, color=0x00ff00, url=link)
        embed.set_author(name=author.name, icon_url=author.avatar_url)
        embed.set_footer(text="Message sent in {}, #{} at {}".format(guild.name, channel.name, message.created_at.strftime("%Y-%m-%d %H:%M:%S")))
        await message.channel.send(embed=embed)
    return False


# commands must include a help dictionary with the following keys: name, description, usage
help = {
    "name": "find",
    "description": "Returns list of tagged messages.",
    "usage": ["find <tag>"]
}
