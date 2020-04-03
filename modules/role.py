import discord
from discord.ext import commands
from loguru import logger

import local_types
import redis_client


async def remove_roles(ctx):
    g: discord.Guild = ctx.guild

    member: discord.member.Member = g.get_member(ctx.author.id)
    roles = redis_client.get_roles(g.id)

    roles_to_remove = []

    for k, v in roles.items():
        try:
            role = g.get_role(int(k))
        except Exception:
            raise
        if role is None:
            logger.error("role is None")
            logger.debug(f"{type(k)}: {v}")
            return
        roles_to_remove.append(role)

    to_remove = []
    for mr in member.roles:
        for r in roles_to_remove:
            if r.id == mr.id:
                to_remove.append(r)

    if len(to_remove) > 0:
        await member.remove_roles(*to_remove, reason="Role Command")


class Role(commands.Cog):
    bot: discord.ext.commands.Bot

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='role',
                      help="Choose your role. Cannot be changed after it is set.")
    @commands.cooldown(type=commands.BucketType.user, rate=1, per=3)
    async def role(self, ctx: discord.ext.commands.Context, role: discord.ext.commands.RoleConverter):
        g: discord.Guild = ctx.guild

        member: discord.member.Member = g.get_member(ctx.author.id)
        roles = redis_client.get_roles(g.id)

        if roles is None:
            await ctx.send(f"{member.mention()} no roles available.")
            return

        to_add = None
        to_add_name = None
        for k, v in roles.items():
            if int(k) == role.id:
                to_add = int(k)
                to_add_name = str(v)

        try:
            await remove_roles(ctx)
        except Exception:
            await ctx.send(f"{ctx.author.mention} an error occurred")
            raise

        if to_add is None:
            await ctx.send(f"{ctx.author.mention} could not find any role by that name")
            return

        await member.add_roles(local_types.Snowflake(id=to_add))
        await ctx.send(f"{ctx.author.mention} successfully changed role to {to_add_name}")

    # @role.error
    # async def role_error(self, ctx, error):
    #    if isinstance(error, commands.MissingRequiredArgument):
    #        await ctx.send_help(ctx.command.name)
    #    else:
    #        await ctx.send(f"{ctx.author.mention} {error}")
    #        logger.error(f"{error}")

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if not member.guild.id == "559659441654595585":
            return

        channel = member.guild.system_channel

        if channel is not None:
            await channel.send(
                f"{member.mention()} Welcome to the server. Please type one of the following commands to set your "
                f"role!\n{self.bot.command_prefix}role weeb|normie for weeb role"
                f"role\nChoose wisely, or else {self.bot.get_emoji(691125561514262628)}")
