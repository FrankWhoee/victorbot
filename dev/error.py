import discord

async def main(message: discord.Message, client: discord.Client, data: dict, command: dict, sqldb: sqlite3.Cursor) -> bool:
    # commands must return a boolean that indicates whether they modified data
    raise Exception("Error: " + command["command"] + " is not a valid command.")
    # return False

# commands must include a help dictionary with the following keys: name, description, usage
help = {
    "name": "error",
    "description": "Trigger an error.",
    "usage": ["error"]
}
