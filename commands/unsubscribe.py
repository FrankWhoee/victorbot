import discord

async def main(message: discord.Message, client: discord.Client, data: dict, command: dict) -> bool:
    del data["guilds"][str(message.guild.id)]["subscribe_channel"]
    await message.channel.send("Removed channel from subscription.")
    return True


help = {
    "name": "unsubscribe",
    "description": "Unsubscribes this channel from boot update.",
    "usage": ["unsubscribe"]
}
