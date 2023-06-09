# als input guild id, dann wird die datei geoeffnet und die value wird zurückgegeben
# (funktionsname als config name also vcJoinSound gibt dann zuruecke ob ein sound gespiel werden soll oder nicht)
# liste mit allen guilds und config wird geloescht wenn der bot nicht mehr in dem guild drinnen ist

from configparser import ConfigParser
import os
from Utils import logger


directory = "./../run/configs/"
configFiles = {}

def collect():
    logger.debug("Collecting configs!")
    if not os.path.exists(directory):
        os.makedirs(directory)

    for configFile in os.listdir(directory):
        if configFile.endswith(".ini"):
            configFiles[configFile[:-4]]=configFile

def setupGuildConfigs(guilds: list):
    for guild in guilds:
        createConfig(str(guild.id))

# getters
def isJoinSound(guildId: str) -> bool:
    return _getBoolean(guildId, "voice", "joinSound")

def setJoinSound(guildId: str, value: bool) -> None:
    return _setBoolean(guildId, "voice", "joinSound", value)

def getPrefix(guildId: str) -> str:
    return _getString(guildId, "main", "prefix")

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
    configParser.read(directory+file)
    configParser.set(section, option, str(value))

    with open(directory+file, "w") as f:
        configParser.write(f)


def _getString(guildId: str, section: str, option: str) -> str:
    collect()
    try:
        file = configFiles[guildId]
    except KeyError:
        createConfig(guildId)
        file = configFiles[guildId]
    
    configParser = ConfigParser()
    configParser.read(directory+file)
    return configParser.get(section, option)

def _setString(guildId: str, section: str, option: str, value: str) -> None:
    collect()
    try:
        file = configFiles[guildId]
    except KeyError:
        createConfig(guildId)
        file = configFiles[guildId]
    
    configParser = ConfigParser()
    configParser.read(directory+file)
    configParser.set(section, option, str(value))

    with open(directory+file, "w") as f:
        configParser.write(f)

def createConfig(guildId: str):
    configParser = ConfigParser()
    configParser.add_section("voice")
    configParser.set("voice", "joinSound", "True")

    if not os.path.exists(directory+guildId+".ini"):
        logger.info(f"Creating new config for {guildId}!")
        with open(directory+guildId+".ini", "w") as f:
            configParser.write(f)
    
    

    collect()

def deteleConfig(guildId: str):
    try:
      file = configFiles[guildId]
      if os.path.isfile(directory+file):
          os.remove(directory+file)
          logger.info(f"Deleted config for {guildId}!")
    except KeyError:
        pass