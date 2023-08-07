import datetime
import sqlite3

import discord

import util
from util.Victor import Victor
from util.decorators import guildCommand
from util.static import number_emojis


@guildCommand
async def main(message: discord.Message, command: dict, victor: Victor, page=0, edit=False) -> bool:
    async with message.channel.typing():
        if len(command["args"]) == 0:
            victor.sqldb.execute("SELECT tag, COUNT(tag)  FROM tags WHERE guildId = ? GROUP BY tag", (message.guild.id,))
            tags = victor.sqldb.fetchall()
            if len(tags) == 0:
                embed = discord.Embed(title="Error", description="No tags found.", color=0xFF0000)
                await message.channel.send(embed=embed)
                return False
            else:
                description = ""
                i = 1
                for tag in tags:
                    description += "`" + str(i) + "`⠀" + tag[0] + ", " + str(tag[1]) + " tags" + "\n"
                    i += 1
                embed = discord.Embed(title="All Tags", description=description, color=0x00ff00)
                await message.channel.send(embed=embed)
            return False
        # commands must return a boolean that indicates whether they modified data
        tag = " ".join(command["args"])
        victor.sqldb.execute("SELECT * FROM tags WHERE tag = ? AND guildId = ? LIMIT ?,?",
                      (tag, message.guild.id, page * 10, 10))

        results = victor.sqldb.fetchall()
        victor.sqldb.execute("SELECT COUNT(tag) FROM tags WHERE tag = ? AND guildId = ?", (tag, message.guild.id))
        tag_length = victor.sqldb.fetchone()[0]
        if tag_length == 0:
            await message.channel.send(embed=discord.Embed(title="Error", description="Tag not found.", color=0xFF0000))
            return False
        elif tag_length == 1 and not edit:
            data = await fetch_information(results[0], victor.client)
            await message.channel.send(embed=create_embed(data))
        else:
            # messageId, guildId, channelId, tag, content, link, authorId
            embed = await embed_list_tags(victor.client, results, tag)
            if edit:
                await message.edit(embed=embed)
                target = message
            else:
                target = await message.channel.send(embed=embed)

            victor.data["guilds"][str(message.guild.id)]["reactions"][str(target.id)] = {"function": "find",
                                                                                  "results": results,
                                                                                  "message": target.id,
                                                                                  "pageable": tag_length > 10 or edit,
                                                                                  "length": tag_length,
                                                                                  "page": page, "args": command["args"]}
    if len(results) > 1:
        for i in range(len(results)):
            await target.add_reaction(number_emojis[i])
    if tag_length > 10:

        await target.add_reaction("◀️")
        await target.add_reaction("▶️")

    return False


async def embed_list_tags(client, results, tag):
    description = ""
    i = 1
    for result in results:
        tag, content, link, author, guild, channel, message_created_at = await fetch_information(result, client)
        description += "`{}`⠀{} • {} • {} • [Link]({})\n".format(i, datetime.datetime.fromtimestamp(message_created_at).strftime("%Y-%m-%d"),
                                                                 author.name + "#" + author.discriminator,
                                                                 (content[0:20].strip() + "...") if len(
                                                                     content) > 20 else content, link)
        i += 1
    embed = discord.Embed(title=tag, description=description, color=0x00ff00)
    return embed


async def fetch_information(result, client):
    channel = client.get_channel(result[2])
    guild = client.get_guild(result[1])
    tag = result[3]
    content = result[4]
    link = result[5]
    author = client.get_user(result[6])
    message_created_at = result[7]
    return tag, content, link, author, guild, channel, message_created_at


def create_embed(data):
    tag, content, link, author, guild, channel, message_created_at = data
    embed = discord.Embed(title=tag, description=content, color=0x00ff00, url=link)
    embed.set_author(name=author.name, icon_url=author.avatar_url)
    embed.set_footer(text="Message sent in {}, #{} at {}".format(guild.name, channel.name,
                                                                 datetime.datetime.fromtimestamp(message_created_at).strftime("%Y-%m-%d %H:%M:%S")))
    return embed


# commands must include a help dictionary with the following keys: name, description, usage
help = {
    "name": "find",
    "description": "Returns list of tagged messages.",
    "usage": ["find <tag>"]
}
