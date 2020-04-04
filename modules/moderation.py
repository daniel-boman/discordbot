import discord
from discord.ext import commands
from loguru import logger

from modules import is_bot_admin


async def delete_messages(channel, u: discord.member.Member, after=None):
    def check(m):
        return m.author.id == u.id

    #    deleted = await channel.history(limit=100, check=check, after=after).flatten()

    logger.debug(f"{channel.id} {u.display_name} {after}")

    if after is not None:
        deleted = await channel.purge(limit=100, after=after, check=check, bulk=True)
    else:
        deleted = await channel.purge(limit=100, check=check, bulk=True)

    if len(deleted) > 0:
        last: discord.Message = deleted[-1]

        logger.debug(f"{len(deleted)} messages found, last: {last.id} {last.created_at}")
        await delete_messages(channel, u, after=last)


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, name='janitor', alias=['clear', 'clean', 'purge'],
                      help="will delete EVERY message made by user(s) in the specified channel")
    @commands.check_any(is_bot_admin(), commands.has_permissions(manage_messages=True))
    @commands.guild_only()
    async def purge(self, ctx: discord.ext.commands.Context, channel: discord.ext.commands.TextChannelConverter,
                    *user: discord.member.Member):
        for u in user:
            await delete_messages(channel, u)
