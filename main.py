import importlib
import json
import os
import traceback

from dotenv import load_dotenv
import discord
from datetime import datetime

load_dotenv()

intents = discord.Intents.all()

client = discord.Client(intents=intents)

data = {"guilds": {}, "dev": False}


def save_data():
    with open("data.json", "w") as f:
        json.dump(data, f)


# !!! Boot up sequence starts

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

if "prefix" not in data:
    data["prefix"] = "!"
    save_data()


# !!! Boot up sequence ends

@client.event
async def on_ready():
    from commands.status import status_embed
    print(f'We have logged in as {client.user}')
    for gid in list(data["guilds"]):
        # Should we clear guild data if the bot is no longer in the guild? Seems dangerous.
        if int(gid) not in [g.id for g in client.guilds]:
            data["guilds"].pop(gid)
            save_data()
        elif "subscribe_channel" in data["guilds"][gid]:
            channel = client.get_channel(data["guilds"][gid]["subscribe_channel"])
            await channel.send(embed=status_embed(client, data))


@client.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    if before.channel is None and after.channel is not None:
        if str(after.channel.guild.id) in data["guilds"]:
            if str(member.id) in data["guilds"][str(after.channel.guild.id)]["grants"]:
                channel = client.get_channel(data["guilds"][str(after.channel.guild.id)]["grants"][str(member.id)])
                await member.move_to(channel)
                del data["guilds"][str(after.channel.guild.id)]["grants"][str(member.id)]


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith(data["prefix"]):
        precommand = message.content[len(data["prefix"]):].split(" ")
        command = {"command": precommand[0], "args": precommand[1:]}
        if command["command"] == "help":
            commands = [f.split(".")[0] for f in os.listdir("commands") if f.endswith(".py")]
            if len(command["args"]) == 0:
                await message.channel.send("```All Commands:\n" + "\n".join(f'{data["prefix"] + c}' for c in commands) + "```")
            else:
                module = importlib.import_module(f'commands.{command["args"][0]}')
                help = getattr(module, "help")
                embed = discord.Embed(title=help["name"], description=help["description"], color=0x00ff00)
                embed.add_field(name="Usage", value="\n".join([data["prefix"] + u for u in help["usage"]]), inline=False)
                await message.channel.send(embed=embed)
        else:
            if os.path.isfile(f'commands/{command["command"]}.py'):
                module = importlib.import_module(f"commands.{command['command']}")
                func = getattr(module, "main")

                await handle_command(command, func, message)
            elif data["dev"] and os.path.isfile(f'dev/{command["command"]}.py'):
                module = importlib.import_module(f"dev.{command['command']}")
                func = getattr(module, "main")

                await handle_command(command, func, message)
            else:
                await message.channel.send(f"Command {command['command']} not found.")


async def handle_command(command, func, message):
    if str(message.guild.id) not in data["guilds"]:
        data["guilds"][str(message.guild.id)] = {"grants": {}, "volume":1}
    try:
        modifiesData = await func(message, client, data, command)
        if modifiesData:
            save_data()
    except discord.errors.Forbidden as e:
        # create an embed with the error message and send it
        embed = discord.Embed(title="Permissions insufficient", color=0xff0000)
        await message.channel.send(embed=embed)
    except Exception as e:
        traceback.print_exc()
        if "owner" in os.environ:
            embed = discord.Embed(title="An unknown error occurred.",
                                  description="Error has been reported to the owner.", color=0xff0000)
            await message.channel.send(embed=embed)
            # create an embed with the error message and author and time stamp
            embed = discord.Embed(title="Error", description=traceback.format_exc(), color=0xff0000)
            embed.set_author(name=message.author.name, icon_url=message.author.avatar.url)
            embed.add_field(name="Message", value=message.content, inline=False)
            embed.set_footer(text=f"{message.created_at}")
            await client.get_user(int(os.environ["owner"])).send(embed=embed)
        else:
            embed = discord.Embed(title="An unknown error occurred.", color=0xff0000)
            await message.channel.send(embed=embed)


if os.environ.get("dev").lower() == "true":
    client.run(os.environ.get("devkey"))
else:
    client.run(os.environ.get("prodkey"))
