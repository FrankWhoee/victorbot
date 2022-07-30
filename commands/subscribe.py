import discord

async def main(message: discord.Message, client: discord.Client, data: dict, command: dict) -> bool:
    if message.guild is not None:
        data["guilds"][str(message.guild.id)]["subscribe_channel"] = message.channel.id
        embed = discord.Embed(title="Subscribe", description="Subscribed to this channel.", color=0x00ff00)
        await message.channel.send(embed=embed)
        return True
    else:
        data["dmsubscribers"].append(message.author.id)
        embed = discord.Embed(title="Subscribe", description="Subscribed to this channel.", color=0x00ff00)
        await message.channel.send(embed=embed)
        return True

help = {
    "name": "subscribe",
    "description": "Sends a status update to this channel every time the bot boots.",
    "usage": ["subscribe"]
}
