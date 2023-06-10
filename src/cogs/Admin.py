from nextcord import user_command, Interaction, Member, ApplicationInvokeError, slash_command, SlashOption
from nextcord.ext.application_checks import has_permissions
from nextcord.ext.commands import Cog, Bot, Context, CommandError

from src.ApiKeys import guildIds
from src.Config import addToBlacklist, removeFromBlacklist


class Admin(Cog):
    def __int__(self, bot: Bot):
        self.bot = bot

    @user_command(name="Kick Member", guild_ids=guildIds)
    @has_permissions(kick_members=True)
    async def kickU(self, interaction: Interaction, member: Member):
        try:
            await member.kick(reason=f"Kicked by {interaction.user.name}")
            await interaction.response.send_message(f"Kicked {member.name+'#'+member.discriminator} by {interaction.user.name+'#'+interaction.user.discriminator}")
        except ApplicationInvokeError:
            await interaction.response.send_message(f"I cant kick {member.name+'#'+member.discriminator} because I "
                                                    "have insufficient permissions!")

    @kickU.error
    async def kickUError(self, ctx: Context, error: CommandError):
        await ctx.send(error, delete_after=3)

    @slash_command(name="clear", description="Clears chat messages", guild_ids=guildIds)
    @has_permissions(manage_messages=True)
    async def clear(self, interaction: Interaction,
                    amount: int = SlashOption(name="amount", description="How many messages should be cleared",
                                              required=False, min_value=2, max_value=999, default=0)):
        await interaction.response.send_message(f"Clearing the chat!", ephemeral=True)
        await interaction.channel.purge() if amount == 0 else await interaction.channel.purge(limit=amount)

    @clear.error
    async def clearError(self, ctx: Context, error: CommandError):
        await ctx.send(error, delete_after=3)

    @slash_command(name="blacklist", description="Blacklist Add/Remove")
    @has_permissions(administrator=True)
    async def blacklist(self, interaction: Interaction,member: Member, action: str = SlashOption(name="action", description="What you want to do", choices=["Add", "Remove"], required=True)):
        if action == "Add":
            addToBlacklist(interaction.guild.id, [str(member.id)])
        elif action == "Remove":
            removeFromBlacklist(interaction.guild.id, [str(member.id)])


def setup(bot: Bot):
    bot.add_cog(Admin(bot))
