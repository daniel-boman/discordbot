import os
import bot
from loguru import logger
import sys

___VERSION___ = "[v0.1.0]"

config = {
    "handlers": [
        {"sink": sys.stdout, "format": ___VERSION___ + " [{time:YYYY-MM-DD at HH:mm:ss}] [{level}]: {message}"}
    ],
}

logger.configure(**config)

logger.info("Now loading...")


def start():
    b = bot.new_bot(os.getenv("COMMAND_PREFIX", "!"), os.getenv("BOT_DESCRIPTION", "A discord bot"))

    b.run(os.getenv("DISCORD_TOKEN"))


start()
