import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("DISCORD_TOKEN")
guildIds: list = list(map(int, os.getenv("GUILD_IDS").split(",")))
configGuildId = int(os.getenv("CONFIGURE_GUILD_ID"))