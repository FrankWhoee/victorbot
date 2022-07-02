import discord

async def main(message: discord.Message, client: discord.Client, data: dict, command: dict) -> bool:
    if len(command["args"]) == 1:
        channel = client.get_channel(int(command["args"][0]))
    else:
        channel = message.author.voice.channel
    if channel is not None:
        await channel.connect()
    return False


help = {
    "name": "join",
    "description": "Joins voice channel.",
    "usage": ["join", "join <channelid>"]
}
