from nextcord import slash_command, Interaction, Member
from nextcord.ext.commands import Cog, Bot, Context, CommandError

from src.ApiKeys import guildIds


class Fun(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command(name="aimlab", description="Aimlab for quang", guild_ids=guildIds)
    async def aimlab(self, interaction: Interaction, member: Member):
        await interaction.response.send_message(f"AIMLAB IST FREE {member.mention}!")

    @aimlab.error
    async def aimlabError(self, ctx: Context, error: CommandError):
        await ctx.send(error, delete_after=3)


def setup(bot: Bot):
    bot.add_cog(Fun(bot))