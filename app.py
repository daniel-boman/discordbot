import os
import bot


def start():
    b = bot.new_bot()

    #    await b.login(token=os.getenv("DISCORD_TOKEN"))
    #    await b.connect()

    b.run(os.getenv("DISCORD_TOKEN"))


start()
