import discord
import git

async def main(message: discord.Message, client: discord.Client, data: dict, command: dict) -> bool:
    async with message.channel.typing():
        git.cmd.Git('.').pull()
    repo = git.Repo(search_parent_directories=True)
    sha = repo.head.commit.hexsha
    short_sha = repo.git.rev_parse(sha, short=8)
    embed = discord.Embed(title="Local version updated.", color=0x00ff00)
    embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
    embed.add_field(name="Current Commit", value=repo.head.commit.message, inline=False)
    embed.add_field(name="Hash", value=short_sha)
    embed.add_field(name="Author", value=repo.head.commit.author.name)
    embed.add_field(name="Date", value=repo.head.commit.authored_datetime.strftime("%Y-%m-%d %H:%M:%S"))

    await message.channel.send(embed=embed)
    return False

# commands must include a help dictionary with the following keys: name, description, usage
help = {
    "name": "template",
    "description": "Template command.",
    "usage": ["template"]
}
