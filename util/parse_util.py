import discord

from util.fuzzy import search


def extract_guild_channel(client: discord.Client, command: dict, include_voice=False) -> (discord.Guild, discord.TextChannel):
    guild = extract_guild(client, command)
    return guild, extract_channel(guild, command, include_voice, index=1)


def extract_channel(guild: discord.Guild, command: dict, include_voice=False, index=0) -> discord.TextChannel:
    channelfuzzy = command["args"][index]

    if channelfuzzy.isdigit():
        channel = guild.get_channel(int(channelfuzzy))
    else:
        channels = {channel.name: channel for channel in guild.channels if (isinstance(channel, discord.TextChannel) or include_voice)}
        channel = search(channelfuzzy, list(channels.keys()))
        channel = channels[channel]
    return channel


def extract_guild(client: discord.Client, command: dict) -> discord.Guild:
    guildfuzzy = command["args"][0]
    if guildfuzzy.isdigit():
        guild = client.get_guild(int(guildfuzzy))
    else:
        guilds = {guild.name: guild for guild in client.guilds}
        guild = search(guildfuzzy, list(guilds.keys()))
        guild = guilds[guild]
    return guild
