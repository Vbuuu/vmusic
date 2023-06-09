from nextcord import slash_command, Interaction, SlashOption, ButtonStyle, Embed, Colour
from nextcord.ext import commands
from nextcord.interactions import Interaction
from nextcord.ui import View, Button, button
from ApiKeys import guildIds
from Config import setJoinSound, isJoinSound

class ConfigBooleanView(View):
    def __init__(self, name: str, guildId: str, setFunction, getFunction):
        super().__init__()
        self.setFunction = setFunction
        self.getFunction = getFunction
        self.guildId = guildId
        self.name = name
    
    @button(label="True", style=ButtonStyle.green)
    async def setTrue(self, button: Button, interaction: Interaction):
        self.setFunction(self.guildId, True)
        if self.getFunction(str(interaction.guild.id)):
            color = Colour.green()
        else:
            color = Colour.red()
        await interaction.response.edit_message(embed=Embed(title="Join Voice Sound", description=f"State: {self.getFunction(str(interaction.guild.id))}", color=color))
    
    @button(label="False", style=ButtonStyle.red)
    async def setFalse(self, button: Button, interaction: Interaction):
        self.setFunction(self.guildId, False)
        if self.getFunction(str(interaction.guild.id)):
            color = Colour.green()
        else:
            color = Colour.red()
        await interaction.response.edit_message(embed = Embed(title="Join Voice Sound", description=f"State: {self.getFunction(str(interaction.guild.id))}", color=color))

class ConfigManager(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    @slash_command(name="config", description="Changes bot config on your server", guild_ids=guildIds)
    async def config(
        self,
        interaction: Interaction,
        setting: str = SlashOption(
            name="setting",
            description="Which setting to change",
            choices=["JoinVoiceSound (Boolean)", "Prefix (String)"],
            required=True
        )
    ) -> None:
        if setting == "JoinVoiceSound (Boolean)":
            embedView = booleanEmbedView("Join Voice Sound", str(interaction.guild.id), setJoinSound, isJoinSound)
        await interaction.response.send_message(embed=embedView[0], view=embedView[1])

def booleanEmbedView(name: str, guildId: str, setFunction, getFunction):
    if getFunction(guildId):
        color = Colour.green()
    else:
        color = Colour.red()
    
    view = ConfigBooleanView(name, guildId, setFunction, getFunction)
    embed = Embed(title=name, description=f"State: {getFunction(guildId)}", color=color)

    return [embed, view]

def setup(bot):
    bot.add_cog(ConfigManager(bot))