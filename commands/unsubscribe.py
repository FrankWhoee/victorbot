import discord

async def main(message: discord.Message, client: discord.Client, data: dict, command: dict) -> bool:
    if "subscribe_channel" not in data["guilds"][str(message.guild.id)]:
        embed = discord.Embed(title="Unsubscribe", description="No channel is subscribed in this guild.", color=0xff0000)
        await message.channel.send(embed=embed)
        return False
    del data["guilds"][str(message.guild.id)]["subscribe_channel"]
    embed = discord.Embed(title="Unsubscribe", description="Unsubscribed from this channel.")
    await message.channel.send(embed=embed)
    return True


help = {
    "name": "unsubscribe",
    "description": "Unsubscribes this channel from boot update.",
    "usage": ["unsubscribe"]
}
