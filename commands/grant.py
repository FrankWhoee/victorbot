import discord
from util.fuzzy import search


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

    fuzzychannel = command["args"][0]
    fuzzyname = command["args"][1]

    channels = {c.name: c for c in message.guild.voice_channels}
    channel = search(fuzzychannel, list(channels.keys()))
    channel = channels[channel]

    names = {m.name: m for m in message.guild.members}
    name = search(fuzzyname, list(names.keys()))
    target_user = names[name]

    if target_user.voice is None:
        if "grants" in data["guilds"][str(message.guild.id)]:
            data["guilds"][str(message.guild.id)]["grants"][str(target_user.id)] = channel.id
        else:
            data["guilds"][str(message.guild.id)]["grants"] = {str(target_user.id): channel.id}
        embed = discord.Embed(title="Grant",
                              description=f"{target_user.mention} has been granted access to {channel.mention}.",
                              color=0x00ff00)
        await message.channel.send(embed=embed)
        return True
    else:
        await target_user.move_to(channel)
        embed = discord.Embed(title="Grant", description=f"{target_user.mention} has been moved to {channel.mention}.",
                              color=0x00ff00)
        await message.channel.send(embed=embed)
        return False


help = {
    "name": "grant",
    "description": "Moves <username> to <channel>. If <username> is not in a voice channel yet, they will be moved as "
                   "soon as then join.",
    "usage": ["grant <channel> <username>", "grant list", "grant clear"]
}
