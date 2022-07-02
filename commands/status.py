import discord
import git
from datetime import datetime
from datetime import timedelta

# create a discord embed with status information
def status_embed(client, data: dict) -> discord.Embed:
    repo = git.Repo(search_parent_directories=True)
    sha = repo.head.commit.hexsha
    short_sha = repo.git.rev_parse(sha, short=8)
    embed = discord.Embed(title=client.user.name + " is online.", color=0x00ff00)
    # convert the boot time to a datetime object
    embed.add_field(name="Boot Time", value=datetime.fromtimestamp(data["boot_time"]).strftime("%Y-%m-%d %H:%M:%S"), inline=False)
    embed.add_field(name="Ping", value=str(round(client.latency * 1000)) + "ms")
    # add uptime to the embed
    uptime = datetime.now().timestamp() - data["boot_time"]
    embed.add_field(name="Uptime", value=str(timedelta(seconds=uptime)).split(".")[0])
    embed.add_field(name="Commit", value=repo.head.commit.message, inline=False)
    embed.add_field(name="Hash", value=short_sha)
    embed.add_field(name="Author", value=repo.head.commit.author.name)
    embed.add_field(name="Date", value=repo.head.commit.authored_datetime.strftime("%Y-%m-%d %H:%M:%S"))
    embed.set_footer(text="Data collected since boot. No past data is retained for status messages.")
    embed.set_author(name=client.user.name)
    embed.set_thumbnail(url=client.user.avatar.url)
    return embed


async def main(message: discord.Message, client: discord.Client, data: dict, command: dict) -> bool:
    # send the embed to the channel
    await message.channel.send(embed=status_embed(client, data))
    return False

help = {
    "name": "status",
    "description": "Get status information about the bot.",
    "usage": ["status"]
}