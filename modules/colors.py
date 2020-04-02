import discord

from discord.ext import commands
from loguru import logger
from modules import is_bot_admin, Snowflake
from threading import Lock


class Colors(commands.Cog):
    bot: discord.ext.commands.Bot

    colorRoles = {}

    mutex = Lock()

    def __init__(self, bot):
        self.bot = bot
        self.reload()

    def reload(self):
        self.mutex.acquire()
        for g in self.bot.guilds:

            try:
                self.colorRoles[g.id].clear()
            except Exception:
                pass  # Ignore error

            d = {}

            for r in g.roles:
                if r.name.lower().startswith("color- "):
                    color_name = r.name.lower().split("color- ")[1]
                    d[color_name] = Snowflake(r.id)

            # logger.debug(f"color roles: {d}")
            self.colorRoles[g.id] = d
        self.mutex.release()

    @commands.command(name='reload_colors', hidden=True)
    @commands.check_any(is_bot_admin(), commands.has_permissions(administrator=True), commands.is_owner())
    @commands.max_concurrency(1, wait=True)
    async def reload_colors(self, ctx):
        await self.reload()

    async def print_colors(self, ctx: discord.ext.commands.Context):
        g: discord.Guild = ctx.guild
        d: dict = self.colorRoles[g.id]

        roles = []
        for r in d.keys():
            roles.append(r)

        await ctx.send(f"```{', '.join(roles)}```")

    # do not use outside of color command function
    async def remove_roles(self, ctx: discord.ext.commands.Context):

        g: discord.Guild = ctx.guild
        member: discord.member.Member = g.get_member(ctx.author.id)

        d: dict = self.colorRoles[g.id]

        to_remove = []
        for r in d.values():
            for mr in member.roles:
                if r.id == mr.id:
                    to_remove.append(r)

        await member.remove_roles(*to_remove, reason="Color Command", atomic=True)

    @commands.command(name='color', help="Choose your name color")
    @commands.cooldown(type=commands.BucketType.user, rate=1, per=3)
    async def color(self, ctx: discord.ext.commands.Context, color: str):
        self.mutex.acquire()
        g: discord.Guild = ctx.guild
        member: discord.member.Member = g.get_member(ctx.author.id)
        color = color.lower()

        if color == "list":
            await self.print_colors(ctx)
        else:
            d: dict = self.colorRoles[g.id]

            if d is None:
                await ctx.send(f"{ctx.author.mention} could not find any color roles in this server!")
            else:
                try:
                    r = d[color]

                    await self.remove_roles(ctx)
                    await member.add_roles(r)
                    await ctx.send(f"{ctx.author.mention} successfully changed your color to {color}")
                except KeyError:
                    await ctx.send(
                        f"{ctx.author.mention} could not find any such color!\n ```{self.bot.command_prefix}{ctx.command.name} list``` to view available colors")

        self.mutex.release()

    @color.error
    async def color_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.CommandOnCooldown):
            await ctx.send(f"{ctx.author.mention} {error}")
        else:
            logger.error(f"color error: {error}")
