import sqlite3

import discord


async def main(message: discord.Message, client: discord.Client, data: dict, command: dict,
               sqldb: sqlite3.Cursor) -> bool:
    async with message.channel.typing():
        # commands must return a boolean that indicates whether they modified data
        tag = " ".join(command["args"])
        sqldb.execute("SELECT * FROM tags WHERE tag = ? AND guildId = ?", (tag,message.guild.id))
        results = sqldb.fetchall()
        if len(results) == 0:
            await message.channel.send(embed=discord.Embed(title="Error", description="Tag not found.", color=0xFF0000))
            return False
        elif len(results) == 1:
            data = await fetch_information(results[0],client)
            await message.channel.send(embed=create_embed(data))
        else:
            # messageId, guildId, channelId, tag, content, link, authorId
            description = ""
            i = 1
            for result in results:
                tag, content, link, author, guild, channel, message = await fetch_information(result,client)
                description += "{} • {} • {} • {} • {} • [link]({})\n".format(i, message.created_at.strftime("%Y-%m-%d"), author.name + "#" + author.discriminator, channel.name, (content[0:10].strip() + "...") if len(content) > 10 else content, link)
                i += 1
                # TODO(#66): Add paging to find
                # if i >= 10:
                #     break
            embed = discord.Embed(title=tag, description=description, color=0x00ff00)
            await message.channel.send(embed=embed)
    return False

async def fetch_information(result,client):
    channel = client.get_channel(result[2])
    message = await channel.fetch_message(result[0])
    guild = client.get_guild(result[1])
    tag = result[3]
    content = result[4]
    link = result[5]
    author = client.get_user(result[6])
    return tag, content, link, author, guild, channel, message

def create_embed(data):
    tag, content, link, author, guild, channel, message = data
    embed = discord.Embed(title=tag, description=content, color=0x00ff00, url=link)
    embed.set_author(name=author.name, icon_url=author.avatar_url)
    embed.set_footer(text="Message sent in {}, #{} at {}".format(guild.name, channel.name,
                                                                 message.created_at.strftime("%Y-%m-%d %H:%M:%S")))
    return embed

# commands must include a help dictionary with the following keys: name, description, usage
help = {
    "name": "find",
    "description": "Returns list of tagged messages.",
    "usage": ["find <tag>"]
}
