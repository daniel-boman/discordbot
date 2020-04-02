import inspect
import discord
import os
import signal

from discord.ext import commands
from loguru import logger

from modules import is_bot_admin, send_pastebin


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='eval', hidden=True)
    @is_bot_admin()
    async def _eval(self, ctx, *, code):
        code = "".join(code)

        code = compile(code, "abc", "single")

        __eval = None

        try:
            __eval = eval(code)
            if inspect.isawaitable(__eval):
                __eval = await __eval

        except Exception as e:
            logger.error(f"error in eval: {e}")

        try:
            await ctx.send(__eval)
        except discord.HTTPException as e:
            if "In content: Must be 2000 or fewer in length".lower() in e.text.lower():
                await send_pastebin(__eval, ctx)

    @commands.command(name='exec', hidden=True)
    @is_bot_admin()
    async def _exec(self, ctx, *, code):
        code = "".join(code)

        code = compile(code, "abc", "exec")

        __eval = None

        try:
            __eval = exec(code)
            if inspect.isawaitable(__eval):
                __eval = await __eval

        except Exception as e:
            logger.error(f"error in exec: {e}")

        try:
            await ctx.send(__eval)
        except discord.HTTPException as e:
            if "In content: Must be 2000 or fewer in length".lower() in e.text.lower():
                await send_pastebin(__eval, ctx)

    @commands.command(name='restart', hidden=True)
    @is_bot_admin()
    async def _restart(self, ctx):
        await ctx.send("Sending quit signal now.")
        os.kill(os.getpid(), signal.SIGTERM)
