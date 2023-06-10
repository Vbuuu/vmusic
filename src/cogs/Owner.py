import nextcord
from nextcord import slash_command, Interaction, Guild, SelectOption, ButtonStyle
from nextcord.ext.application_checks import is_owner
from nextcord.ext.commands import Cog, Bot, Context, CommandError
from nextcord.ui import View, Select, button, Button

from src.ApiKeys import configGuildId
from src.Utils import logger


class ServerLeaveView(View):
    def __init__(self, bot: Bot):
        super().__init__()
        self.selection = ServerLeaveSelect(bot.guilds)
        self.add_item(self.selection)
        self.bot = bot

    @button(label="Confirm", style=ButtonStyle.green)
    async def confirm(self, button: Button, interaction: Interaction):
        guilds = []
        for guildId in self.selection.values:
            guild = self.bot.get_guild(int(guildId))
            if guild is None:
                logger.error(f"No guild with the id {guildId} found!")  # No guild found
                return
            await guild.leave()
            guilds.append(guild.name)

        await interaction.response.send_message(f"Left: {', '.join(guilds)}")


class ServerLeaveSelect(Select):
    def __init__(self, guilds: list):
        options = []
        for guild in guilds:
            options.append(SelectOption(label=guild.name, value=str(guild.id), description=guild.description))

        super().__init__(placeholder="Select an guild", max_values=len(guilds), min_values=1, options=options)


class Owner(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command(name="server", description="Leave/List Servers", guild_ids=[configGuildId])
    @is_owner()
    async def server(self, interaction: Interaction):
        await interaction.response.send_message("You have to choose Edit/Leave/List")

    @server.subcommand(name="leave", description="Leave a selected server")
    async def serverLeave(self, interaction: Interaction):
        await interaction.response.send_message(view=ServerLeaveView(self.bot))

    @server.subcommand(name="list", description="Lists all servers the bot is currently on")
    async def serverList(self, interaction: Interaction):

        servers = ""

        for guild in self.bot.guilds:
            servers += f"{guild.name} ({guild.id}) \n"

        await interaction.response.send_message(servers)

    @server.error
    async def configError(self, ctx: Context, error: CommandError):
        await ctx.send(error, delete_after=3)


def setup(bot: Bot):
    bot.add_cog(Owner(bot))
