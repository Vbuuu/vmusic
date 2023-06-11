from asyncio import sleep
import os
from nextcord.ext import commands
from nextcord import Member, FFmpegPCMAudio, ClientException, VoiceState, slash_command, Interaction
from nextcord.ext.commands import Bot

from src.ApiKeys import guildIds
from src.Checks import blacklisted
from src.JsonConfig import getJoinSound
from src.Utils import logger


class Voice(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState):
        if before.channel == after.channel or member.id == self.bot.user.id:
            return
        if before.channel is None and getJoinSound(after.channel.guild.id):
            channel = member.voice.channel
            try:
                vc = await channel.connect()
                await sleep(.5)
                vc.play(FFmpegPCMAudio(os.path.dirname(__file__)+"/../sounds/sound.mp3"))

                while vc.is_playing():
                    await sleep(.1)
                await vc.disconnect()
            except ClientException as e:
                logger.error("", e)

    @slash_command(name="join", description="Joins your voice channel", guild_ids=guildIds)
    @blacklisted()
    async def join(self, interaction: Interaction):
        if interaction.user.voice and not interaction.guild.voice_client:
            await interaction.user.voice.channel.connect()
            await interaction.response.send_message("Joined your channel!", delete_after=2)
        else:
            await interaction.response.send_message(f"{interaction.user.mention} you are not in a voice channel or I am already in a voice channel!", delete_after=10)

    @slash_command(name="leave", description="Leaves your voice channel", guild_ids=guildIds)
    @blacklisted()
    async def leave(self, interaction: Interaction):
        if interaction.user.voice.channel:
            await interaction.guild.voice_client.disconnect()
            await interaction.response.send_message("Left your Voice Channel!", delete_after=2)
        else:
            await interaction.response.send_message(f"{interaction.user.mention} you are not in my voice channel!", delete_after=10)


def setup(bot: Bot):
    bot.add_cog(Voice(bot))
