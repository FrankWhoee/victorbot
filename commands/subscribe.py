import discord

async def main(message: discord.Message, client: discord.Client, data: dict, command: dict) -> bool:
    data["guilds"][str(message.guild.id)]["subscribe_channel"] = message.channel.id
    await message.channel.send("Set channel to send status updates to.")
    return True


help = {
    "name": "subscribe",
    "description": "Sends a status update to this channel every time the bot boots.",
    "usage": "subscribe"
}
