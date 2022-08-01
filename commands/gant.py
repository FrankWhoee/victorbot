import re

import discord

from util.nsfw import predict_nsfw_from_url


async def main(message: discord.Message, client: discord.Client, data: dict, command: dict) -> bool:
    async with message.channel.typing():
        pred = predict_nsfw_from_url(message.attachments[0].url)["eval.jpg"]
        embed = discord.Embed(title="NSFW Prediction", color=0x00ff00)
        embed.add_field(name="Drawings", value=str(round(pred["drawings"] * 100)) + "%", inline=False)
        embed.add_field(name="Hentai", value=str(round(pred["hentai"] * 100)) + "%", inline=False)
        embed.add_field(name="Neutral", value=str(round(pred["neutral"] * 100)) + "%", inline=False)
        embed.add_field(name="Porn", value=str(round(pred["porn"] * 100)) + "%", inline=False)
        embed.add_field(name="Sexy", value=str(round(pred["sexy"] * 100)) + "%", inline=False)
        embed.set_image(url=message.attachments[0].url)
        embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
    await message.channel.send(embed=embed)

    return False


# commands must include a help dictionary with the following keys: name, description, usage
help = {
    "name": "gant",
    "description": f"Gives AI prediction on whether picture is NSFW.",
    "usage": ["gant"]
}
