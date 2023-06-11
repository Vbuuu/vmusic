from cooldowns import cooldown, SlashBucket
from nextcord import slash_command, Interaction
from nextcord.ext import commands
from nextcord.ext.commands import Bot

from src.ApiKeys import guildIds
from src.Checks import blacklisted


class Testing(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command(name="hello", description="Greet the bot", guild_ids=guildIds)
    @blacklisted()
    async def hello(self, interaction: Interaction):
        await interaction.response.send_message(f"Fuck off {interaction.user.display_name}!")

    @slash_command(name="ping", description="Pong!", guild_ids=guildIds)
    @blacklisted()
    @cooldown(1, 10, SlashBucket.author)
    async def ping(self, interaction: Interaction):
        await interaction.response.send_message(f"Pong ({int(self.bot.latency*1000)}ms)", delete_after=10)


def setup(bot: Bot):
    bot.add_cog(Testing(bot))
