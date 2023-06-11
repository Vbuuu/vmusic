import json
import os

import jsbeautifier
from nextcord.ext.commands import when_mentioned_or

from src.Utils import logger

_directory = "./../run/configs/"
_configFiles = {}


def collect():
    logger.debug("Collecting configs!")
    if not os.path.exists(_directory):
        os.makedirs(_directory)

    for configFile in os.listdir(_directory):
        if configFile.endswith(".json"):
            _configFiles[configFile[:-5]] = configFile


def _getFile(guildId: int):
    collect()
    try:
        file = _configFiles[str(guildId)]
    except KeyError:
        _createConfig(guildId)
        file = _configFiles[str(guildId)]

    return file


def _getJson(guildId: int):
    file = _getFile(guildId)
    with open(_directory + file, "r") as f:
        data = json.load(f)
        f.close()
        return data


def _setJson(guildId: int, data):
    file = _getFile(guildId)

    with open(_directory + file, "w") as f:
        options = jsbeautifier.default_options()
        options.indent_size = 2
        f.write(jsbeautifier.beautify(json.dumps(data), options))
        f.close()


def _createConfig(guildId: int):
    defaultConfig = {
        "main": {
            "prefix": ".",
            "blacklist": []
        },
        "voice": {
            "joinSound": True
        }
    }

    if not os.path.exists(_directory + str(guildId) + ".json"):
        logger.info(f"Creating new config for {guildId}!")
        with open(_directory + str(guildId) + ".json", "w") as f:
            options = jsbeautifier.default_options()
            options.indent_size = 2
            f.write(jsbeautifier.beautify(json.dumps(defaultConfig), options))
            f.close()

    collect()


def setupGuildConfigs(guilds: list):
    for guild in guilds:
        _createConfig(guild.id)


# main
def setPrefix(guildId: int, value: str):
    data = _getJson(guildId)
    data["main"]["prefix"] = value
    _setJson(data)


def getPrefix(guildId: int):
    data = _getJson(guildId)
    return data["main"]["prefix"]


def getPrefixBot(bot, message):
    if not message.guild:
        return when_mentioned_or(".")(bot, message)
    else:
        return when_mentioned_or(getPrefix(message.guild.id))(bot, message)


def getBlacklist(guildId: int) -> list[int]:
    data = _getJson(guildId)
    return data["main"]["blacklist"]


def setBlacklist(guildId: int, newList: list[int]):
    data = _getJson(guildId)
    data["main"]["blacklist"] = newList
    _setJson(guildId, data)


def addToBlacklist(guildId: int, values: list[int]):
    newList = getBlacklist(guildId)

    for value in values:
        newList.append(value)

    setBlacklist(guildId, newList)


def removeFromBlacklist(guildId: int, values: list[int]):
    newList = getBlacklist(guildId)

    for value in values:
        if value in newList:
            newList.remove(value)

    setBlacklist(guildId, newList)


# voice
def setJoinSound(guildId: int, value: bool):
    data = _getJson(guildId)
    data["voice"]["joinSound"] = value
    _setJson(guildId, data)


def getJoinSound(guildId: int):
    data = _getJson(guildId)
    return data["voice"]["joinSound"]
