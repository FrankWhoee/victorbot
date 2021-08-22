import math
import random
import subprocess
import time
from datetime import datetime, date
from threading import Timer
import discord
from discord.ext import tasks
import json
import os
from os import walk
import git
from git import Repo
import requests
from pokemon_names import NAMES, KEYWORDS
from discord import User
import sentiment
from secrets import secrets
from discord.ext import tasks, commands

# TODO: Add free sentiment analysis
# Note: Turns out free sentiment analysis is bad. No-go. Sentiment analysis is dead.

# Discord mandated command to access member data.
intents = discord.Intents.all()

pokemon_hint_puzzle = []

emotes = []
grants = []

# important Discord objects
vip_vc = 685271778636988425
vip_tc = 761059144253177866
vip_bot = 763814808100667402
ns_vc = 821137880172462121
default_guild = None  # Set on_ready

# status stuff
start_time = datetime.today()
messages_heard = 0
commands_used = 0

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
# Toxic meter

sounds = []
for (dirpath, dirnames, filenames) in walk("sounds"):
    sounds.extend(filenames)
    break

# GIF Stuff

gifs_left = 2

gifs = {}
for (dirpath, dirnames, filenames) in walk("gifs"):
    for name in dirnames:
        for (dp, dn, f) in walk("gifs/" + name):
            dp = dp.replace("gifs/", "")
            gifs[dp] = []
            for files in f:
                gifs[dp].append("./gifs/" + name + "/" + files)
            break
for key in gifs.keys():
    gifs[key].sort()

ris_quota = 3


def set_ris_quota():
    global ris_quota
    try:
        risdata = requests.get(
            "https://serpapi.com/account?api_key=f4ad401292cbfe0f77814f18745482fa77e637f7a97c27ace729abce45e897f5").json()
        reqleft = risdata["plan_searches_left"]
        today = date.today()
        next_month_start = today.replace(month=today.month + 1, day=1)
        ris_quota = math.floor(reqleft / ((next_month_start - today).total_seconds() / 60 / 60 / 24))
        print("Set ris_quota to " + str(ris_quota))
    except:
        ris_quota = 3
        print("Could not set ris_quota. Setting to default (ris_quota = 3)")


set_ris_quota()
# Glorious stuff
quotes = open("cm.txt", "r")
quotes = quotes.read().split("\n\n")

# Shakespeare interlude
# shakespeare = open("poems/shake2.txt", "r")
# shakespeare = shakespeare.read().split("\n")
# shake_i = 0
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



def reset_gif_limit():
    global gifs_left
    global t
    gifs_left = 2
    t = Timer(24 * 60 * 60, reset_gif_limit)
    t.start()


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
            score += 5
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


def random_sound():
    f = []
    for (dirpath, dirnames, filenames) in walk("sounds"):
        f.extend(filenames)
        break
    return random.choice(f)


async def grant(member, target):
    if member.voice is None:
        grants.append({"member": member, "target": target})
    else:
        await member.move_to(client.get_channel(target), reason="move grant used")

# @tasks.loop(seconds=10.0)
# async def slow_count():
#     random_shake = random.choice(shakespeare)
#     print(random_shake)
#     incog = client.get_channel(vip_bot)
#     if incog is not None:
#         await incog.send(random_shake)

@client.event
async def on_message_edit(before, after):
    await on_message(after)


@client.event
async def on_reaction_add(reaction, user):
    if user.id != client.user.id:
        for e in emotes:
            if e["id"] == reaction.message.id:
                response = e["response"]
                command = e["command"]
                if command == "request":
                    author = e["author"]
                    target = e["target"]
                    if reaction.emoji == "✅":
                        if type(author) is User:
                            author = default_guild.get_member(author.id)
                        print(author)
                        if author.voice is not None:
                            await author.move_to(target, reason="move request approved by vip")
                            await author.send("Your request was to join " + e["target"].name + " was approved!")
                        else:
                            await grant(author, target.id)
                            await author.send("Your request was to join " + e[
                                "target"].name + " was approved! You will be moved to " + e[
                                                  "target"].name + " as soon as you join a channel.")

                    elif reaction.emoji == "❌":
                        await author.send("Your request was to join " + e["target"].name + " was denied.")
                emotes.remove(e)
                break


@client.event
async def on_voice_state_update(member, before, after):
    # grants
    if after.channel is not None:
        for gr in grants:
            if gr["member"].id == member.id:
                await member.move_to(client.get_channel(gr["target"]), reason="move grant used")
                grants.remove(gr)


