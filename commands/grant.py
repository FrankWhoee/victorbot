import discord
from util.fuzzy import search, map_search


async def main(message: discord.Message, client: discord.Client, data: dict, command: dict) -> bool:
    if len(command["args"]) == 1:
        if command["args"][0] == "list":
            embed = discord.Embed(title="Grants", description="List of all grants in this guild.")
            for user in data["guilds"][str(message.guild.id)]["grants"]:
                embed.add_field(name=client.get_user(int(user)).name,
                                value=client.get_channel(data["guilds"][str(message.guild.id)]["grants"][user]).name)
            await message.channel.send(embed=embed)
            return False
        elif command["args"][0] == "clear":
            data["guilds"][str(message.guild.id)]["grants"] = {}
            embed = discord.Embed(title="Grants", description="Cleared all grants in this guild.", color=0x00ff00)
            await message.channel.send(embed=embed)
            return True

    fuzzy_channel = command["args"][0]
    channels = {c.name: c for c in message.guild.voice_channels}
    channel = search(fuzzy_channel, list(channels.keys()))
    channel = channels[channel]

    fuzzy_names = command["args"][1:]
    fuzzy_names = [name for name in fuzzy_names if not (name.startswith("<@") and name.endswith(">"))]
    names = {m.name: m for m in message.guild.members}
    target_users = map_search(fuzzy_names, list(names.keys())).values()
    target_users = [names[u] for u in target_users]
    target_users += message.mentions
    data_modified = False
    for target_user in target_users:
        if target_user.voice is None:
            if "grants" in data["guilds"][str(message.guild.id)]:
                data["guilds"][str(message.guild.id)]["grants"][str(target_user.id)] = channel.id
            else:
                data["guilds"][str(message.guild.id)]["grants"] = {str(target_user.id): channel.id}
            embed = discord.Embed(title="Grant",
                                  description=f"{target_user.mention} has been granted access to {channel.mention}.",
                                  color=0x00ff00)
            await message.channel.send(embed=embed)
            data_modified = True
        else:
            await target_user.move_to(channel)
            embed = discord.Embed(title="Grant", description=f"{target_user.mention} has been moved to {channel.mention}.",
                                  color=0x00ff00)
            await message.channel.send(embed=embed)
    return data_modified


help = {
    "name": "grant",
    "description": "Moves <username> to <channel>. If <username> is not in a voice channel yet, they will be moved as "
                   "soon as then join.",
    "usage": ["grant <channel> <username>", "grant list", "grant clear"]
}
