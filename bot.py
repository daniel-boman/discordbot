import discord
import logging
from discord.ext import commands


def new_bot() -> discord.ext.commands.bot:
    bot = commands.Bot(command_prefix="!", description="A discord bot")

    @bot.event
    async def on_ready():
        logging.debug(f"signing in as [{bot.user.id}] [{bot.user.name}]")

    return bot
