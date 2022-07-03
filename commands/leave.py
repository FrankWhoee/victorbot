import discord

async def main(message: discord.Message, client: discord.Client, data: dict, command: dict) -> bool:
    if message.guild.voice_client is not None:
        await message.guild.voice_client.disconnect()
    else:
        embed = discord.Embed(title="Error", description="I am not in a voice channel.", color=0xFF0000)
        await message.channel.send(embed=embed)
    return False


help = {
    "name": "leave",
    "description": "Leaves voice channel.",
    "usage": ["leave"]
}
