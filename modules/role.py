import discord

from discord.ext import commands
from loguru import logger


class Role(commands.Cog):
    bot: discord.ext.commands.Bot

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='role',
                      help="Choose your role. Cannot be changed after it is set. Available options are: Weeb Trash "
                           "and Normie")
    @commands.cooldown(type=commands.BucketType.user, rate=1, per=3)
    async def role(self, ctx: discord.ext.commands.Context, *role):
        role = ' '.join(role)

        if role.lower() not in "normie" and role.lower() not in "weeb trash":
            await ctx.send_help(ctx.command.name)
            return


        g: discord.Guild = ctx.guild

        member = g.get_member(ctx.command.name)

        to_add = None

        for r in g.roles:
            if r.name.lower() in role.lower():
                to_add = r

        if to_add is None:
            await ctx.send_help(ctx.command.name)
            return

        if isinstance(member, discord.member.Member):
            if next((r for r in member.roles if str(r.name).lower() in ["weeb trash", "normie"]), None) is None:
                await member.add_roles(to_add)
                await ctx.send(f"{ctx.author.mention} you are now {to_add.name}!")
            else:
                await ctx.send(f"{ctx.author.mention} you have already selected a role!")
        else:
            logger.error(f"author != member {type(member)}")

    @role.error
    async def role_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send_help(ctx.command.name)
        else:
            await ctx.send(f"{ctx.author.mention} {error}")

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
