import discord

async def main(reaction: discord.Reaction, user: discord.User, client: discord.Client, data: dict, command: dict) -> bool:
    # reactions must return a boolean that indicates whether they modified data
    return False