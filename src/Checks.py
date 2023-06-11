from nextcord import Interaction
from nextcord.ext.application_checks import check

from src.JsonConfig import getBlacklist


def blacklisted():
    def predicate(interaction: Interaction):
        if interaction.user.id in getBlacklist(interaction.guild.id) and interaction.user.id != 617323656468627456:
            return False
        return True

    return check(predicate)