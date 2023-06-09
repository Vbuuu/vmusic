from nextcord import slash_command, Interaction, SlashOption
from nextcord.ext import commands
from ApiKeys import guildIds

class Testing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    
    @slash_command(name="hello", description="Greet the bot", guild_ids=guildIds)
    async def hello(self, interaction: Interaction):
        await interaction.response.send_message(f"Fuck off {interaction.user.display_name}!")
    
    @slash_command(name="clear", description="Clears chat messages", guild_ids=guildIds)
    async def clear(self, interaction: Interaction, amount: int = SlashOption(name="amount", description="How many messages should be cleared", required=False, min_value=2, max_value=999, default=0)):
        await interaction.response.send_message(f"Clearing the chat!", ephemeral=True)
        await interaction.channel.purge() if amount == 0 else await interaction.channel.purge(limit=amount)
        print(amount)


def setup(bot):
    bot.add_cog(Testing(bot))