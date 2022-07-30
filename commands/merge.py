import discord
from util.decorators import guildCommand

@guildCommand
async def main(message: discord.Message, client: discord.Client, data: dict, command: dict) -> bool:
    if len(message.mentions) == 1:
        from_user = message.author
        target_user = message.mentions[0]
    else:
        from_user = message.mentions[0]
        target_user = message.mentions[1]

    if (target_user.voice is None and from_user.voice is None):
        embed = discord.Embed(title="Error", description="Both users are not in a voice channel.", color=0xFF0000)
    elif from_user.voice is None:
        embed = discord.Embed(title="Error", description=f"{from_user.mention} is not in a voice channel.",
                              color=0xFF0000)
    elif target_user.voice is None:
        embed = discord.Embed(title="Error", description=f"{target_user.mention} is not in a voice channel.",
                              color=0xFF0000)
    elif target_user.voice.channel is from_user.voice.channel:
        embed = discord.Embed(title="Error", description="Both users are in the same voice channel.", color=0xFF0000)
    else:
        from_channel = from_user.voice.channel
        target_channel = target_user.voice.channel
        if from_channel is not None and target_channel is not None:
            for member in from_channel.members:
                await member.move_to(target_channel)
        return False
    await message.channel.send(embed=embed)
    return False

help = {
    "name": "merge",
    "description": "Merges everyone from the same voice channel as @user1 to the same voice channel as @user2.",
    "usage": ["merge <@user1> <@user2>"]
}
