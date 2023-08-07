import sqlite3
from util.logger import Logger
import discord


class Victor():
    # client: discord.Client, data: dict, command: dict, sqldb: sqlite3.Cursor, logger: util.logger.Logger
    client: discord.Client = None
    data: dict = None
    sqldb: sqlite3.Cursor = None
    logger: Logger = None

    def __init__(self, client: discord.Client, data: dict, sqldb: sqlite3.Cursor, logger: Logger):
        self.client = client
        self.data = data
        self.sqldb = sqldb
        self.logger = logger
