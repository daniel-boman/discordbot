import requests
import json

from loguru import logger
from discord.ext import commands


class Snowflake(object):
    def __init__(self, id: int):
        self.id = id


def is_bot_admin():
    def predicate(ctx):
        return ctx.author.id == 112192451694833664

    return commands.check(predicate)


async def send_pastebin(content: str, ctx):
    link = paste(content)
    await ctx.send(f"{ctx.author.mention} {link}")


def paste(content) -> str:
    post = None
    try:

        post = requests.post("https://hastebin.com/documents", data=json.dumps(content))
    except ValueError as e:
        print(content)
        logger.error(f"error uploading paste: {e}", e)
        return post.json()

    return f"https://hastebin.com/{post.json()['key']}"
