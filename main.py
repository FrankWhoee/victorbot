import math
import random
import discord
import json
import os
from os import walk
import git
import sentiment

# Discord mandated command to access member data.
intents = discord.Intents.default()
intents.members = True

# Extract secrets from local file.
if os.path.exists("secrets.json"):
    with open("secrets.json") as f:
        secrets = json.load(f)
else:
    secrets = {}
    secrets["token"] = os.environ.get("token")

# Instantiate discord.py Client
TOKEN = secrets["token"]
client = discord.Client(intents=intents)

# Set constants and global variables
prefix = "`"
vc = None
volume = 0.25
admin = [194857448673247235, 385297155503685632]

# Set up git for pull command
project_dir = os.path.dirname(os.path.abspath(__file__))
os.environ['GIT_ASKPASS'] = os.path.join(project_dir, 'askpass.py')
os.environ['GIT_USERNAME'] = secrets["git-username"]
os.environ['GIT_PASSWORD'] = secrets["pat"]
g = git.cmd.Git('.')
g.pull()

# Toxic meter

sounds = []
for (dirpath, dirnames, filenames) in walk("sounds"):
    sounds.extend(filenames)
    break

# Glorious stuff
quotes = open("cm.txt", "r")
quotes = quotes.read().split("\n\n")

farm_stop = False

ranks = {-1000: "Bourgeoisie", -500: "Terrorist", -200: "Enemy Spy", -100: "Enemy of the State", -10: "Radicalist",
         0: "Foreigner", 10: "Comrade", 100: "Follower", 1000: "Ally", 10000: "Leader",
         100000: "Mao Zedong's Right Hand"}

glorious_keywords = ["china", "ccp", "chinese", "beijing", "changchun", "changde", "changsha", "changshu", "chengde",
                     "chengdu", "chongqing", "dali", "dalian", "datong", "dunhuang", "fuzhou", "guangzhou", "guilin",
                     "guiyang", "haikou", "hangzhou", "harbin", "hefei", "hohhot", "jinan", "jiuquan", "kaifeng",
                     "kashi", "kunming", "laiwu", "lanzhou", "lhasa", "liaoyang", "luoyang", "macau", "nanchang",
                     "naijing", "nanning", "pingyao", "qingdao", "qinhuangdao", "sanya", "shanghai", "shenyang",
                     "shenzhen", "shijiazhuang", "suzhou", "taiyuan", "tianjin", "urumqi", "wenzhou", "wuhan", "wuxi",
                     "xiamen", "xi'an", "xining", "yanan", "yangzhou", "zhengzhou"]

unglory_keywords = ["hong kong", "america", "uyghur", "massacre", "protest", "tibet", "taiwan", "falun gong",
                    "nanking", "winne", "pooh", "tank", "man", "rape", "leap", "cultural"]

# Load local database. Create new database if it doesn't exist.

database = {}

if os.path.isfile("database.json"):
    with open('database.json') as json_file:
        database = json.load(json_file)


def current_vc(guild):
    for vc in client.voice_clients:
        if vc.guild == guild:
            return vc


def get_score(query, compare):
    score = 0
    for letter in compare:
        if letter in query:
            score += 0.5
    if min(len(compare), len(query)) == len(query):
        for i in range(0, len(query)):
            if query[i] == compare[i]:
                score += 1
    else:
        for i in range(0, len(compare)):
            if query[i] == compare[i]:
                score += 1
    qsplit = query.split(" ")
    csplit = compare.split(" ")
    for s in qsplit:
        if s in csplit:
            score += 3
    return score


def search_sound(query):
    scores = {}
    f = []
    for (dirpath, dirnames, filenames) in walk("sounds"):
        f.extend(filenames)
        break
    for file in f:
        scores[file] = get_score(query, file.replace(".mp3", ""))
    max = list(scores.keys())[0]
    for s in scores:
        if scores[s] > scores[max]:
            max = s
    return max


