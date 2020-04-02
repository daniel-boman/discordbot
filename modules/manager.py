import discord

from discord.ext import commands
from loguru import logger
from modules import is_bot_admin, send_pastebin


class Manager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="edit", help="used to edit other modules and/or commands", hidden=True)
    @commands.check(is_bot_admin)
    async def edit(self, ctx, *args):
        raise NotImplementedError()
