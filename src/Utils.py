# https://stackoverflow.com/questions/237079/how-do-i-get-file-creation-and-modification-date-times

from datetime import datetime
import gzip
import logging
import os
import platform
import sys

logger = logging.getLogger("vmusic")


def setupLogger():
    directory = "./../run/logs/"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # renames older log files
    if os.path.exists(directory + "latest.log"):
        creationDate = getCreationDate(directory + "latest.log")
        filename = creationDate

        if os.path.exists(directory + filename + ".gz"):
            counter = 2
            while os.path.exists(directory + filename + "-" + str(counter) + ".gz"):
                counter += 1
            filename = creationDate + "-" + str(counter)

        with open(directory + "latest.log", "r") as lf:
            with gzip.open(directory + filename + ".gz", "w") as gf:
                gf.write(bytes(lf.read(), "utf-8"))

    logger.setLevel(logging.INFO)
    # fileHandler = logging.FileHandler("./../run/logs/latest.log", encoding="utf-8", mode="w")
    streamHandler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] (%(name)s) %(message)s", datefmt="%H:%M:%S")
    # fileHandler.setFormatter(formatter)
    streamHandler.setFormatter(formatter)

    # logger.addHandler(fileHandler)
    logger.addHandler(streamHandler)


def getCreationDate(path: str):
    if platform.system() == "Windows":
        return _unixToDate(os.path.getctime(path))
    else:
        stat = os.stat(path)
        try:
            return _unixToDate(stat.st_birthtime)
        except AttributeError:
            return _unixToDate(stat.st_mtime)


def _unixToDate(timestamp: float):
    return datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d")