@client.event
async def on_message(message):
    global vc
    global volume
    param = None
    # Filter out non-command messages
    message_split = message.content.split(" ")
    has_glory = any(item in glorious_keywords for item in message_split)
    has_unglory = any(item in unglory_keywords for item in message_split)
    if has_unglory and not message.content.startswith(prefix):
        s = sentiment.get_sentiment(message)
        if s.score > 0:
            delta_social_credit(message.author.id, s.score * s.magnitude * -100)
        else:
            delta_social_credit(message.author.id, s.score * s.magnitude * -1)
        save_db()
        return
    elif has_glory and not message.content.startswith(prefix):
        s = sentiment.get_sentiment(message)
        if s.score > 0:
            delta_social_credit(message.author.id, s.score * s.magnitude)
        else:
            delta_social_credit(message.author.id, s.score * s.magnitude * 100)
        save_db()
        return
    elif not message.content.startswith(prefix):
        s = sentiment.get_sentiment(message)
        delta_toxicity(message.author.id, -1 * s.score * s.magnitude)
        save_db()
        return

    if message.author == client.user:
        return
    if prefix in message.content and len(message.content.split(" ")) < 2:
        command = message.content
    elif prefix in message.content:
        command = message.content.split(" ")[0]
        param = message.content.split(" ")[1:]
    command = command[1:]
    if command == "join":
        await join(message)
    elif command == "leave":
        await current_vc(message.guild).disconnect()
    elif command == "play":
        if not client.voice_clients:
            vc = await message.author.voice.channel.connect()
        elif message.author.voice is not None and current_vc(message.guild).channel != message.author.voice.channel:
            await current_vc(message.guild).disconnect()
            vc = await message.author.voice.channel.connect()
        vc.stop()
        filename = search_sound(" ".join(param))
        if filename == "china national anthem.mp3":
            update_social_credit()
        audio_source = discord.FFmpegPCMAudio('sounds/' + filename)
        audio_source = discord.PCMVolumeTransformer(audio_source, volume=volume)
        vc.play(audio_source, after=None)
    elif command == 'stop':
        vc.stop()
    elif command == "volume":
        if not param:
            await message.channel.send("Volume is " + str(volume * 100) + "% right now.")
        else:
            volume = float(param[0]) / 100
            await message.channel.send("Volume is now " + str(volume * 100) + "%")
    elif command == "focus":
        await join(message)
        if not param and message.author.id in [194857448673247235, 385297155503685632]:
            for vch in message.guild.voice_channels:
                if not vch.members and not vch.id == 758559024962207795:
                    await message.guild.get_member(194857448673247235).move_to(vch)
                    await message.guild.get_member(385297155503685632).move_to(vch)
                    break
        elif param[0] == "all":
            if (len(param) > 1 and param[1] == "vip") and message.author.roles[
                len(message.author.roles) - 1] >= message.guild.get_role(756005374955487312):
                vch = message.guild.get_channel(685271778636988425)
                for m in current_vc(message.guild).channel.members:
                    await m.move_to(vch)
            else:
                for vch in message.guild.voice_channels:
                    if not vch.members and not vch.id == 758559024962207795:
                        for m in current_vc(message.guild).channel.members:
                            await m.move_to(vch)
                        break
        elif (message.author.roles[len(message.author.roles) - 1] >= message.guild.get_role(
                756005374955487312) and message.author in message.mentions) or (
                message.author.roles[len(message.author.roles) - 1] >= message.guild.get_role(685269061512331288)):
            for vch in message.guild.voice_channels:
                if not vch.members and not vch.id == 758559024962207795:
                    for m in message.mentions:
                        await m.move_to(vch)
                    break
    elif command == "merge":
        if message.author.roles[len(message.author.roles) - 1] >= message.guild.get_role(756005374955487312):
            if param[0] == "all":
                await join(message)
                # Collect all members in voice channel
                members = []
                for vch in message.guild.voice_channels:
                    members.extend(vch.members)

                if (len(param) > 1 and param[1] == "vip") and message.author.roles[
                    len(message.author.roles) - 1] >= message.guild.get_role(756005374955487312):
                    target_vch = message.guild.get_channel(685271778636988425)
                else:
                    target_vch = message.guild.voice_channels[0]
                for m in members:
                    await m.move_to(target_vch)
            elif len(message.mentions) == 1:
                if message.mentions[0].voice is None:
                    await message.channel.send(message.mentions[0].name + " is not in a voice channel currently.")
                    return
                elif message.author.voice is None:
                    await message.channel.send("You are not in a voice channel currently.")
                    return
                vch = message.mentions[0].voice.channel
                for m in message.author.voice.channel.members:
                    await m.move_to(vch)
            elif len(message.mentions) == 2:
                if message.mentions[1].voice is None:
                    await message.channel.send(message.mentions[1].name + " is not in a voice channel currently.")
                    return
                elif message.mentions[0].voice is None:
                    await message.channel.send(message.mentions[0].name + " is not in a voice channel currently.")
                    return
                vch = message.mentions[1].voice.channel
                for m in message.mentions[0].voice.channel.members:
                    await m.move_to(vch)
        else:
            await message.channel.send("You are not authorized to use this command.")
    elif command == "pull":
        if message.author.id in admin:
            g.pull()
            await message.channel.send("Local version updated.")
        else:
            await message.channel.send("You are not authorized to use this command.")
    elif command == "peter":
        await message.channel.send("Пётр")
    elif command == "farm":
        await join(message)
        if param and param[0] == "stop":
            global farm_stop
            farm_stop = True
            vc.stop()
            print("stop")
        else:
            farm(message)
    elif command == "glory":
        if not param:
            file, embed = construct_glory_embed(message.author)
            await message.channel.send(file=file, embed=embed)
        elif len(message.mentions) > 0:
            file, embed = construct_glory_embed(message.mentions[0])
            await message.channel.send(file=file, embed=embed)
        elif param[0] == "leaderboard" or param[0] == "lb":
            glory = get_glory(avg_glory())
            file = discord.File("images/" + glory.lower() + ".png", filename="image.png")
            embed = discord.Embed(title=glory + " Leaderboard",
                                  description="\"" + quotes[random.randint(0, len(quotes))].replace("\n", " ") + "\"",
                                  color=0xcd0000)
            embed.set_thumbnail(url="attachment://image.png")
            for id in get_glorious_leaderboard():
                sc = database["social_credit"][id]
                embed.add_field(name=(await client.fetch_user(id)).name, value=round(20 * math.log(sc), 2),
                                inline=False)
            await message.channel.send(embed=embed, file=file)
    elif command == "toxic":
        if not param:
            embed = construct_toxic_embed(message.author)
            await message.channel.send(embed=embed)
        elif len(message.mentions) > 0:
            embed = construct_toxic_embed(message.mentions[0])
            await message.channel.send(embed=embed)
        elif param[0] == "leaderboard" or param[0] == "lb":
            embed = discord.Embed(title=sounds[random.randint(0, len(sounds) - 1)] + " Leaderboard",
                                  color=discord.Colour(0).from_rgb(random.randint(0, 255), random.randint(0, 255),
                                                           random.randint(0, 255)))
            for id in get_toxic_leaderboard():
                embed.add_field(name=(await client.fetch_user(id)).name, value=round(database["toxicity"][id], 2),
                                inline=False)
            await message.channel.send(embed=embed)
    elif command == "sen":
        if not param:
            messages = await message.channel.history(limit=2).flatten()
            s = sentiment.get_sentiment(messages[1])
        else:
            s = sentiment.get_sentiment_raw(" ".join(param))
        embed = discord.Embed(title="Sentiment Analysis")
        embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
        embed.add_field(name="Score", value=s.score, inline=True)
        embed.add_field(name="Magnitude", value=s.magnitude, inline=True)
        await message.channel.send(embed=embed)


