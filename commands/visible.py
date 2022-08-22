import re
import sqlite3

import discord

import util
from util.errors import CommandError
from util.nsfw import predict_nsfw_from_url
from util.parse_util import extract_channel, extract_guild_channel

MAX_VISIBLE_MESSAGES = 20

url_regex_pattern = r"(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"


async def main(message: discord.Message, client: discord.Client, data: dict, command: dict,
               sqldb: sqlite3.Cursor, logger: util.logger.Logger) -> bool:
    async with message.channel.typing():
        if message.guild is None:
            if len(command["args"]) < 2 or len(command["args"]) > 2:
                raise CommandError("Invalid number of arguments. See `!help visible`.")

            guild, channel = extract_guild_channel(client, command)
        else:
            if len(command["args"]) < 1 or len(command["args"]) > 1:
                raise CommandError("Invalid number of arguments. See `!help visible`.")
            guild = message.guild
            channel = extract_channel(guild, command)

        stats = {}
        attachments = []
        async for m in channel.history(limit=MAX_VISIBLE_MESSAGES):
            if m.author.id not in stats:
                stats[m.author.id] = {"messages": 0, "attachments": 0, "links": 0}
            stats[m.author.id]["messages"] += 1
            stats[m.author.id]["attachments"] += len(m.attachments)
            stats[m.author.id]["links"] += re.search(url_regex_pattern, m.content) is not None
            for a in m.attachments:
                attachments.append(a.url)

        max_score = 0
        for a_url in attachments:
            pred = predict_nsfw_from_url(a_url)["eval.jpg"]
            max_pred = max(pred["hentai"], pred["porn"], pred["sexy"])
            if max_pred > max_score:
                max_score = max_pred

        embed = discord.Embed(title="Visible Messages", description=channel.mention,
                              color=discord.Color.from_rgb(r=round(max_score * 256), g=round((1 - max_score) * 256),
                                                           b=0))
        embed.set_footer(text=f"Risk Assessment: " + str(max_score * 100)[:5] + "%")
        for author_id in stats:
            author = client.get_user(author_id)
            if author is None:
                author = "Unknown"
            else:
                author = author.name + "#" + author.discriminator
            embed.add_field(name=author,
                            value=f"{stats[author_id]['messages']} messages with {stats[author_id]['attachments']} attachments and {stats[author_id]['links']} links",
                            inline=False)

    await message.channel.send(embed=embed)
    return False


# commands must include a help dictionary with the following keys: name, description, usage
help = {
    "name": "visible",
    "description": f"Gives data on the last {MAX_VISIBLE_MESSAGES} messages in a channel.",
    "usage": ["visible <channel>", "visible <channelid>", "visible <guild> <channel>", "visible <guildid> <channelid>"]
}
