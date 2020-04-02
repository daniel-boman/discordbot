import discord
import modules

from discord.ext import commands
from loguru import logger
from modules import role, admin, manager, colors


def new_bot(command_prefix: str, description: str) -> discord.ext.commands.bot:
    bot = commands.Bot(command_prefix=command_prefix, description=description)

    @bot.event
    async def on_ready():
        logger.info(f"Signed in as [{bot.user.id}] [{bot.user.name}]")

        bot.add_cog(role.Role(bot))
        bot.add_cog(admin.Admin(bot))
        # bot.add_cog(manager.Manager(bot))
        bot.add_cog(colors.Colors(bot))

    return bot
