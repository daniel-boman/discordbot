import discord
from discord.ext import commands
from loguru import logger

import local_types
import redis_client
from modules import is_bot_admin


class Manager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(hidden=True)
    @commands.check_any(is_bot_admin(), commands.has_permissions(manage_roles=True))
    @commands.guild_only()
    async def edit(self, ctx: discord.ext.commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command.name)

    @edit.group(name='nsfw', help="add or remove channels where the bot is allowed to post NSFW content")
    async def nsfw(self, ctx):
        pass

    @edit.group(name='roles', help="add or remove roles for use in role command.")
    async def roles(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command.name)

    @roles.command(name='list')
    async def roles_list(self, ctx: discord.ext.commands.Context):
        roles = redis_client.get_roles(ctx.guild.id)

        if roles is None:
            await ctx.send("no roles available")
            return

        for k, v in roles.items():
            await ctx.send(f"{k}: {v}")

    @roles.command(name='add')
    async def roles_add(self, ctx: discord.ext.commands.Context, *role: discord.ext.commands.RoleConverter):
        for r in role:
            redis_client.add_role(ctx.guild.id, local_types.Snowflake(r.id, r.name))
            await ctx.send(f"{ctx.author.mention} added role [id:{r.id} name:{r.name}]")

    @roles.command(name='remove', aliases=["del", "rm"])
    async def roles_remove(self, ctx: discord.ext.commands.Context, *role: discord.ext.commands.RoleConverter):
        for r in role:
            redis_client.remove_role(ctx.guild.id, local_types.Snowflake(r.id, r.name))
            await ctx.send(f"{ctx.author.mention} removed role [id:{r.id} name:{r.name}]")

    @roles_list.error
    async def roles_list_error(self, ctx, error):
        logger.error(f"error in roles_list: {error}")

    @roles_add.error
    async def roles_add_error(self, ctx, error):
        logger.error(f"error in roles_add: {error}")

    @roles_remove.error
    async def roles_remove_error(self, ctx, error):
        logger.error(f"error in roles_remove: {error}")
