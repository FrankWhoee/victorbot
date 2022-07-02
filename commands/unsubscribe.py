import discord

async def main(message: discord.Message, client: discord.Client, data: dict, command: dict) -> bool:
    del data["guilds"][str(message.guild.id)]["subscribe_channel"]
    embed = discord.Embed(title="Unsubscribe", description="Unsubscribed from this channel.")
    await message.channel.send(embed=embed)
    return True


help = {
    "name": "unsubscribe",
    "description": "Unsubscribes this channel from boot update.",
    "usage": ["unsubscribe"]
}