def get_glorious_leaderboard():
    sorted_leaderboard = sorted(database["social_credit"], key=database["social_credit"].get, reverse=True)
    return sorted_leaderboard


def get_toxic_leaderboard():
    sorted_leaderboard = sorted(database["toxicity"], key=database["toxicity"].get, reverse=True)
    return sorted_leaderboard


def avg_glory():
    sum = 0
    for value in database["social_credit"].values():
        sum += value
    return sum / len(database["social_credit"])


def construct_toxic_embed(author):
    sc = database["toxicity"][str(author.id)] if str(author.id) in database["toxicity"] else 0
    embed = discord.Embed(title=sounds[random.randint(0, len(sounds) - 1)],
                          color=discord.Colour(0).from_rgb(random.randint(0, 255), random.randint(0, 255),
                                                           random.randint(0, 255)))
    embed.set_author(name=author.name, icon_url=author.avatar_url)
    embed.add_field(name="Toxicity", value=round(sc, 2), inline=True)
    place = str(get_toxic_leaderboard().index(str(author.id)) + 1)
    last_digit = place[len(place) - 1]
    if last_digit == "1":
        suffix = "st"
    elif last_digit == "2":
        suffix = "nd"
    elif last_digit == "3":
        suffix = "rd"
    else:
        suffix = "th"
    embed.add_field(name="Position", value=place + suffix, inline=True)
    return embed


