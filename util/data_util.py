import discord


def initializeGuildData(guild: discord.Guild, data: dict) -> bool:
    if str(guild.id) not in data["guilds"]:
        data["guilds"][str(guild.id)] = {"grants": {}, "volume": 1, "reactions": {}, "timers":{}}
        return True
    return False

def initializeDMData(user: discord.User, data: dict) -> bool:
    if str(user.id) not in data["dms"]:
        data["dms"][str(user.id)] = {"reactions": {}}
        return True
    return False
