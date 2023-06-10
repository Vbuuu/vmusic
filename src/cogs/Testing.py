from nextcord import slash_command, Interaction, SlashOption
from nextcord.ext import commands
from nextcord.ext.application_checks import has_permissions
from nextcord.ext.commands import Bot, Context, CommandError

from src.ApiKeys import guildIds


class Testing(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command(name="hello", description="Greet the bot", guild_ids=guildIds)
    async def hello(self, interaction: Interaction):
        await interaction.response.send_message(f"Fuck off {interaction.user.display_name}!")

    @slash_command(name="ping", description="Pong!", guild_ids=guildIds)
    async def ping(self, interaction: Interaction):
        await interaction.response.send_message(f"Pong ({int(self.bot.latency*1000)}ms)", delete_after=10)


def setup(bot: Bot):
    bot.add_cog(Testing(bot))