def construct_glory_embed(author):
    sc = database["social_credit"][str(author.id)] if str(author.id) in database["social_credit"] else 0
    glory = get_glory(sc)
    file = discord.File("images/" + glory.lower() + ".png", filename="image.png")
    embed = discord.Embed(title=glory,
                          description="\"" + quotes[random.randint(0, len(quotes))].replace("\n", " ") + "\"",
                          color=0xcd0000)
    embed.set_author(name=author.name, icon_url=author.avatar_url)
    embed.set_thumbnail(url="attachment://image.png")
    embed.add_field(name="Social Credit", value=round(20 * math.log(sc), 2), inline=True)
    place = str(get_glorious_leaderboard().index(str(author.id)) + 1)
    last_digit = place[len(place) - 1]
    if last_digit == "1":
        suffix = "st"
    elif last_digit == "2":
        suffix = "nd"
    elif last_digit == "3":
        suffix = "rd"
    else:
        suffix = "th"
    embed.add_field(name="Position", value=place + suffix, inline=True)
    return file, embed


def get_glory(sc):
    if sc > 0:
        for key in list(ranks)[::-1]:
            if sc >= key:
                return ranks[key]
    else:
        for key in ranks.keys():
            if sc <= key:
                return ranks[key]


def farm(error):
    global farm_stop
    if not farm_stop and client.voice_clients:
        vc.stop()
        audio_source = discord.FFmpegPCMAudio('sounds/china national anthem.mp3')
        audio_source = discord.PCMVolumeTransformer(audio_source, volume=volume)
        vc.play(audio_source, after=farm)
        update_social_credit()
    else:
        farm_stop = False


async def join(message):
    global vc
    if client.voice_clients:
        await current_vc(message.guild).disconnect()
    vc = await message.author.voice.channel.connect()


def delta_social_credit(id, delta):
    if not "social_credit" in database.keys():
        database["social_credit"] = {}
    if not str(id) in database["social_credit"]:
        database["social_credit"][str(id)] = delta
    else:
        database["social_credit"][str(id)] += delta


def delta_toxicity(id, delta):
    if not "toxicity" in database.keys():
        database["toxicity"] = {}
    if not str(id) in database["toxicity"]:
        database["toxicity"][str(id)] = delta
    else:
        database["toxicity"][str(id)] += delta


def update_social_credit():
    global vc
    if not "social_credit" in database.keys():
        database["social_credit"] = {}
    for m in vc.channel.members:
        delta_social_credit(m.id, 1)
    save_db()


def save_db():
    with open('database.json', 'w') as outfile:
        json.dump(database, outfile)


@client.event
async def on_member_join(member):
    print("New member joined.")


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(TOKEN)
