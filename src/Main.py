import nextcord
from nextcord import Intents, Interaction, Embed, SlashOption
from nextcord.ext import commands
from nextcord.ext.help_commands import PaginatedHelpCommand

from ApiKeys import *
from Config import collect, setupGuildConfigs, getPrefixBot, getPrefix
from Utils import logger, setupLogger

load_dotenv()

intents = Intents.all()
bot = commands.Bot(command_prefix=getPrefixBot, intents=intents, help_command=PaginatedHelpCommand())
blacklist = ["Kick Member"]

# TODO: use nextwave musicplayer


def getAllCommands(ignoreBlacklisted = False) -> list[str]:
    cogsMap = bot.cogs
    commands = []

    for key in cogsMap:
        for command in cogsMap[key].application_commands:
            if command.name not in blacklist or ignoreBlacklisted:
                commands.append(command.name)

    return commands


def setupCogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f"cogs.{filename[:-3]}")
            logger.info(f"Loaded {filename[:-3]} extension!")


@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user} on {len(bot.guilds)} servers!")
    setupGuildConfigs(bot.guilds)
    await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.listening, name="/help"))


@bot.slash_command(name="help", description="Shows help", guild_ids=guildIds)
async def help(interaction: Interaction, command: str = SlashOption(name="command", description="The command you want to have more information about", required=False)):
    if command == None:
        helpMap = {}
        cogsMap = bot.cogs

        for key in cogsMap:
            commands = []
            for cmd in cogsMap[key].application_commands:
                if cmd.name not in blacklist:
                    commands.append((cmd.name, cmd.description))

            helpMap[key] = commands

        embed = Embed(title="VMUSIC Commands",
                      description="Use `/help [command]` for additional command information.")
        for key in helpMap:

            li = []
            for cmd in helpMap[key]:
                li.append(f"**/{cmd[0]}** : {cmd[1]}")

            embed.add_field(name=key, value="\n".join(li))

        await interaction.response.send_message(embed=embed)

    else:
        try:
            cogsMap = bot.cogs
            commands = ""

            for key in cogsMap:
                for cmd in cogsMap[key].application_commands:
                    if cmd.name not in blacklist and command == cmd.name:
                        commands = (cmd.name, cmd.description, key)

            embed = Embed(title=commands[2])
            embed.add_field(name="/"+commands[0], value=commands[1])

            await interaction.response.send_message(embed=embed)
        except IndexError:
            await interaction.response.send_message(f"Command {command} not found!", ephemeral=True)


# main
setupLogger()
setupCogs()
collect()
bot.run(token)
