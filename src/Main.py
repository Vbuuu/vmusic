
import os
from nextcord import Intents
from dotenv import load_dotenv
from nextcord.ext import commands

from ApiKeys import *
from Config import collect, setupGuildConfigs
from Utils import logger, setupLogger

load_dotenv()


intents = Intents.all()
bot = commands.Bot(command_prefix=".", intents=intents)

def setupCogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f"cogs.{filename[:-3]}")
            logger.info(f"Loaded {filename[:-3]} extension!")

@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user} on {len(bot.guilds)} servers!")
    setupGuildConfigs(bot.guilds)

# main
setupLogger()
setupCogs()
collect()
bot.run(token)