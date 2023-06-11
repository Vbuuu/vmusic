from cooldowns import cooldown, SlashBucket
from nextcord import slash_command, Interaction, Member
from nextcord.ext.commands import Cog, Bot

from src.ApiKeys import guildIds
from src.Checks import blacklisted


class Fun(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command(name="aimlab", description="Aimlab for quang", guild_ids=guildIds)
    @blacklisted()
    @cooldown(1, 60, SlashBucket.author)
    async def aimlab(self, interaction: Interaction, member: Member):
        await interaction.response.send_message(f"AIMLAB IST FREE {member.mention}!")


def setup(bot: Bot):
    bot.add_cog(Fun(bot))