from nextcord import slash_command, SlashOption, ButtonStyle, Embed, Colour
from nextcord.ext import commands
from nextcord.ext.application_checks import has_permissions
from nextcord.ext.commands import Bot, Context, CommandError
from nextcord.interactions import Interaction
from nextcord.ui import View, Button, button
from src.ApiKeys import guildIds
from src.Config import setJoinSound, isJoinSound, getPrefix, setPrefix


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
        await interaction.response.edit_message(
            embed=Embed(title="Join Voice Sound", description=f"State: {self.getFunction(str(interaction.guild.id))}",
                        color=color))

    @button(label="False", style=ButtonStyle.red)
    async def setFalse(self, button: Button, interaction: Interaction):
        self.setFunction(self.guildId, False)
        if self.getFunction(str(interaction.guild.id)):
            color = Colour.green()
        else:
            color = Colour.red()
        await interaction.response.edit_message(
            embed=Embed(title="Join Voice Sound", description=f"State: {self.getFunction(str(interaction.guild.id))}",
                        color=color))


class ConfigManager(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @slash_command(name="prefix", description="Changes the server prefix", guild_ids=guildIds)
    @has_permissions(administrator=True)
    async def prefix(self, interaction: Interaction, prefix: str = SlashOption(
        name="prefix",
        description="The new prefix",
        required=True
    )):
        if prefix is not None or prefix == "":
            setPrefix(str(interaction.guild.id), prefix)
            await interaction.response.send_message(f"Prefix changed to: {getPrefix(str(interaction.guild.id))}", ephemeral=True)
        else:
            await interaction.response.send_message(f"Invalid prefix.", ephemeral=True)

    @prefix.error
    async def prefixError(self, ctx: Context, error: CommandError):
        await ctx.send(error, delete_after=3)


    @slash_command(name="config", description="Changes bot config on your server", guild_ids=guildIds)
    @has_permissions(administrator=True)
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
        embedView = None
        if setting == "JoinVoiceSound (Boolean)":
            embedView = booleanEmbedView("Join Voice Sound", str(interaction.guild.id), setJoinSound, isJoinSound)
        elif setting == "Prefix (String)":
            embed = Embed(title="Prefix", description=f"Prefix currently set to: {getPrefix(str(interaction.guild.id))}"
                                                      "\n Use /prefix [prefix] to change it")

            await interaction.response.send_message(embed=embed)

        if embedView is not None:
            await interaction.response.send_message(embed=embedView[0], view=embedView[1], ephemeral=True)

    @config.error
    async def configError(self, ctx: Context, error: CommandError):
        await ctx.send(error, delete_after=3)


def booleanEmbedView(name: str, guildId: str, setFunction, getFunction):
    if getFunction(guildId):
        color = Colour.green()
    else:
        color = Colour.red()

    view = ConfigBooleanView(name, guildId, setFunction, getFunction)
    embed = Embed(title=name, description=f"State: {getFunction(guildId)}", color=color)

    return [embed, view]


def setup(bot: Bot):
    bot.add_cog(ConfigManager(bot))