def greater_than(message, role_id):
    return message.author.roles[len(message.author.roles) - 1] >= message.guild.get_role(role_id)


def greater_than_vip(message):
    return greater_than(message, 756005374955487312)


def expire_request(req):
    emotes.remove(req)


@client.event
async def on_message(message):
    global messages_heard
    global commands_used
    messages_heard += 1
    global gifs_left
    global vc
    global volume
    global ris_quota
    global emotes
    global grants
    global g
    param = None
    # Filter out non-command messages
    if message.content.startswith("The pokémon is "):
        await piece(message)
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
        if message.content in gifs.keys():
            if "bot" in message.channel.name or gifs_left > 0:
                if "bot" not in message.channel.name:
                    gifs_left -= 1
                gif_length = len(gifs[message.content])
                for i in range(0, gif_length):
                    if i % math.ceil(gif_length / 10) == 0:
                        time.sleep(0.5)
                        await message.channel.send(file=discord.File(gifs[message.content][i]))
        s = sentiment.get_sentiment(message)
        delta_toxicity(message.author.id, -1 * s.score * s.magnitude)
        save_db()
        return
    commands_used += 1
    if message.author == client.user:
        return
    if prefix in message.content and len(message.content.split(" ")) < 2:
        command = message.content
    elif prefix in message.content:
        command = message.content.split(" ")[0]
        param = message.content.split(" ")[1:]
    command = command[1:]
    if command == "join":
        if not param:
            await join(message)
        else:
            if client.voice_clients:
                await current_vc(message.guild).disconnect()
            vc = await message.guild.get_channel(int(param[0])).connect()
    elif command == "leave":
        await current_vc(message.guild).disconnect()
    elif command == "play":
        if not client.voice_clients:
            vc = await message.author.voice.channel.connect()
        elif message.author.voice is not None and current_vc(message.guild).channel != message.author.voice.channel:
            await current_vc(message.guild).disconnect()
            vc = await message.author.voice.channel.connect()
        vc.stop()
        if len(param) == 1 and param[0] == "random":
            filename = random_sound()
        else:
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
    elif command == "status":
        embed = await create_status_embed()
        await message.channel.send(embed=embed)
    elif command == "focus":
        await join(message)
        if not param and message.author.id in [194857448673247235, 385297155503685632]:
            for vch in message.guild.voice_channels:
                if not vch.members and not vch.id == 758559024962207795:
                    await message.guild.get_member(194857448673247235).move_to(vch)
                    await message.guild.get_member(385297155503685632).move_to(vch)
                    break
        elif param[0] == "all":
            if (len(param) > 1 and param[1] == "vip") and greater_than_vip(message):
                vch = message.guild.get_channel(vip_vc)
                for m in current_vc(message.guild).channel.members:
                    await m.move_to(vch)
            else:
                for vch in message.guild.voice_channels:
                    if not vch.members and not vch.id == 758559024962207795:
                        for m in current_vc(message.guild).channel.members:
                            await m.move_to(vch)
                        break
        elif param[0] == "game":
            if (len(param) > 1 and param[1] == "vip") and greater_than_vip(message):
                vch = message.guild.get_channel(vip_vc)
                for m in current_vc(message.guild).channel.members:
                    if m.activity != None and m.activity.name == message.author.activity.name:
                        await m.move_to(vch)
            else:
                for vch in message.guild.voice_channels:
                    if not vch.members and not vch.id == 758559024962207795:
                        for m in current_vc(message.guild).channel.members:
                            if m.activity != None and m.activity.name == message.author.activity.name:
                                await m.move_to(vch)
                        break
        elif (greater_than_vip(message) and message.author in message.mentions) or (
                greater_than(message, 685269061512331288)):
            for vch in message.guild.voice_channels:
                if not vch.members and not vch.id == 758559024962207795:
                    for m in message.mentions:
                        await m.move_to(vch)
                    break
    elif command == "merge":
        if message.author.roles[len(message.author.roles) - 1] >= message.guild.get_role(756005374955487312):
            # merge all
            if param[0] == "all":
                await join(message)
                # Collect all members in voice channel
                members = []
                for vch in message.guild.voice_channels:
                    members.extend(vch.members)

                # merge all vip
                if (len(param) > 1 and param[1] == "vip") and greater_than_vip(message):
                    target_vch = message.guild.get_channel(vip_vc)
                else:
                    target_vch = message.author.voice.channel
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
    elif command == "peter" or command == "pyotr":
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
                user = (await client.fetch_user(id))
                embed.add_field(name=user.name + "#" + user.discriminator,
                                value=(-1 if sc < 0 else 1) * round(20 * math.log10(abs(sc)), 2),
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
                user = (await client.fetch_user(id))
                embed.add_field(name=user.name + "#" + user.discriminator, value=round(database["toxicity"][id], 2),
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
    elif command == "ngrok" or command == "ssh":
        response_text = """
                        {0.author.mention}\nPublic URL: {1}
                        """.format(message, createNgrok())
        await message.channel.send(response_text)
    elif command == "gifs":
        await message.channel.send("You have " + str(gifs_left) + " fordnide dances left.")
    elif command == "stock":
        if not param:
            await message.channel.send(
                "You must input a ticker symbol. Example: `stock FIT`. To specify a date, do `stock FIT 2021-04-21`")
            return
        param[0] = param[0].upper()
        if param[0] == "REGIONS":
            embed = discord.Embed(title="Regions", color=0xffffff)
            embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
            embed.add_field(name="London Stock Exchange", value="TICKER.LON", inline=False)
            embed.add_field(name="Toronto Stock Exchange", value="TICKER.TRT", inline=False)
            embed.add_field(name="Toronto Venture Exchange", value="TICKER.TRV", inline=False)
            embed.add_field(name="XETRA (Germany)", value="TICKER.DEX", inline=False)
            embed.add_field(name="BSE (India)", value="TICKER.BSE", inline=False)
            embed.add_field(name="Shanghai Stock Exchange", value="TICKER.SHH", inline=False)
            embed.add_field(name="Shenzhen Stock Exchange", value="TICKER.SHZ", inline=False)
            await message.channel.send(embed=embed)
        elif param[0] == "SPN":
            datekey = datetime.today().strftime('%Y-%m-%d')
            voicemembers = []
            for vch in message.guild.voice_channels:
                voicemembers.extend(vch.members)
            members = await message.guild.fetch_members(limit=None).flatten()
            date = {
                "4. close": len(voicemembers) * 10,
                "5. volume": len(members) * 10
            }
            embed = discord.Embed(title=param[0], description=datekey, color=0x04ff00)
            file = discord.File("images/spn.png", filename="image.png")
            embed.set_thumbnail(url="attachment://image.png")
            embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
            embed.add_field(name="Close", value=date["4. close"], inline=True)
            embed.add_field(name="Volume", value=date["5. volume"], inline=True)
            embed.set_footer(text="Time Series (Daily)")
            await message.channel.send(embed=embed, file=file)
        else:
            data = requests.get(
                "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + param[0] + "&apikey=" +
                secrets["alphav"]).json()
            try:
                if len(param) < 2:
                    datekey = list(data["Time Series (Daily)"].keys())[0]
                else:
                    datekey = param[1]
                date = data["Time Series (Daily)"][datekey]
            except:
                await message.channel.send("Ticker not found!")
                return
            embed = discord.Embed(title=param[0], description=datekey, color=0x04ff00)
            embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
            embed.add_field(name="Open", value=date["1. open"], inline=True)
            embed.add_field(name="High", value=date["2. high"], inline=True)
            embed.add_field(name="Low", value=date["3. low"], inline=True)
            embed.add_field(name="Close", value=date["4. close"], inline=True)
            embed.add_field(name="Volume", value=date["5. volume"], inline=True)
            embed.set_footer(text="Time Series (Daily)")
            await message.channel.send(embed=embed)
    elif command == "pokeid":
        # if message.reference is None and param is None:
        #     messages = await message.channel.history(limit=2).flatten()
        #     image = messages[1].embeds[0].image.url
        # elif param is None:
        #     image = (await message.channel.fetch_message(message.reference.message_id)).embeds[0].image.url
        # elif message.reference is None and param:
        #     image = (await message.channel.fetch_message(param[0])).embeds[0].image.url
        # status = await message.channel.send("Processing...")
        # data = {}
        # rangemax = 898
        # progresslevel = 0
        # for i in range(1, rangemax):
        #     try:
        #         compare = requests.get("https://pokeapi.co/api/v2/pokemon/" + str(i)).json()
        #     except:
        #         continue
        #     name = compare["name"]
        #     compare = compare["sprites"]["front_default"]
        #     r = requests.post(
        #         "https://api.deepai.org/api/image-similarity",
        #         data={
        #             'image1': compare,
        #             'image2': image,
        #         },
        #         headers={'api-key': 'ae719ef7-058a-47e2-b36d-2161f8006e28'}
        #     )
        #     distance = r.json()["output"]["distance"]
        #     data[name] = distance
        #     print(str(i) + ": " + name + "[" + str(distance) + "]")
        #     progress = (i / rangemax)
        #     if progress > 0.5 and progresslevel == 0:
        #         await message.channel.send("Search is 50% complete.")
        #         progresslevel = 1
        #     elif progress > 0.75 and progresslevel == 1:
        #         await message.channel.send("Search is 75% complete.")
        #         progresslevel = 2
        #     elif progress > 0.9 and progresslevel == 2:
        #         await message.channel.send("Search is 90% complete.")
        #         progresslevel = 3
        # data = dict(sorted(data.items(), key=lambda item: item[1]))
        # keys = list(data.keys())
        # output = ""
        # for i in range(10):
        #     output += keys[i] + ": " + str(data[keys[i]]) + "\n"
        # await message.channel.send("Top 10 guesses: \n" + output)
        embed = discord.Embed(title="Method deprecated.", color=0xff0000)
        await message.channel.send(embed=embed)
    elif command == "ris":
        if param:
            if param[0] == "quota":
                await message.channel.send("You have " + str(ris_quota) + " reverse image searches left for today.")
            elif param[0] == "month":
                risdata = requests.get(
                    "https://serpapi.com/account?api_key=f4ad401292cbfe0f77814f18745482fa77e637f7a97c27ace729abce45e897f5").json()
                reqleft = risdata["plan_searches_left"]
                await message.channel.send("You have " + str(reqleft) + " reverse image searches left for this month.")
        else:
            response = await ris(message, param)
            output = "Image Results: \n"
            for data, i in zip(response["image_results"], range(1, len(response["image_results"]) + 1)):
                output += "`" + str(i) + ":` " + data["title"] + " [<" + data["link"] + ">] \n"
            await message.channel.send(output)
    elif command == "rps":
        if param:
            if param[0] == "quota":
                await message.channel.send("You have " + str(ris_quota) + " reverse image searches left for today.")
            elif param[0] == "month":
                risdata = requests.get(
                    "https://serpapi.com/account?api_key=f4ad401292cbfe0f77814f18745482fa77e637f7a97c27ace729abce45e897f5").json()
                reqleft = risdata["plan_searches_left"]
                await message.channel.send("You have " + str(reqleft) + " reverse image searches left for this month.")
        else:
            download_image(await extract_image(message, param), "pokeid.jpg")
            response = requests.post(
                'https://sdk.photoroom.com/v1/segment',
                headers={'x-api-key': 'ac8b31c8dc009b60ea14436088841c54c00bf155'},
                files={'image_file': open("pokeid.jpg", 'rb')},
            )

            response.raise_for_status()

            with open('pokeid.png', 'wb') as f:
                f.write(response.content)

            headers = {
                'Authorization': 'Client-ID 684b5695b24c688',
            }

            response = requests.post('https://api.imgur.com/3/image', headers=headers,
                                     files={'image': open("pokeid.png", 'rb')}).json()
            imgururl = response["data"]["link"]
            response = await ris(message, param, url=imgururl)
            embed1 = discord.Embed(title="Pokemon Guesses", color=0xffbb00)
            used = []
            for data, i in zip(response["image_results"], range(1, len(response["image_results"]) + 1)):
                used = await pokecheck(data, embed1, i, used)

            embed2 = discord.Embed(title="Relevant Results", color=0xd400ff)
            for data, i in zip(response["image_results"], range(1, len(response["image_results"]) + 1)):
                if data["link"] in used:
                    continue
                await kwcheck(data, embed2, i)

            await message.channel.send(embed=embed2)
            await message.channel.send(embed=embed1)
    elif command == "echo":
        await message.channel.send(" ".join(param))
    elif command == "request" or command == "drag":
        if message.channel.type == discord.ChannelType.private:
            for e in emotes:
                if e["author"].id == message.author.id:
                    await message.channel.send(
                        "You already have a request pending! Requests expire 30min after issuing.")
                    return
            target = -1
            if "vip" in param:
                target = vip_vc
            else:
                name = " ".join(param)

                for channel in default_guild.voice_channels:
                    if channel.name.lower() == name.lower():
                        target = channel.id
                        break
            target_channel = client.get_channel(target)
            await message.channel.send("Request to join " + target_channel.name + " sent!")
            vip_tc_channel = client.get_channel(vip_tc)
            response = await vip_tc_channel.send(
                message.author.mention + " has requested to join " + target_channel.name + ". Click ✅ to approve and ❌ to reject.")
            await response.add_reaction("✅")
            await response.add_reaction("❌")
            print(message.author.dm_channel)
            req = {"author": message.author, "response": response, "id": response.id, "command": "request",
                   "target": target_channel, "time": time.time()}
            emotes.append(req)
            Timer(1800, expire_request, args=[req]).start()
        else:
            message.author.send("You can only use `request in a DM!")
    elif command == "grant" and (
            message.channel.id in [vip_tc, vip_bot] or message.channel.type == discord.ChannelType.private):
        if "vip" in param:
            target = vip_vc
        elif "nutstation" in param:
            target = ns_vc
        elif "clear" in param:
            grants = []
            await message.channel.send("Grants cleared.")
            return
        elif "list" in param:
            output = "Currently, "
            for k in range(len(grants) - 1):
                g = grants[k]
                output += g["member"].mention + ", "
            if len(grants) > 1:
                output += "and " + grants[len(grants) - 1]["member"].mention + " have grants right now."
            elif len(grants) == 1:
                output += grants[0]["member"].mention + "has a grant right now."
            elif len(grants) == 0:
                output = "Nobody has a grant right now."
            await message.channel.send(output)
            return
        else:
            await message.channel.send("Must specify a target VC.")
            return
        granted = []
        for m in message.mentions:
            cont = False
            for gr in grants:
                if gr["member"].id == m.id:
                    await message.channel.send(m.mention + " already has a grant.")
                    cont = True
            if cont: continue
            await grant(m, target)
            granted.append(m)
        await message.channel.send(
            "Grant" + ("s" if len(granted) != 1 else "") + " given to " + str(len(granted)) + " member" + (
                "s" if len(granted) != 1 else "") + ".")


async def create_status_embed():
    global commands_used
    global gifs_left
    global messages_heard
    global ris_quota
    embed = discord.Embed(title="Status", description="VictorBot is online.", color=0x00d12a)
    embed.set_author(name="VictorBot")
    embed.set_thumbnail(url=client.user.avatar_url)
    time_delta = (datetime.today() - start_time)
    total_seconds = time_delta.total_seconds()
    days = time_delta.days
    hours = math.floor((total_seconds - days * 24 * 60 * 60) / 3600)
    minutes = math.floor((total_seconds - days * 24 * 60 * 60 - hours * 60 * 60) / 60)
    seconds = math.floor((total_seconds - days * 24 * 60 * 60 - hours * 60 * 60 - minutes * 60))
    embed.add_field(name="Boot Time", value=start_time.isoformat(), inline=False)
    embed.add_field(name="Uptime",
                    value=str(time_delta.days) + ":" + str(hours) + ":" + str(minutes) + ":" + str(seconds),
                    inline=True)
    embed.add_field(name="Messages Heard", value=str(messages_heard), inline=True)
    embed.add_field(name="Commands Used", value=str(commands_used), inline=True)
    embed.add_field(name="RIS Left", value=str(ris_quota), inline=True)
    embed.add_field(name="GIFs Left", value=str(gifs_left), inline=True)
    commits = await shell("git rev-list --all --count")
    embed.add_field(name="Commit", value=commits, inline=True)
    embed.set_footer(text="Data collected since boot. No past data is retained.")
    return embed


async def shell(command):
    process = subprocess.Popen(command.split(" "),
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return stdout.decode("utf-8")


async def piece(message):
    global pokemon_hint_puzzle
    target = message.content
    target = target.replace("The pokémon is ", "")
    target = target.replace(".", "")
    target = target.replace("\\", "")
    target = [char for char in target]
    # check if we're still solving the same puzzle
    if len(target) != len(pokemon_hint_puzzle):
        pokemon_hint_puzzle = target
    else:
        for new, old in zip(target, pokemon_hint_puzzle):
            if new != old and new != "_" and old != "_":
                pokemon_hint_puzzle = target
                break
    if target != pokemon_hint_puzzle:
        for i, new, old in zip(range(len(target)), target, pokemon_hint_puzzle):
            if new != "_":
                pokemon_hint_puzzle[i] = new
    else:
        await message.channel.send("New puzzle detected.")
    temp = pokemon_hint_puzzle.copy()
    for i, c in zip(range(len(temp)), temp):
        if c == "_":
            temp[i] = "\\_"
    await message.channel.send("".join(temp))
    guesses = []
    for n in NAMES:
        if len(n) == len(temp):
            is_guess = True
            for i in range(len(n)):
                if n[i].lower() != temp[i].lower() and temp[i] != "\\_":
                    is_guess = False
                    break
            if is_guess: guesses.append(n)

    if len(guesses) > 1:
        output = "Possible name matches: \n"
        for guess in guesses:
            output += guess + "\n"
        await message.channel.send(output)
    else:
        await message.channel.send(guesses[0])
        await message.channel.send("Puzzle solved.")
        return
    solved = True
    for c in temp:
        if c == "\\_":
            solved = False
    if solved:
        await message.channel.send("Puzzle solved.")


async def pokecheck(data, embed, i, used):
    for pokemon in NAMES:
        if pokemon.split("-")[0] in data["title"].lower() or pokemon.split("-")[0] in data[
            "link"].lower() or pokemon in \
                data["title"].lower() or pokemon in data["link"].lower() or pokemon.replace("-", " ") in \
                data["title"].lower() or pokemon.replace("_", " ") in data["link"].lower():
            used.append(data["link"])
            if pokemon.split("-")[0] in data["title"].lower() or pokemon.split("-")[0] in data["link"].lower():
                embed.add_field(name=str(i), value=pokemon.split("-")[0], inline=False)
                return used
            else:
                embed.add_field(name=str(i), value=pokemon, inline=False)
    return used


def download_image(url, output):
    img_data = requests.get(url).content
    with open(output, 'wb') as handler:
        handler.write(img_data)


async def kwcheck(data, embed, i):
    for kw in KEYWORDS:
        if kw in data["title"].lower() or kw in data["link"].lower() or kw.replace("-", " ") in data[
            "title"].lower() or kw.replace("_", " ") in data["link"].lower():
            embed.add_field(name=str(i) + ": " + kw, value="[" + data["title"] + "](" + data["link"] + ")",
                            inline=False)
            return


async def ris(message, param, url=None):
    global ris_quota
    if ris_quota >= 1:
        ris_quota -= 1
        if not url:
            image = await extract_image(message, param)
        else:
            image = url
        params = (
            ('engine', 'google_reverse_image'),
            ('image_url', image),
            ('api_key', 'f4ad401292cbfe0f77814f18745482fa77e637f7a97c27ace729abce45e897f5'),
        )
        response = requests.get('https://serpapi.com/search', params=params).json()
        return response
    else:
        message.channel.send("You've run out of reverse image searches for today.")


async def extract_message(message, param):
    if message.attachments:
        return message
    elif message.reference is None and param is None:
        messages = await message.channel.history(limit=2).flatten()
        return messages[1]
    elif param is None:
        return await message.channel.fetch_message(message.reference.message_id)
    elif message.reference is None and param:
        return await message.channel.fetch_message(param[0])


async def extract_image(message, param):
    target = extract_message(message)
    if target.embeds:
        return target.embeds[0].image.url
    else:
        return target.attachments[0].url


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
    embed.add_field(name="Social Credit", value=(-1 if sc < 0 else 1) * round(20 * math.log10(abs(sc)), 2), inline=True)
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


def createNgrok():
    try:
        response = json.loads(requests.get('http://localhost:4040/api/tunnels').text)
        pub_url = response['tunnels'][0]['public_url']
    except:
        p = subprocess.Popen("exec " + "~/ngrok tcp 22", stdout=subprocess.PIPE, shell=True)
        while (True):
            try:
                response = json.loads(requests.get('http://localhost:4040/api/tunnels').text)
                pub_url = response['tunnels'][0]['public_url']
                break
            except Exception as e:
                print("Attempting ngrok connection again...")
    return pub_url.replace("tcp://", "")


def save_db():
    with open('database.json', 'w') as outfile:
        json.dump(database, outfile)


@client.event
async def on_member_join(member):
    print("New member joined.")


@client.event
async def on_ready():
    global default_guild
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    channel = client.get_channel(vip_bot)
    await channel.send(embed=await create_status_embed())
    print("Sent status message.")
    default_guild = client.get_guild(231243081993682945)


t = Timer(24 * 60 * 60, reset_gif_limit)
t = Timer(24 * 60 * 60, set_ris_quota)
t.start()
# slow_count.start()
client.run(TOKEN)
