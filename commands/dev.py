import discord

async def main(message: discord.Message, client: discord.Client, data: dict, command: dict) -> bool:
    if data["dev"]:
        data["dev"] = False
        await message.channel.send("Disabled developer mode.")
    else:
        data["dev"] = True
        await message.channel.send("Enabled developer mode.")
    return True

help = {
    "name": "dev",
    "description": "Toggle developer mode.",
    "usage": ["dev"]
}
