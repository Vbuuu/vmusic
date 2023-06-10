# als input guild id, dann wird die datei geoeffnet und die value wird zurückgegeben
# (funktionsname als config name also vcJoinSound gibt dann zuruecke ob ein sound gespiel werden soll oder nicht)
# liste mit allen guilds und config wird geloescht wenn der bot nicht mehr in dem guild drinnen ist
import json
from configparser import ConfigParser
import os

from nextcord.ext.commands import when_mentioned_or

from Utils import logger

directory = "./../run/configs/"
configFiles = {}


def collect():
    logger.debug("Collecting configs!")
    if not os.path.exists(directory):
        os.makedirs(directory)

    for configFile in os.listdir(directory):
        if configFile.endswith(".ini"):
            configFiles[configFile[:-4]] = configFile


def setupGuildConfigs(guilds: list):
    for guild in guilds:
        createConfig(str(guild.id))


# getters
def isJoinSound(guildId: int) -> bool:
    return _getBoolean(str(guildId), "voice", "joinSound")


def setJoinSound(guildId: int, value: bool) -> None:
    return _setBoolean(str(guildId), "voice", "joinSound", value)


def getPrefix(guildId: int) -> str:
    return _getString(str(guildId), "main", "prefix")


def getPrefixBot(bot, message):
    if not message.guild:
        return when_mentioned_or(".")(bot, message)
    else:
        return when_mentioned_or(getPrefix(message.guild.id))(bot, message)


def setPrefix(guildId: int, value: str) -> None:
    return _setString(str(guildId), "main", "prefix", value)


def setBlacklist(guildId: int, value: list) -> None:
    return _setList(str(guildId), "main", "blacklist", value)


def addToBlacklist(guildId: int, value: list[str]) -> None:
    return _appendToList(str(guildId), "main", "blacklist", value)


def removeFromBlacklist(guildId: int, value: list[str]) -> None:
    return _removeFromList(str(guildId), "main", "blacklist", value)


def _getBoolean(guildId: str, section: str, option: str) -> bool:
    collect()
    try:
        file = configFiles[guildId]
    except KeyError:
        createConfig(guildId)
        file = configFiles[guildId]

    configParser = ConfigParser()
    configParser.read(directory + file)
    return configParser.getboolean(section, option)


def _setBoolean(guildId: str, section: str, option: str, value: bool) -> None:
    collect()
    try:
        file = configFiles[guildId]
    except KeyError:
        createConfig(guildId)
        file = configFiles[guildId]

    configParser = ConfigParser()
    configParser.read(directory + file)
    configParser.set(section, option, str(value))

    with open(directory + file, "w") as f:
        configParser.write(f)


def _getString(guildId: str, section: str, option: str) -> str:
    collect()
    try:
        file = configFiles[guildId]
    except KeyError:
        createConfig(guildId)
        file = configFiles[guildId]

    configParser = ConfigParser()
    configParser.read(directory + file)
    return configParser.get(section, option)


def _setString(guildId: str, section: str, option: str, value: str) -> None:
    collect()
    try:
        file = configFiles[guildId]
    except KeyError:
        createConfig(guildId)
        file = configFiles[guildId]

    configParser = ConfigParser()
    configParser.read(directory + file)
    configParser.set(section, option, str(value))

    with open(directory + file, "w") as f:
        configParser.write(f)


def _setList(guildId: str, section: str, option: str, value: list) -> None:
    collect()
    try:
        file = configFiles[guildId]
    except KeyError:
        createConfig(guildId)
        file = configFiles[guildId]

    configParser = ConfigParser()
    configParser.read(directory+file)
    configParser.set(section, option, "["+",".join(value)+"]")

    with open(directory + file, "w") as f:
        configParser.write(f)


def _getList(guildId: str, section: str, option) -> list:
    collect()
    try:
        file = configFiles[guildId]
    except KeyError:
        createConfig(guildId)
        file = configFiles[guildId]

    configParser = ConfigParser()
    configParser.read(directory + file)
    return list(map(str, json.loads(configParser.get(section, option))))


def _appendToList(guildId: str, section: str, option: str, values: list[str]) -> None:
    list = _getList(guildId, section, option)

    for value in values:
        if value not in list:
            list.append(value)

    print(list)

    _setList(guildId, section, option, list)


def _removeFromList(guildId: str, section: str, option: str, values: list[str]) -> None:
    list  = _getList(guildId, section, option)

    for value in values:
        if value in list:
            list.remove(value)

    print(list)


def createConfig(guildId: str):
    configParser = ConfigParser()
    configParser.add_section("main")
    configParser.add_section("voice")

    configParser.set("main", "prefix", ".")
    configParser.set("main", "blacklist", "[]")
    configParser.set("voice", "joinSound", "True")

    if not os.path.exists(directory + guildId + ".ini"):
        logger.info(f"Creating new config for {guildId}!")
        with open(directory + guildId + ".ini", "w") as f:
            configParser.write(f)

    collect()


def deleteConfig(guildId: str):
    try:
        file = configFiles[guildId]
        if os.path.isfile(directory + file):
            os.remove(directory + file)
            logger.info(f"Deleted config for {guildId}!")
    except KeyError:
        pass
