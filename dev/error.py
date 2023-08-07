import discord

from util.Victor import Victor


async def main(message: discord.Message, command: dict, victor: Victor) -> bool:
    # commands must return a boolean that indicates whether they modified data
    raise Exception("Error: " + command["command"] + " is not a valid command.")
    # return False

# commands must include a help dictionary with the following keys: name, description, usage
help = {
    "name": "error",
    "description": "Trigger an error.",
    "usage": ["error"]
}
