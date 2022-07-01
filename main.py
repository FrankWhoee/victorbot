import importlib
import json
import os

from dotenv import load_dotenv
import discord
from datetime import datetime

load_dotenv()

intents = discord.Intents.all()

client = discord.Client(intents=intents)

data = {}
def save_data():
    with open("data.json", "w") as f:
        json.dump(data, f)

if os.path.isfile("data.json"):
    with open("data.json", "r") as f:
        data = json.load(f)
else:
    save_data()

# save boot time to data and save last boot time to data
if "boot_time" not in data:
    data["boot_time"] = datetime.now().timestamp()
    save_data()
else:
    data["last_boot_time"] = data["boot_time"]
    data["boot_time"] = datetime.now().timestamp()
    save_data()


prefix = data["prefix"] if "prefix" in data else "!"


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith(prefix):
        precommand = message.content[len(prefix):].split(" ")
        command = {"command": precommand[0], "args": precommand[1:]}
        if command["command"] == "help":
            commands = [f.split(".")[0] for f in os.listdir("commands") if f.endswith(".py")]
            if len(command["args"]) == 0:
                await message.channel.send("```All Commands:\n" + "\n".join(f"{c}" for c in commands) + "```")
            else:
                module = importlib.import_module(f'commands.{command["args"][0]}')
                help = getattr(module, "help")
                # create an embed with the help information
                embed = discord.Embed(title=help["name"], description=help["description"], color=0x00ff00)
                embed.add_field(name="Usage", value=help["usage"], inline=False)
                await message.channel.send(embed=embed)
        else:
            # check if there is a file in commands with the command name
            if os.path.isfile(f'commands/{command["command"]}.py'):
                # import the file and get the function
                module = importlib.import_module(f"commands.{command['command']}")
                func = getattr(module, "main")
                # call the function with the message and client
                await func(message, client, data, command)
            else:
                await message.channel.send(f"Command {command['command']} not found.")


client.run(os.environ.get("discord"))
