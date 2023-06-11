from nextcord import user_command, Interaction, Member, ApplicationInvokeError, slash_command, SlashOption, Embed, \
    Colour
from nextcord.ext.application_checks import has_permissions
from nextcord.ext.commands import Cog, Bot

from src.ApiKeys import guildIds
from src.Checks import blacklisted
from src.JsonConfig import addToBlacklist, removeFromBlacklist


class Admin(Cog):
    def __int__(self, bot: Bot):
        self.bot = bot

    @user_command(name="Kick Member", guild_ids=guildIds)
    @has_permissions(kick_members=True)
    @blacklisted()
    async def kickU(self, interaction: Interaction, member: Member):
        try:
            await member.kick(reason=f"Kicked by {interaction.user.name}")
            await interaction.response.send_message(f"Kicked {member.name+'#'+member.discriminator} by {interaction.user.mention}")
        except ApplicationInvokeError:
            await interaction.response.send_message(f"I cant kick {member.name+'#'+member.discriminator} because I "
                                                    "have insufficient permissions!")

    @slash_command(name="clear", description="Clears chat messages", guild_ids=guildIds)
    @has_permissions(manage_messages=True)
    @blacklisted()
    async def clear(self, interaction: Interaction,
                    amount: int = SlashOption(name="amount", description="How many messages should be cleared",
                                              required=False, min_value=2, max_value=999, default=0)):
        await interaction.response.send_message(f"Clearing the chat!", ephemeral=True)
        await interaction.channel.purge() if amount == 0 else await interaction.channel.purge(limit=amount)

    @slash_command(name="blacklist", description="Blacklist Add/Remove")
    @has_permissions(administrator=True)
    @blacklisted()
    async def blacklist(self, interaction: Interaction, member: Member, action: str = SlashOption(name="action", description="What you want to do", choices=["Add", "Remove"], required=True), reason: str = SlashOption(name="reason", description="Describe why you are doing this", required=False)):
        if action == "Add":
            addToBlacklist(interaction.guild.id, [member.id])
            embed = Embed(title="Blacklist", description=f"{interaction.user.mention} has blacklisted {member.mention}", colour=Colour.red())
            embed.add_field(name="Reason: ", value=reason if reason is not None else "No Reason specified!")

            await interaction.response.send_message(embed=embed)
        elif action == "Remove":
            removeFromBlacklist(interaction.guild.id, [member.id])

            embed = Embed(title="Blacklist", description=f"{interaction.user.mention} has un blacklisted {member.mention}",colour=Colour.green())
            embed.add_field(name="Reason: ", value=reason if reason is not None else "No Reason specified!")

            await interaction.response.send_message(embed=embed)


def setup(bot: Bot):
    bot.add_cog(Admin(bot))
