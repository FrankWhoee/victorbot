import discord
from util.fuzzy import search

async def main(message: discord.Message, client: discord.Client, data: dict, command: dict) -> bool:
    # commands must return a boolean that indicates whether they modified data

    guildfuzzy = command["args"][0]
    channelfuzzy = command["args"][1]
    message_string = " ".join(command["args"][2:])

    # detect if guildfuzzy is an id or a name
    if guildfuzzy.isdigit():
        guild = client.get_guild(int(guildfuzzy))
    else:
        guilds = {guild.name: guild for guild in client.guilds}
        guild = search(guildfuzzy, list(guilds.keys()))
        guild = guilds[guild]

    # detect if channelfuzzy is an id or a name
    if channelfuzzy.isdigit():
        channel = guild.get_channel(int(channelfuzzy))
    else:
        channels = {channel.name: channel for channel in guild.channels}
        channel = search(channelfuzzy, list(channels.keys()))
        channel = channels[channel]

    # create an embed
    embed = discord.Embed(title="Message", description=f"Sending message to {channel.mention} in {guild.name}. React with ✅ to confirm or ❌ to cancel.", color=0x00FF00)
    embed.add_field(name="Message Contents", value=message_string)
    embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
    react_message = await message.channel.send(embed=embed)
    data["guilds"][str(guild.id)]["reactions"][str(react_message.id)] = {"function": "message", "args": [channel, message_string]}

    return False

# commands must include a help dictionary with the following keys: name, description, usage
help = {
    "name": "message",
    "description": "Sends a message to a channel in a guild.",
    "usage": ["message <guild> <channel> <message>", "message <guildid> <channelid> <message>"]
}
