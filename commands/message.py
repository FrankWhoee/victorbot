import discord

from util.data_util import initializeGuildData
from util.parse_util import extract_channel, extract_guild


async def main(message: discord.Message, client: discord.Client, data: dict, command: dict) -> bool:
    # commands must return a boolean that indicates whether they modified data
    if message.guild is None:
        guild = extract_guild(client, command)
        channel = extract_channel(guild, command)
        message_string = " ".join(command["args"][2:])
    else:
        guild = message.guild
        channel = extract_channel(guild, command)
        message_string = " ".join(command["args"][1:])

    # if message_string is empty, return an error
    if message_string == "":
        embed = discord.Embed(title="Error", description="No message specified.", color=0xff0000)
        await message.channel.send(embed=embed)
        return False

    # create an embed
    embed = discord.Embed(title="Message",
                          description=f"Sending message to {channel.mention} in {guild.name}. React with ✅ to confirm or ❌ to cancel.",
                          color=0x00FF00)
    embed.add_field(name="Message Contents", value=message_string)
    embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
    react_message = await message.channel.send(embed=embed)
    await react_message.add_reaction("✅")
    await react_message.add_reaction("❌")
    initializeGuildData(guild, data)
    if message.guild is None:
        data["dms"][str(message.author.id)]["reactions"][str(react_message.id)] = {"function": "message",
                                                                                   "args": [channel.id, message_string]}
    else:
        data["guilds"][str(guild.id)]["reactions"][str(react_message.id)] = {"function": "message",
                                                                             "args": [channel.id, message_string]}
    return True


# commands must include a help dictionary with the following keys: name, description, usage
help = {
    "name": "message",
    "description": "Sends a message to a channel in a guild.",
    "usage": ["message <guild> <channel> <message>", "message <guildid> <channelid> <message>"]
}
