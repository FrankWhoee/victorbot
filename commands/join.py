import discord
from util.decorators import guildCommand

@guildCommand
async def main(message: discord.Message, client: discord.Client, data: dict, command: dict) -> bool:
    if len(command["args"]) == 1:
        channel = client.get_channel(int(command["args"][0]))
    else:
        channel = message.author.voice.channel
    if channel is not None:
        # client leaves voice channel if in one
        if client.voice_clients.get(message.guild.id) is not None:
            await client.voice_clients.get(message.guild.id).disconnect()
        await channel.connect()
    return False


help = {
    "name": "join",
    "description": "Joins voice channel.",
    "usage": ["join", "join <channelid>"]
}
